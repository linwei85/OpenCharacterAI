"""
Author: Simon Lin (linwei85@gmail.com)
File: unit test for daily_reflect.py
"""

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from server.action import daily_reflect

def test_reflect_chat_history():
    my_name = "Simon"
    my_profile = "I am a programmer"
    talk_to_name = "Siri"
    talk_to_profile = "I am a chatbot"
    chat_history = [
        {
            "role": "user",
            "content": "Hello, Siri"
        },
        {
            "role": "bot",
            "content": "Hello, Simon"
        },
        {
            "role": "user",
            "content": "How are you?"
        },
        {
            "role": "bot",
            "content": "I am fine, thank you."
        }
    ]
    floder_template = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))+"/server/prompt"
    result = daily_reflect.reflect_chat_history(my_name, my_profile, talk_to_name, talk_to_profile, chat_history, floder_template)
    print("-->result:"+result)
    assert result is not None
