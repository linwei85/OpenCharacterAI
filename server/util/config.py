"""
Author: Simon Lin (linwei85@gmail.com)

File: config.py
Description: Global configuration of the Server 

"""
import os
import sys
import yaml
import openai

config_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
configuration = None
if(configuration is None):
    with open(f"{config_file_path}/config.yaml", 'r') as stream:
        configuration = yaml.safe_load(stream)