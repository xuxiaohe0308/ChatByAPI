import requests
from os import listdir
import json
import tiktoken
from config import API_FILENAME, MODEL, URL, CONV_FILENAME, MAX_TOKENS
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
    if MAX_TOKENS:
        while num_tokens_from_messages(message) > MAX_TOKENS:
            if len(message) == 1:
                raise IndexError("Message too long!")
            message = message[1:]

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


# https://platform.openai.com/docs/guides/chat/introduction
def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301"):
  """Returns the number of tokens used by a list of messages."""
  try:
      encoding = tiktoken.encoding_for_model(model)
  except KeyError:
      encoding = tiktoken.get_encoding("cl100k_base")
  if model == "gpt-3.5-turbo-0301":  # note: future models may deviate from this
      num_tokens = 0
      for message in messages:
          num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
          for key, value in message.items():
              num_tokens += len(encoding.encode(value))
              if key == "name":  # if there's a name, the role is omitted
                  num_tokens += -1  # role is always required and always 1 token
      num_tokens += 2  # every reply is primed with <im_start>assistant
      return num_tokens
  else:
      raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.
  See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")
