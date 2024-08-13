import requests
import keras
import numpy as np
from config import TOKEN, CHAT_ID

__all__ = ['format_text', 'send_message']

def format_text(offer, square):
    model = keras.models.load_model('price_model.keras')
    x = np.array([square])
    _ = model.predict(x)
    price = int(_[0])
    text = (f'{offer['datetime']}\n{offer['price']} руб\n'
            f'Рекомендуем цену: {price} руб\n{offer['adress']}\n{offer['url']}')
    return text

def send_message(text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    requests.post(url=url, data={'chat_id': CHAT_ID, 'text': text})

def main():
    pass

if __name__ == '__main__':
    main()
