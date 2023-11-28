"""
Author: Simon Lin (linwei85@gmail.com)

File: character.py
Description: Defines the Character class that represent a specific person. 

"""
import datetime
from tinydb import TinyDB, Query
from util.common_util import get_character_profile
from action.daily_reflect import reflect_chat_history


class Character:
    """
    Character class represents a specific person. 
    """
    def __init__(self, id:str, name: str, profile: str, floder_data_saved=False):
        """
        Constructor
        """
        self.id = id
        self.name = name
        self.profile = profile
        self.floder_data_saved = floder_data_saved
        # load memory from tiny db
        self.memory = None
        memory_db = TinyDB(f"{floder_data_saved}/memory.json")
        # get the latest memory from memory_db
        if len(memory_db) > 0:
            self.memory = memory_db.all()[-1]

        # load recent conversation from tiny db
        self.recent_conversation = None
        conversation_db = TinyDB(f"{floder_data_saved}/recent_conversation.json")
        # get the latest 50 conversation from conversation_db
        if len(conversation_db) >= 0:
            self.recent_conversation = conversation_db.all()[-50:]
        
        
    def save(self, save_folder):
        """
        Save character's current state (i.e., memory). 

        INPUT: 
        save_folder: The folder where we wil be saving our character's state. 
        OUTPUT: 
        None
        """
        # save memory to tiny db
        if not self.memory:
            memory_db = TinyDB(f"{save_folder}/memory.json")
            self.memory.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            memory_db.insert(self.memory)
        
        # save recent conversation to tiny db
        if not self.recent_conversation:
            conversation_db = TinyDB(f"{save_folder}/recent_conversation.json")
            item = Query()
            for conversation in self.recent_conversation:
                if not conversation_db.contains(item.id == conversation.id):
                    conversation_db.insert(conversation)
    
    def reflect(self):
        """
        The character will review daily chat history, reflect on some key information and update his or her memory.
        """
        # load daily conversation from tiny db
        conversation_db = TinyDB(f"{self.floder_data_saved}/daily_conversation.json")
        lastday = datetime.date.today() - datetime.timedelta(days=1)
        # get the conversated history of lastday
        lastday_conversation = conversation_db.search(Query().timestamp >= lastday.strftime("%Y-%m-%d"))
        if len(lastday_conversation) == 0:
            return
        sorted_results = sorted(lastday_conversation, key=lambda x: x['timestamp'], reverse=True)
        lastday_conversation_100 = sorted_results[:100]


        # reflect on the conversation
        talk_to_character_name = lastday_conversation_100[0].name
        talk_to_character_profile = get_character_profile(talk_to_character_name, f"{self.floder_data_saved}/characters.json")
        reflect_chat_history(self.name, self.profile, talk_to_character_name, talk_to_character_profile, "./prompt")


    def retrieve(self):
        """
        Retrieve the character's chat history. 
        """
        pass

    def chat(self):
        """
        Chat with the character. 
        """
