import json
import os
import random
import string
from client import models
from setting_ads import models as setting_models



def random_string(length):
    characters = string.ascii_letters
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

def check_caption_file_exist(message_id):
    file_path=models.Filename.objects.get(message_id=message_id,is_caption=True).filename
    if os.path.exists(file_path):
        return True
    return False



def filter_caption(message_id: str, channel_to_id: str):
    message=models.Message.objects.get(message_id=message_id)

    if models.Message.objects.get(message_id=message_id).caption:
        if check_caption_file_exist(message_id=message_id):
            caption_file_path = models.Filename.objects.get(message_id=message.message_id, is_caption=True).filename

            channel_from= models.Message.objects.get(message_id=message_id).channel_from
            channel_to=setting_models.Channels.objects.get(channel_id=channel_to_id)

            keyword_texts = setting_models.KeywordChannelAds.objects.filter(channel=channel_from)
            keyword_text_list = [keyword.text for keyword in keyword_texts]

            my_channel_text=setting_models.KeywordChannelAds.objects.get(channel=channel_to).text

            with open(caption_file_path, 'r') as f:
                caption = f.read()
                caption = '\n'.join(line for line in caption.splitlines() if line.strip())
                for key_word in keyword_text_list:
                    caption = caption.replace(key_word, '')
                caption = caption + '\n' + my_channel_text
            return caption
        else:
            caption_file_path = models.Filename.objects.get(message_id=message.message_id, is_caption=True).filename
            with open(caption_file_path, 'r') as f:
                caption = f.read()
                caption = '\n'.join(line for line in caption.splitlines() if line.strip())
            return caption
    return None


def get_photo_filenames_by_message_id(message_id):
    messages = models.Filename.objects.filter(message_id=str(message_id), is_photo=True)
    photo_filenames = [message.filename for message in messages]
    return photo_filenames


def get_media_files_json_data(message_id):
    media_files = get_photo_filenames_by_message_id(message_id)
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


    from_channel = models.Message.objects.get(message_id=message_id).channel_from
    ##
    channel_configs = setting_models.Channel_config.objects.filter(from_channel=from_channel)
    channel_id_list = [channel_config.to_channel.channel_id for channel_config in channel_configs]
    ##
    data_list = []
    for ch_id in channel_id_list:
        caption = filter_caption(message_id,ch_id)
        media[0]['caption'] = caption
        media[0]['parse_mode'] = 'HTML'
        if caption is not None:
            data_list.append(
                {
                    'data': {'chat_id': ch_id, 'media': json.dumps(media)},
                    'files': files,
                    'token': setting_models.Channel_config.objects.get(to_channel__channel_id=ch_id,
                                                               from_channel=from_channel).bot.bot_token,
                    'channel_from': from_channel.channel_id,
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

