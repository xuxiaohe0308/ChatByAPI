import http.client
from util import send_request


if __name__ == '__main__':

    print('Command-line chatting tool using openai-api.')
    print('Note: This python script is only for single-sentence chat. '
          'For full conversation version please use \'conversation.py\'.')
    print('-- Please type your message below and begin your chat! --')

    resp = {}
    while True:
        msg = [{"role": "user", "content": input()}]
        while True:
            try:
                resp = send_request(msg)
                break
            except http.client.RemoteDisconnected:
                continue

        print('\033[0;32m{}\033[0m'.format(resp['choices'][0]['message']['content']))