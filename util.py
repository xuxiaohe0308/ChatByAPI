import requests
from os import listdir
import json
from config import API_FILENAME, MODEL, URL, CONV_FILENAME
try:
    from config import PROXY_PORT
except:
    PROXY_PORT = 0


def get_apikey():

    if API_FILENAME not in listdir():
        with open(API_FILENAME, 'w') as f:
            f.write('')

        print('APIKey not found! Please paste your APIKey here, or paste into file \'{}\' later.'.format(API_FILENAME))
        apikey = input()

        with open(API_FILENAME, 'w') as f:
            f.write(apikey)

        return apikey

    with open(API_FILENAME, 'r') as f:
        apikey = f.read()
    return apikey


def send_request(message):

    headers = {"Content-Type": "application/json",
               "Authorization": "Bearer {}".format(get_apikey())
               }

    data = {"model": MODEL,
            "messages": message
            }

    if PROXY_PORT:
        proxies = {"http": "http://127.0.0.1:{}".format(PROXY_PORT), "https": "http://127.0.0.1:{}".format(PROXY_PORT)}
        response = requests.post(URL, json=data, headers=headers, proxies=proxies, timeout=300)
    else:
        response = requests.post(URL, json=data, headers=headers, timeout=300)

    if response.status_code >= 300 or response.status_code < 200:
        raise ConnectionError('Server response error! {}, \'{}\''.format(response.status_code, json.loads(response.content)['error']['message']))

    content = json.loads(response.content)
    return content


def read_conversation():
    if CONV_FILENAME in listdir():
        with open(CONV_FILENAME, 'r') as f:
            conversation = [json.loads(_) for _ in f.readlines()]
        return conversation
    return []


def write_conversation(conversation):
    with open(CONV_FILENAME, 'a') as f:
        f.writelines(json.dumps(conversation) + '\n')

