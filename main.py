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
                'Comments': [u"@%s : %s" % (c['user']['username'], c['text']) for c in data['comments']['nodes']]
            }
        except KeyError:
            print("Unexpected error in parsing JSON. Try again. ")
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
            except (urllib.error.URLError, urllib.error.HTTPError, ConnectionError) as e:  # IMPROVE!
                print(str(e))
                return json.loads("{}")
            else:
                break


# MAIN
print("##########")
print("Enter the IDs of the posts seperated by commas. Press Enter when done.")
posts = [id.strip() for id in input().split(',')]
for i in posts:
    print("#####")
    print(i)
    i = Post(i)
    meta = i.post_meta()
    print(meta)
print("##########")
