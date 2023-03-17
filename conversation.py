import http.client
from util import send_request, read_conversation, write_conversation


if __name__ == '__main__':

    print('Command-line chatting tool using openai-api.')
    print('-- Please type your message below and begin your chat! --')

    conversation = read_conversation()
    resp = {}

    while True:
        user_msg = {"role": "user", "content": input()}
        conversation.append(user_msg)
        while True:
            try:
                resp = send_request(conversation)
                break
            except (http.client.RemoteDisconnected, ConnectionResetError):
                continue
        resp_msg = resp['choices'][0]['message']
        print('\033[0;32m{}\033[0m'.format(resp_msg['content']))
        conversation.append(resp_msg)
        write_conversation(user_msg)
        write_conversation(resp_msg)
