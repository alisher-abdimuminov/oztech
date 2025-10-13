import firebase_admin
from firebase_admin import credentials, messaging



cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)


def notify(notification, users):
    for user in users:
        if user.fcm_token:
            message = messaging.Message(
                notification=messaging.Notification(
                    title=notification.title,
                    body=notification.description,
                ),
                data={"type": notification.type},
                token=user.fcm_token,
            )

            try:
                response = messaging.send(message)
                print(f"Successfully sent message to topic: {response}")
            except Exception as e:
                print(f"Error sending message to topic: {e}")
