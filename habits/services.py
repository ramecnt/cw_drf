from cw_drf.settings import TG_BOT_KEY
import requests


def send_tg_message(chat_id, text):
    params = {
        'text': text,
        'chat_id': chat_id
    }
    url = f'https://api.telegram.org/bot{TG_BOT_KEY}/sendMessage'
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Failed to send message: {response.text}")
    else:
        print(f"Message sent successfully to chat_id {chat_id}: {text}")


def is_today(frequency, start_date, today):
    delta = (today - start_date).days
    if frequency == 'daily':
        return True
    elif frequency == '3 days':
        return delta % 3 == 0
    elif frequency == 'weekly':
        return delta % 7 == 0
    return False
