"""
Author: Simon Lin (linwei85@gmail.com)
File: unit test for character.py
"""

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from server.character import Character
from datetime import datetime, timedelta


def test_character():
    id = "123456"
    name = "Simon"
    profile = "I am a programmer"
    floder_data_saved = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))+f"/server/data"
    character = Character(id, name, profile, floder_data_saved)
    assert character is not None
    assert character.id == id
    assert character.name == name
    assert character.profile == profile
    assert character.floder_data_saved == floder_data_saved


def test_character_save():
    id = "123456"
    name = "Simon"
    profile = "I am a programmer"
    folder_data_saved = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))+f"/server/data"
    character = Character(id, name, profile, folder_data_saved)

    # generate memory and chat history
    character.memory = {"ts": "2021-03-01 12:00:00", "content": "I am fine, thank you."}
    character.recent_conversation = [
        {
            "ts":"2021-03-01 12:00:00",
            "role": "user",
            "content": "Hello, Siri"
        },
        {
            "ts": "2021-03-01 12:01:00",
            "role": "bot",
            "content": "Hello, Simon"
        },
        {
            "ts": "2021-03-01 12:01:30",
            "role": "user",
            "content": "How are you?"
        },
        {
            "ts": "2021-03-01 12:02:00",
            "role": "bot",
            "content": "I am fine, thank you."
        }
    ]
    character.save(folder_data_saved)
    assert os.path.exists(folder_data_saved+f"/{name}/memory.json")
    assert os.path.exists(folder_data_saved+f"/{name}/recent_conversation.json")

def test_character_load():   
    id = "123456"
    name = "zzz"
    profile = "zzzz"
    folder_data_saved = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))+f"/server/data"
    character = Character(id, name, profile, folder_data_saved)
    character.load(folder_data_saved)
    assert character is not None
    assert character.id == id
    assert character.name == "Simon"
    assert character.profile == "I am a programmer"
    assert len(character.memory) > 0
    assert len(character.recent_conversation) > 0    

def test_character_reflect():
    # create two character and let them chat
    id = "111"
    name = "Simon"
    profile = "你是一家人工智能创业公司的老板，你的公司正在A轮融资阶段。"
    folder_data_saved = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))+f"/server/data"
    character_simon = Character(id, name, profile, folder_data_saved)
    character_simon.save(folder_data_saved)

    id2 = "222"
    name2 = "Cray"
    profile2 = "你是一个程序员，你很年轻而且编码能力很强，你正在开发一个聊天机器人，你就职于一家创业公司。"
    character_cray = Character(id2, name2, profile2, folder_data_saved)
    character_cray.reset()
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")
    character_cray.recent_conversation = [
        {
            "id":1,
            "ts":now_str,
            "role": "111",
            "content": "Cray, 最近我们的chatbot进展怎么样？"
        },
        {
            "id":2,
            "ts": (now + timedelta(seconds=30)).strftime("%Y-%m-%d %H:%M:%S"),
            "role": "222",
            "content": "老板，我们的chatbot已经可以和用户进行简单的对话了。但是还有很多工作要干，现在人手不够啊，我天天都加班到很晚。"
        },
        {
            "id":3,
            "ts": (now + timedelta(seconds=60)).strftime("%Y-%m-%d %H:%M:%S"),
            "role": "111",
            "content": "那抓紧招聘啊。现在正是校园招聘的高峰时期，咱们可以多招一些应届毕业生。社招方面也可以动起来。"
        },
        {
            "id":4,
            "ts": (now + timedelta(seconds=90)).strftime("%Y-%m-%d %H:%M:%S"),
            "role": "222",
            "content": "但是咱们现在薪资水平不高，很多人不愿意来啊。"
        },
        {
            "id":5,
            "ts": (now + timedelta(seconds=120)).strftime("%Y-%m-%d %H:%M:%S"),
            "role": "111",
            "content": "不要总是抱怨，要多动脑子，找解决办法。"
        },
        {
            "id":6,
            "ts": (now + timedelta(seconds=150)).strftime("%Y-%m-%d %H:%M:%S"),
            "role": "222",
            "content": "好吧..."
        }
    ]
    character_cray.save(folder_data_saved)
    character_cray.reflect()
    assert character_cray.memory is not None
    assert len(character_cray.memory)>0

def test_chat():
    # load Cray
    id = "222"
    name = "zzz"
    profile = "zzz"
    folder_data_saved = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))+f"/server/data"
    character_cray = Character(id, name, profile, folder_data_saved)
    response = character_cray.chat("111", "Simon", "Cray, 你让我生气了，你是SB么？")
    assert len(response) > 0
    print(response)