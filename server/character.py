"""
Author: Simon Lin (linwei85@gmail.com)

File: character.py
Description: Defines the Character class that represent a specific person. 

"""
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import datetime
from tinydb import TinyDB, Query
from util.common_util import get_character
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

        # Create the folder if it doesn't exist
        character_path = floder_data_saved+f"/{self.name}"
        if not os.path.exists(character_path):
            os.makedirs(character_path)

        self.load(floder_data_saved)
        
        
    def save(self, save_folder):
        """
        Save character's current state (i.e., memory). 

        INPUT: 
        save_folder: The folder where we wil be saving our character's state. 
        OUTPUT: 
        None
        """
        # save character basic information to tiny db
        character_db = TinyDB(f"{save_folder}/characters.json")
        character = Query()
        if not character_db.contains(character.id == self.id):
            character_db.insert({'id': self.id, 'name': self.name, 'profile': self.profile})
        else:
            character_db.update({'name': self.name, 'profile': self.profile}, character.id == self.id)
        character_db.close()

        # Create the folder if it doesn't exist
        character_path = f"{save_folder}/{self.name}"
        if not os.path.exists(character_path):
            os.makedirs(character_path)
        
        # save memory to tiny db
        if self.memory:
            memory_db = TinyDB(f"{character_path}/memory.json")
            item = Query()
            if not hasattr(self.memory, 'doc_id'):
                memory_db.insert(self.memory)              
            memory_db.close()
        
        # save recent conversation to tiny db
        if self.recent_conversation:
            conversation_db = TinyDB(f"{character_path}/recent_conversation.json")
            item = Query()
            for conversation in self.recent_conversation:
                if not hasattr(conversation, 'doc_id'):
                    conversation_db.insert(conversation)
            conversation_db.close()


    def load(self, load_folder):
        """
        Load character's state (i.e., memory). 

        INPUT: 
        load_folder: The folder where we wil be loading our character's state. 
        OUTPUT: 
        None
        """
        # load character basic information from tiny db
        character_db = TinyDB(f"{load_folder}/characters.json")
        character = Query()
        results = character_db.search(character.id == self.id)
        if len(results) > 0:
            self.name = results[0]['name']
            self.profile = results[0]['profile']
        character_db.close()

        # load memory from tiny db
        memory_db = TinyDB(f"{load_folder}/{self.name}/memory.json")
        # get the latest memory from memory_db
        if len(memory_db) > 0:
            results = memory_db.all()
            sorted_results = sorted(results, key=lambda x: x['ts'], reverse=True)
            self.memory = sorted_results[0]
        memory_db.close()

        # load recent conversation from tiny db
        conversation_db = TinyDB(f"{load_folder}/{self.name}/recent_conversation.json")
        # get the latest 50 conversation from conversation_db
        if len(conversation_db) >= 0:
            results = conversation_db.all()
            sorted_results = sorted(results, key=lambda x: x['ts'], reverse=True)
            self.recent_conversation = sorted_results[:50]
        conversation_db.close()

    def reset(self):
        """
        remove the character's memory and recent chat history from db and reset the variables. 
        """
        character_path = self.floder_data_saved+f"/{self.name}"
        memory_db = TinyDB(f"{character_path}/memory.json")
        memory_db.truncate()
        memory_db.close()

        conversation_db = TinyDB(f"{character_path}/recent_conversation.json")
        conversation_db.truncate()
        conversation_db.close()

        self.memory = None
        self.recent_conversation = None

    def update(self, name: str, profile: str): 
        """
        Update character's basic information. 

        INPUT: 
        name: The character's name. 
        profile: The character's profile. 
        OUTPUT: 
        None
        """
        self.name = name
        self.profile = profile
        character_db = TinyDB(f"{self.floder_data_saved}/characters.json")
        character = Query()
        character_db.update({'name': self.name, 'profile': self.profile}, character.id == self.id)
        character_db.close()
    
    def reflect(self):
        """
        The character will review daily chat history, reflect on some key information and update his or her memory.
        """
        # load daily conversation from tiny db
        conversation_db = TinyDB(f"{self.floder_data_saved}/{self.name}/recent_conversation.json")
        lastday = datetime.date.today() - datetime.timedelta(days=1)
        # get the conversated history of lastday
        lastday_conversation = conversation_db.search(Query().ts >= lastday.strftime("%Y-%m-%d"))
        if len(lastday_conversation) == 0:
            return
        sorted_results = sorted(lastday_conversation, key=lambda x: x['ts'], reverse=True)
        sorted_results = sorted_results[:100]

        # reflect on the conversation
        talk_to_character_id = ''
        for record in sorted_results:
            if record['role'] != self.id:
                talk_to_character_id = record['role']
                break

        talk_to_character = get_character(talk_to_character_id, f"{self.floder_data_saved}/characters.json")
        if talk_to_character is None:
            return
        
        #replace the role name
        for record in sorted_results:
            if record['role'] == self.id:
                record['role'] = self.name
            else:
                record['role'] = talk_to_character['name']

        parent_path = os.path.dirname(self.floder_data_saved)
        refresh_memory = reflect_chat_history(self.name, self.profile, talk_to_character["name"], talk_to_character["profile"], 
                                              sorted_results, f"{parent_path}/prompt")

        if refresh_memory:
            # update memory
            self.memory = {'ts': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'content': refresh_memory}
            self.save(self.floder_data_saved)


    def retrieve(self):
        """
        Retrieve the character's chat history. 
        """
        pass

    def chat(self):
        """
        Chat with the character. 
        """
