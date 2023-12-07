"""
Author: Simon Lin (linwei85@gmail.com)

File: chat.py
Description: Defines the chat action of Character. 
This action means the character will chat to other role according to it's memory and recent chat history.
"""
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import yaml
from util.config import configuration
from util.common_util import get_chat_response



def chat(my_name:str, my_profile:str, my_memory:str, talk_to_name:str, saying: str, chat_history, floder_template=False):
    # check the parameter wether is valid
    if not my_name or not my_profile or not talk_to_name or not saying or not my_memory:
        return None
    
    # format the template
    with open(f"{floder_template}/gpt4/chat.yaml", 'r') as stream:
        try:
            template = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    template['talkToCharacter']['name'] = talk_to_name
    template['talkToCharacter']['saying'] = saying
    template['myCharacter']['name'] = my_name
    template['myCharacter']['profile'] = my_profile
    template['myCharacter']['memory'] = my_profile
    template['chatHistory'] = chat_history
    prompt = template['prompt'].format(**template)

    resp_txt = get_chat_response(configuration["model"], prompt, int(configuration["max_tokens"]))
    return resp_txt