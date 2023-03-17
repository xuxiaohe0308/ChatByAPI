from util import read_conversation


if __name__ == '__main__':
    conversation = read_conversation()
    for item in conversation:
        if item['role'] == 'user':
            print(item['content'])
        elif item['role'] == 'assistant':
            print('\033[0;32m{}\033[0m'.format(item['content']))
