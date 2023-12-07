"""
Author: Simon Lin (linwei85@gmail.com)
File: unit test for chat.py
"""

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from server.action import chat
import datetime

def test_chat():
    my_name = "Cray"
    my_profile = "你是一个程序员，你很年轻而且编码能力很强，你正在开发一个聊天机器人，你就职于一家创业公司。"
    my_memory = "Memory Entry: Cray Reflects on Conversation with Simon\n\nDate: 2023-12-07\n\nToday I had an important conversation with my boss, Simon, about the progress and challenges we face with our chatbot project. We discussed extending our team given the increasing workload and my extensive overtime.\n\nAs a programmer, my dedication to coding and advancing our chatbot has been the cornerstone of the project's development so far. While I was able to relay to Simon that we've made significant progress, allowing the bot to engage in basic dialogues with users, my concerns about our human resources were pressing. Our chatbot has potential, but without a stronger team, the product's future is at stake.\n\nSimon, as the head of our AI startup, understands the pressure of our A-round financing stage. He was quick to emphasize action over complaints, directing the focus toward practical solutions, such as hiring more staff. His suggestion to leverage the peak of campus recruitment and also initiate outside recruitment is a reflection of his strategic way of thinking. Simon\u2019s response implied that he sees the problem, but also trusts me to be proactive in seeking ways to resolve it rather than wait for directives. Indeed, our conversation provided me with a sense of urgency as well as an acknowledgment that Simon values my input and trusts my ability to help find solutions.\n\nFrom the chat history, it's evident that Simon is results-oriented and, despite the current low salary levels which make recruiting difficult, he believes in tackling problems head-on and swiftly. While I initially felt apprehensive about the hiring obstacles, Simon's response highlighted the importance of creative solutions in building a talented team, potentially indicating his experience and confidence in overcoming such hurdles in a startup environment.\n\nIn conclusion, today's interaction with Simon left me with a reinforced understanding of his leadership approach and the importance of adopting a problem-solving mindset. As I continue to develop the chatbot, my memory of this exchange will serve as a reminder to actively contribute ideas for team expansion and project scalability. My reflection on this day reinforces my role not just as a developer but as an integral part of a growing company looking to innovate and compete in the AI field."
    my_memory = "no memory"
    talk_to_name = "Simon"
    saying = "Cray, 最近怎么样？上次跟你聊的问题有什么进展么？"
    yestoday = datetime.datetime.now() - datetime.timedelta(days=1)
    yestoday_str = yestoday.strftime("%Y-%m-%d %H:%M:%S")
    '''
    chat_history = [
        {
            "id":1,
            "ts":yestoday_str,
            "role": "Simon",
            "content": "Cray, 最近我们的chatbot进展怎么样？"
        },
        {
            "id":2,
            "ts": (yestoday + datetime.timedelta(seconds=30)).strftime("%Y-%m-%d %H:%M:%S"),
            "role": "Cray",
            "content": "老板，我们的chatbot已经可以和用户进行简单的对话了。但是还有很多工作要干，现在人手不够啊，我天天都加班到很晚。"
        },
        {
            "id":3,
            "ts": (yestoday + datetime.timedelta(seconds=60)).strftime("%Y-%m-%d %H:%M:%S"),
            "role": "Simon",
            "content": "那抓紧招聘啊。现在正是校园招聘的高峰时期，咱们可以多招一些应届毕业生。社招方面也可以动起来。"
        },
        {
            "id":4,
            "ts": (yestoday + datetime.timedelta(seconds=90)).strftime("%Y-%m-%d %H:%M:%S"),
            "role": "Cray",
            "content": "但是咱们现在薪资水平不高，很多人不愿意来啊。"
        },
        {
            "id":5,
            "ts": (yestoday + datetime.timedelta(seconds=120)).strftime("%Y-%m-%d %H:%M:%S"),
            "role": "Simon",
            "content": "不要总是抱怨，要多动脑子，找解决办法。"
        },
        {
            "id":6,
            "ts": (yestoday + datetime.timedelta(seconds=150)).strftime("%Y-%m-%d %H:%M:%S"),
            "role": "Cray",
            "content": "好吧..."
        }
    ]
    '''
    chat_history = []
    

    floder_template = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))+"/server/prompt"
    result = chat.chat(my_name, my_profile, my_memory, talk_to_name, saying, chat_history, floder_template)
    print("-->result:"+result)
    assert result is not None
