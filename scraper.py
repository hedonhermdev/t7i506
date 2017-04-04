# pylint: disable=C0321, C0111, C0301, C0103
# IMPORTS
import json
import re
import urllib.error
import urllib.request

from bs4 import BeautifulSoup, SoupStrainer


class Post(object):
    def __init__(self, id):
        self.id = id
    # MEDIA META
    def post_meta(self):
        try:
            data = self.get_data()['entry_data']['PostPage'][0]["media"]
            return {
                'Media': data['display_src'],
                'Caption': u'%s' % data['caption'],
                'Date': data['date'],
                'Number of likes': data['likes']['count'],
                'Number of comments': data['comments']['count'],
                'Comments': [u"@%s : %s" % (c['user']['username'], c['text']) for c in data['comments']['nodes']],
                'Code' : data['code']
            }
        except KeyError:
            return 0

    def get_data(self):
        while True:
            try:
                url = urllib.request.urlopen(
                    'http://www.instagram.com/p/' + self.id)
                scripts_only = SoupStrainer('script')
                soup = BeautifulSoup(url, 'html.parser',
                                     parse_only=(scripts_only))
                scripts = soup.find_all('script', {'type': 'text/javascript'})
                for sc in scripts:
                    if re.compile('^window._sharedData').search(str(sc.string)):
                        return json.loads(str(sc.string)[21:-1])
            except (urllib.error.URLError, urllib.error.HTTPError, ConnectionError, ) as e:  # IMPROVE!
                print(str(e))
                return json.loads("{}")
            else:
                break

    # Save data in a text file.
    def writetofile(self, fn):
        with open(fn, 'w') as f:
            if self.post_meta():
                meta = self.post_meta()
                f.write("***\n\n")
                # Caption
                f.write('Caption: %s \n' % meta['Caption'])
                # Number of Likes
                f.write('Number of likes: %i \n' % meta['Number of likes'].encode('ascii', 'ignore').decode('windows-1252'))
                #Number of Comments
                f.write('Number of comments: %i \n' % meta['Number of comments'])
                #Comments
                f.write('Comments: ')
                for c in meta['Comments']:
                    s = c.encode('ascii', 'ignore').decode('windows-1252')
                    f.write(s + '\n')

    #Save Media locally
    def save_media(self):
        if self.post_meta():
            urllib.request.urlretrieve(self.post_meta()['Media'], self.post_meta()['Code'])
