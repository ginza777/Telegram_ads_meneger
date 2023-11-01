from celery import shared_task

from client.models import Message, Filename
from log_info.models import SomeErrors,Message_log
from log_info.views import message_log_view
from sender.tasks import send_message
import os

def check_photo_caption_with_count(message_id):
    message = Message.objects.get(id=message_id)
    if message.photo_count>0:
        photo_file=Filename.objects.filter(message_id=message_id,is_photo=True)
        caption_file=Filename.objects.filter(message_id=message_id,is_caption=True)
        if photo_file.count()==message.photo_count and caption_file.count()==1:
            return True
        else:
            message_log_view(message, f"check_photo_with_count error message_id={message_id} photo_file.count()={photo_file.count()} message.photo_count={message.photo_count} caption_file.count()={caption_file.count()}")
            SomeErrors.objects.create(title=f"check_photo_with_count error",error=f"message_id={message_id} photo_file.count()={photo_file.count()} message.photo_count={message.photo_count} caption_file.count()={caption_file.count()}")
            return False


def check_files_existence(message_id):
    # Fetch image and caption file paths from the database
    message=Message.objects.get(id=message_id)
    image_file_paths = Filename.objects.filter(message_id=message_id, is_photo=True).values_list('filename', flat=True)
    caption_file_paths = Filename.objects.filter(message_id=message_id, is_caption=True).values_list('filename',
                                                                                                     flat=True)

    # Check if all image files exist
    all_image_files_exist = all(os.path.exists(image_path) for image_path in image_file_paths)

    # Check if all caption files exist
    all_caption_files_exist = all(os.path.exists(caption_path) for caption_path in caption_file_paths)

    if not all_image_files_exist:
        missing_image = next((image_path for image_path in image_file_paths if not os.path.exists(image_path)), None)
        if missing_image:
            #================[log start]================
            message_log_view(message, f"check_files_existence: IF NOT ALL_IMAGE_FILES_EXIST: TRY: MISSING_IMAGE={missing_image}")
            #================[log end]================

    if not all_caption_files_exist:
        missing_caption = next(
            (caption_path for caption_path in caption_file_paths if not os.path.exists(caption_path)), None)
        if missing_caption:
            #================[log start]================
            message_log_view(message, f"check_files_existence: IF NOT ALL_CAPTION_FILES_EXIST: TRY: MISSING_CAPTION={missing_caption}")

            #================[log end]================

    if all_image_files_exist and all_caption_files_exist:
        return True

    return  False

@shared_task(name='send_message')
def send_message_task():
    messages = Message.objects.all()
    for message in messages:
        if check_photo_caption_with_count(message_id=message.message_id):
            if check_files_existence(message_id=message.message_id):
                send_message(message_id=message.message_id)





@shared_task(name='delete_message')
def delete_message():
    print('Hello from celery')
    return 'Hello from celery'


