from pyfcm import FCMNotification

from django.conf import settings


class Notify:
    push_service = FCMNotification(api_key=settings.FCM_API_KEY)

    def __init__(self, message_body, registration_ids = None, data_message = None, message_title = None):
        self.message_title = message_title
        self.message_body = message_body
        self.data_message = data_message
        self.registration_ids = registration_ids

    def notify_device(self):
        self.push_service.notify_multiple_devices(
            registration_ids=self.registration_ids,
            message_title=self.message_title,
            message_body=self.message_body,
            data_message=self.data_message
        )
