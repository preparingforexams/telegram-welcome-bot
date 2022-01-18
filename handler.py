import json
import random

_FILE_IDS = [
    # Saufen
    "CQACAgIAAxkDAAMGYAQ3hb7J8740ND6tbnwf9m7o7s8AAooKAAIVSiBITKyTWpm8keweBA",
    # Alkpause
    "CQACAgIAAxkDAAMHYAQ3qNopch3GK9ZgfFckciIikHAAAosKAAIVSiBICtvI62oH3_seBA",
    # Trinken
    "CQACAgIAAxkDAAMIYAQ-CYlzFAABOG5HIV4Z52M2pOpsAAKYCgACFUogSOiJTDCf_HlXHgQ",
    # Aktuelle Situation
    "CQACAgIAAxkDAAMnYBGy7xpSrNxeVGqU-hKkmvKVQVoAAlcLAAKJO4hIuBttZLzEECYeBA",
    # Komasaufen
    "CQACAgIAAxkBAANZYeaJDEyC6yYa1Qe8RYxfyawvb_IAAmoWAAItbjBLXvJA_jHnjIkjBA",
]


def handle_message(event, context):
    update = json.loads(event['body'])
    message = update['message']
    message_id = message['message_id']
    new_users = message.get('new_chat_members')
    if new_users:
        print(f"Got {len(new_users)} new users before filtering")
        new_users = list(filter(lambda u: not u['is_bot'], new_users))

    if not new_users:
        print("No new users")

        audio = message.get('audio')
        if audio:
            print(f"Audio file ID {audio['file_id']}")

        return {
            'statusCode': 204
        }

    file_id = random.choice(_FILE_IDS)
    body = {
        'method': "sendAudio",
        'chat_id': message['chat']['id'],
        'audio': file_id
    }

    if len(new_users) == 1:
        username = new_users[0]['first_name']
        body['reply_to_message_id'] = message_id
        body['allow_sending_without_reply'] = True
    else:
        username = "liebe Alkoholiker"

    body['caption'] = f"Willkommen, {username}"

    return json.dumps(body)
