"""
Author: Simon Lin (linwei85@gmail.com)

File: common_util.py
Description: Defines kinds of util functions. 

"""
from tinydb import TinyDB, Query
from openai import OpenAI
from . import config
import httpx


# read profile
def get_character_profile(name: str, db_path: str):
    # Load profile from TinyDB
    profile_db = TinyDB(db_path)
    
    # Define the query
    Character = Query()
    result = profile_db.search(Character.name == name)
    
    if result:
        return result
    return None


def create_openai_client():
    # Create an OpenAI client
    proxy_client = httpx.Client(proxies={"http://": config.configuration["proxy"], "https://": config.configuration["proxy"]})
    openai_client = OpenAI(api_key=config.configuration["api_key"], http_client=proxy_client)
    return openai_client