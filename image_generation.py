# Creating images from scratch based on a text prompt
# https://platform.openai.com/docs/guides/images/introduction

from config import ROOT_URL, PROXY_PORT
from util import get_apikey
import requests
import json
import base64
from os import mkdir


URL = ROOT_URL + '/images/generations'
SIZE_MAP = {1:"256x256", 2:"512x512", 3:"1024x1024"}


def send_request(prompt, n=1, size=3):

    headers = {"Content-Type": "application/json",
               "Authorization": "Bearer {}".format(get_apikey())
               }

    data = {"prompt": prompt,
            "n": n,
            "size": SIZE_MAP[size],
            "response_format": "b64_json"
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


if __name__ == "__main__":

    print('Command-line image generation tool using openai-api.')
    print('-- Please type your text prompt below --')
    prompt = input()
    n = 0

    while True:
        print('-- Please type the image amount you want to generate (1~10) --')
        n = input()
        if not n.isdigit() or n <= '0' or n > '10':
            print('The amount must between 1 and 10. ')
            continue
        n = int(n)
        break
    content = send_request(prompt, n=n)

    try:
        mkdir('images')
    except:
        pass

    for i, item in enumerate(content['data']):
        img_png = base64.b64decode(item['b64_json'])
        with open('images/{}-{}.png'.format(prompt.replace(' ', '_'), i), 'wb') as f:
            f.write(img_png)
    print('Images were successfully generated and saved in \'images\' directory. ')
    