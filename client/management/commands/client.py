import asyncio
from concurrent.futures import ThreadPoolExecutor

from asgiref.sync import sync_to_async
from django.core.management.base import BaseCommand
from telethon import TelegramClient, events
from telethon.tl.types import Message
from asyncio import Queue, create_task
from client.views import random_string
from client.models import Client_Settings, Channels, Filename
from client.models import Message as MessageModel

message_queue = Queue()
is_processing = False

# Bot va Client sozlamalari

env = Client_Settings.objects.last()
channels = list(Channels.objects.filter(my_channel=False).values_list('channel_link', flat=True))

# ThreadPoolExecutor obyektini yaratish
executor = ThreadPoolExecutor(max_workers=4)


async def process_queue(client):
    global is_processing
    while not message_queue.empty():
        is_processing = True
        event = await message_queue.get()
        if isinstance(event.message, Message) and hasattr(event.message, 'media') and event.message.media:
            if event.media.photo:
                if event.message.grouped_id is not None:
                    if event.message.grouped_id and event.message is not None and event.message.raw_text != '':
                        await process_grouped_media_with_caption(event, client)

                    if event.message.grouped_id and event.message.raw_text == '':
                        await process_grouped_media_without_caption(event, client)

                if event.message.grouped_id is None:
                    print("grouped_id yo'q")
                    if event.message.grouped_id is None and event.message is not None and event.message.raw_text != '':
                        print("rasm va caption bor")
                        await process_single_media_with_caption(event, client)

            print(100 * '*')
            message_queue.task_done()
        is_processing = False


async def main():
    client = TelegramClient(env.phone, env.api_id, env.api_hash)
    await client.start()

    @client.on(events.NewMessage(chats=channels))
    async def my_event_handler(event):
        if not is_processing:
            create_task(process_queue(client))
        await message_queue.put(event)

    await client.run_until_disconnected()


async def process_grouped_media_with_caption(event, client):
    print('grouped_id bor caption bor')
    photo = event.media.photo
    group_id = event.message.grouped_id
    channel_id = event.message.peer_id.channel_id
    print(channel_id)
    print('\n\n\n')
    caption = event.message.raw_text
    print(caption)
    caption_file = f'media/{group_id}/{group_id}.txt'
    photo_file = f'media/{group_id}/{group_id}-{random_string(7)}.jpeg'

    await client.download_media(photo, file=photo_file)
    await write_caption_to_file(caption_file, caption)
    await crate_message(message_id=group_id, channel_id=channel_id, single_photo=False, caption=caption_file,
                        photo_file=photo_file)


async def process_grouped_media_without_caption(event, client):
    print('grouped_id bor caption yoq')
    photo = event.media.photo
    group_id = event.message.grouped_id
    channel_id = event.message.peer_id.channel_id
    print(channel_id)
    print('\n\n\n')
    file_path = f'media/{group_id}/{group_id}-{random_string(7)}.jpeg'
    await client.download_media(photo, file=file_path)
    await crate_message(message_id=group_id, channel_id=channel_id, single_photo=False, caption=None,
                        photo_file=file_path)


async def process_single_media_with_caption(event, client):
    photo = event.media.photo
    message_id = event.message.id
    channel_id = event.message.peer_id.channel_id
    caption = event.message.raw_text
    print(caption)
    print('\n\n\n')
    print(message_id)
    print(channel_id)
    print('\n\n\n')
    file_path = f'media/{message_id}/{message_id}-{random_string(7)}.jpeg'
    caption_file = f'media/{message_id}/{message_id}.txt'
    await client.download_media(photo, file=file_path)
    await write_caption_to_file(caption_file, caption)
    await crate_message(message_id=message_id, channel_id=channel_id, single_photo=True, caption=caption_file,
                        photo_file=file_path)


@sync_to_async
def crate_message(message_id, channel_id, single_photo=False, photo_file=None, caption=None):
    message, created = MessageModel.objects.get_or_create(message_id=message_id)
    print(f"-100{channel_id}", '\n\n\n')
    if channel_id is not None:
        channel = Channels.objects.get(channel_id=f"-100{channel_id}", my_channel=False)
        print('get', channel)
        message.channel_from = channel.channel_id
    if photo_file is not None:
        file = Filename.objects.create(filename=photo_file,message_id=message_id, is_photo=True)
        file.save()
        message.photo = True
        message.photo_count = message.photo_count + 1
    if caption is not None:
        file = Filename.objects.create(filename=caption,message_id=message_id, is_caption=True)
        message.caption = True
        file.save()

    if single_photo:
        message.single_photo = True
        message.photo_count = 1
        message.photo = True


    message.save()

    try:
        MessageModel.objects.get(id=(message.id - 1), end=False)
        old_message = MessageModel.objects.get(id=message.id - 1)
        old_message.end = True
        old_message.save()

    except MessageModel.DoesNotExist:
        print('Message topilmadi')


async def write_caption_to_file(file_path, caption_text):
    try:
        with open(file_path, 'w') as f:
            f.write(caption_text)
        return True
    except:
        return False


class Command(BaseCommand):
    help = 'Starts the Telegram listener'

    def handle(self, *args, **options):
        asyncio.run(main())
