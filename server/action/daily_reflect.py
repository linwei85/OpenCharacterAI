"""
Author: Simon Lin (linwei85@gmail.com)

File: daily_reflect.py
Description: Defines the daily reflect action of Character. 
This action means the character will reflect according to the chat hisotry of last day and then update his memory.
"""
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import yaml
from util.config import configuration
from util.common_util import create_openai_client



def reflect_chat_history(my_name:str, my_profile:str, talk_to_name:str, talk_to_profile:str, chat_history, floder_template=False):
    # check the parameter wether is valid
    if not my_name or not my_profile or not talk_to_name or not talk_to_profile:
        return None
    
    # format the template
    with open(f"{floder_template}/gpt4/reflect.yaml", 'r') as stream:
        try:
            template = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    
    template['talkToCharacter']['name'] = talk_to_name
    template['talkToCharacter']['profile'] = talk_to_profile
    template['myCharacter']['name'] = my_name
    template['myCharacter']['profile'] = my_profile
    template['chatHistory'] = chat_history
    prompt = template['prompt'].format(**template)


    # call openapi interface to get result
    openai = create_openai_client()
    response = openai.chat.completions.create(
            model=configuration["model"],
            messages=[
                {"role":"user", "content": prompt}
            ],
            max_tokens=int(configuration["max_tokens"]/10)
        )
    reflect_content = response.choices[0].message.content.strip()
    return reflect_content