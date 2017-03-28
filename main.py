#IMPORTS
from bs4 import BeautifulSoup, SoupStrainer
import urllib.request, urllib.error
import tkinter as Tk
import json
#MEDIA META
def post_meta(json_dict):
    data = json_dict['entry_data']['PostPage'][0]["media"] 
    return {
        'Media' : data['display_src'],
        'Caption' :u'%s' % data['caption'],
        'Date' : data['date'],
        'Number of likes' : data['likes'],
        'Number of comments' : data['comments']['count'],
        'Comments' : [u"@%s : %s" % (c['user']['username'], c['text']) for c in data['comments']['nodes']]
    }

def get_data(postid):
    while True:
        try:
            url = urllib.request.urlopen('http://www.instagram.com/p/' + postid)
            scripts_only = SoupStrainer('script')
            soup = BeautifulSoup(url, 'html.parser', parse_only=(scripts_only))
            print()
            return json.loads(str(list(soup.find_all('script'))[4].string)[21:-1])
        except (urllib.error.URLError, urllib.error.HTTPError): #IMPROVE
            return json.loads("{null:null}")
        else:
            break
