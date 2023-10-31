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
        caption = models.Filename.objects.filter(message_id=message_id, is_caption=True).last().filename
        channel= models.Channels.objects.get(channel_id=models.Message.objects.get(message_id=message_id).channel_from,my_channel=False)
        my_channel=models.Channel_config.objects.filter(from_channel=channel).last().to_channel

        keyword_texts = models.KeywordChannelAds.objects.filter(channel=channel)
        keyword_text_list = [keyword.text for keyword in keyword_texts]
        my_channel_text=models.KeywordChannelAds.objects.get(channel=my_channel).text

        with open(caption, 'r') as f:
            caption = f.read()
            for key_word in keyword_text_list:
                caption = caption.replace(key_word, '')
            caption = caption + '\n' + my_channel_text

        return caption
    return None


def get_photo_filenames_by_message_id(message_id):
    messages = models.Filename.objects.filter(message_id=str(message_id), is_photo=True)
    photo_filenames = [message.filename for message in messages]
    return photo_filenames


def get_media_files_json_data(message_id):
    media_files = get_photo_filenames_by_message_id(message_id)
    caption = filter_caption(message_id)
    media, files = [], {}
    for media_file in media_files:
        if media_file is not None:
            random_name = os.path.basename(media_file)
            media.append(
                {
                    'type': 'photo',
                    'media': f"attach://{random_name}",
                }
            )
            # Faylni byte ma'lumotga o'qish
            with open(media_file, 'rb') as f:
                file_data = f.read()
            files[random_name] = file_data

    media[0]['caption'] = caption
    media[0]['parse_mode'] = 'HTML'
    channel = models.Message.objects.get(message_id=message_id).channel_from
    ##
    channel_id = models.Channel_config.objects.filter(from_channel__channel_id=channel)
    channel_id_list = [channel.to_channel.channel_id for channel in channel_id]
    ##
    data_list = []
    for ch_id in channel_id_list:
        data_list.append(
            {
                'data': {'chat_id': ch_id, 'media': json.dumps(media)},
                'files': files,
                'token': models.Channel_config.objects.get(to_channel__channel_id=ch_id,
                                                           from_channel__channel_id=channel).bot.bot_token,
                'channel_from': channel,
                'message_id': message_id
            }
        )

    return data_list


async def write_caption(file_path, caption_text):
    try:
        with open(file_path, 'w') as f:
            f.write(caption_text)
        return True
    except:
        return False
