import json
import os
import random
import shutil
import string
from asgiref.sync import sync_to_async
from client import models


def random_string(length):
    characters = string.ascii_letters
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


def filter_caption(message_id: str):
    if models.Message.objects.get(message_id=message_id).caption:
        caption = models.Filename.objects.get(message_id=message_id, is_caption=True).filename
        channel= models.Channels.objects.get(channel_id=models.Message.objects.get(message_id=message_id).channel_from,my_channel=False)
        my_channel=models.Channel_config.objects.get(from_channel=channel).to_channel

        keyword_texts = models.KeywordChannelAds.objects.filter(channel=channel)
        print('keyword text',keyword_texts)# Barcha bog'liq "KeywordChannelAds" obyektlarni olish
        keyword_text_list = [keyword.text for keyword in keyword_texts]
        print(keyword_text_list)
        my_channel_text=models.KeywordChannelAds.objects.get(channel=my_channel).text

        with open(caption, 'r') as f:
            caption = f.read()
            for key_word in keyword_text_list:
                caption = caption.replace(key_word, '')
            caption = caption + '\n' + my_channel_text

        return caption
    return None


def get_photo_filenames_by_message_id(message_id):
    # `message_id` orqali `Message` obyektini qidirish

    messages = models.Filename.objects.filter(message_id=str(message_id), is_photo=True)
    print(messages)
    # Agar `Message` topilsa, `photo_file` ning `filename` atributini olish
    photo_filenames = [message.filename for message in messages]
    print(photo_filenames)
    return photo_filenames


def get_media_files_json_data(message_id):
    media_files = get_photo_filenames_by_message_id(message_id)
    print('media files',media_files)
    caption = filter_caption(message_id)
    print('caption',caption)

    media, files = [], {}

    for media_file in media_files:
        if media_file is not None:
            random_name = random_string(5)
            print(random_name)
            print(media_file)
            media.append(
                {
                    'type': 'photo',
                    'media': f"attach://{random_name}",
                }
            )
            files[random_name] = open(media_file, "rb")
    media[0]['caption'] = caption
    media[0]['parse_mode'] = 'HTML'
    channel= models.Message.objects.get(message_id=message_id).channel_from
    channel_id=models.Channel_config.objects.get(from_channel__channel_id=channel).to_channel.channel_id
    data = {
        'chat_id': channel_id,
        'media': json.dumps(media)
    }
    print(data)
    print(files)
    return data, files


async def write_caption(file_path, caption_text):
    try:
        with open(file_path, 'w') as f:
            f.write(caption_text)
        return True
    except:
        return False
