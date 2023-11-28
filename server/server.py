import openai
from typing import Union
from fastapi import FastAPI, Form
from pydantic import BaseModel
import textwrap
from fastapi.middleware.cors import CORSMiddleware
from tinydb import TinyDB, Query



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=3600
)

'''
# open source api key
openai.api_key="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"
max_length = 1980
max_key_point_no = 3
max_final_summary_len = 200;
'''

# some gloabl config
character_db_path = "characters.json"
character_db = TinyDB(character_db_path)



# create a background thread to run tasks
# def background(): 
#     while True:
#         print("background")
#         time.sleep(1)
# thread = threading.Thread(target=background)
# thread.start()
# print("thread started")
# print(threading.active_count())
# print(threading.enumerate())
# print(threading.current_thread())                          


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/create_character")
async def create_character(name: str = Form(...), profile: str = Form(...)):
    
    #step1, parse character profile from parameter
    print("-->create_character")
    # check wether the character name exists
    Character = Query()
    results = character_db.search(Character.name == name)
    if len(results) > 0:
        response = {"status":"failed", "message": "character name exists"}
        return {"message": response}
     
    #step2, create a character in the database and return the character id
    character_id = character_db.insert({'name': name, 'profile': profile})
    
    #step3, return the character id
    response = {"status":"success", "character_id": character_id}
    return {"message": response}


@app.post("/chat_character")
async def chat_character(character_id: int = Form(...), user_input: str = Form(...)):
    #step1, get character profile from database
    Character = Query()
    results = character_db.search(Character.id == character_id)
    if len(results) == 0:
        response = {"status":"failed", "message": "character id does not exist"}
        return {"message": response}
    character_profile = results[0]['profile']

    #step2, load character memory from database

    #step3, load history chats from database as context

    
    #step2, chat with the character
    response = {"status":"success", "message": "chat with character"}
    return {"message": response}