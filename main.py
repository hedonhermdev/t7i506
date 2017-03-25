#IMPORTS
import re
from bs4 import BeautifulSoup
import urllib.request, urllib.error
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

def get_data(postid):
    while True:
        try:
            url = urllib.request.urlopen('http://www.instagram.com/p/' + postid) 
            soup = BeautifulSoup(url, 'html.parser')
            script = list(soup.body.find_all('script'))[2]
            return str(script.string)[21: -1]
        except (urllib.error.URLError, urllib.error.HTTPError) as e: #IMPROVE
            return "There was an error. Please try again. Error code : %i" % e.code
        else:
            break
print(get_data('BQ0gGg2jr1W'))