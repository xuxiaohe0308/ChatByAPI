# ChatGPT command-line chatting (Python)

Chat with ChatGPT in command line! It's more stable compared to browser-based chatting.

This is only for personal use.

## Usage

Python3

`pip3 install requests`

First, create a new file named `apikey` which includes your openai secret APIkey. This can be generated in https://platform.openai.com/account/api-keys

To launch a single-sentence chat, please use

`python singlechat.py`

To launch/continue a full conversation with prior messages referring functionality, please use

`python conversation.py`

The conversation history is saved in `conversation.txt`. To show the full conversation please use

`python show_conversation.py`

You can change your own proxy_port in `config.py`. For example, for Clash it's 7890 in default.

## Refs 

https://platform.openai.com/docs/api-reference/chat