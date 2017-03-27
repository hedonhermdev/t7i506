#IMPORTS
from bs4 import BeautifulSoup
import urllib.request, urllib.error
import tkinter as Tk
import json
#MEDIA META
def post_meta(json_dict):
    data = json_dict['entry_data']['PostPage'][0]["media"] 
    return {
        'Media' : data['display_src'],
        'caption' :u'%s' % data['caption'],
        'Date' : data['date'],
        'Number of likes' : data['likes'],
        'Number of comments' : data['comments']['count'],
        'Comments' : [u"@%s : %s" % (c['user']['username'], c['text']) for c in data['comments']['nodes']]
    }

def get_data(postid):
    while True:
        try:
            url = urllib.request.urlopen('http://www.instagram.com/p/' + postid)
            soup = BeautifulSoup(url, 'html.parser')
            return json.loads(str(list(soup.find('body').find_all('script'))[2].string)[21:-1])
        except (urllib.error.URLError, urllib.error.HTTPError) as e: #IMPROVE
            return json.loads("{}")
        else:
            break

