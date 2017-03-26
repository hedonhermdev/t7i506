#IMPORTS
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
            soup = BeautifulSoup(url, 'lxml')
            return json.loads(str(list(soup.find('body').find_all('script'))[2].string)[21:-1])
        except (urllib.error.URLError, urllib.error.HTTPError) as e: #IMPROVE
            return json.loads("{}")
        else:
            break

