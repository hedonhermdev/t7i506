#IMPORTS
from bs4 import BeautifulSoup as soup
import urllib.request
import tkinter as Tk
import json

#MEDIA META
def post_meta(json_script):
    data = json.loads(json_script)['entry_data']['PostPage'][0]["media"]
    return {
        'media' : data['display_src'],
        'caption' : data['caption'],
        'date' : data['date'],
        'num_of_likes' : data['likes'],
        'num_of_comments' : data['comments']['count'],
        'comments' : [(c['user']['username'], c['text']) for c in data['comments']['nodes']]
    }
