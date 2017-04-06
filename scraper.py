# pylint: disable=I0011, C0321, C0111, C0301, C0103
# IMPORTS
import json
import os
import re
import urllib.error
import urllib.request

from bs4 import BeautifulSoup, SoupStrainer


class Post(object):
    def __init__(self, id):
        self.id = id  # POST_ID
    # MEDIA meta

    def post_meta(self):
        try:
            data = self.get_data()['entry_data']['PostPage'][0]["media"]
            return {
                'Media': data['display_src'],
                'Caption': u'%s' % data['caption'],
                'Date': data['date'],
                'Number of likes': data['likes']['count'],
                'Number of comments': data['comments']['count'],
                'Comments': [u"@%s :: %s" % (c['user']['username'], c['text']) for c in data['comments']['nodes']],
                'Code': data['code']
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

    def createdir(self):
        if not os.path.exists(self.id):
            os.makedirs(self.id)
    # Save data in a text file.

    def writetofile(self):
        self.createdir()
        fn = self.id + '.txt'
        with open(os.path.join(self.id, fn), 'w') as f:
            if self.post_meta():
                meta = self.post_meta()
                f.write("***\n\n")
                # Caption
                f.write('Caption: \n --%s \n' % meta['Caption'])
                # Number of Likes
                f.write('Number of likes: \n --%i \n' %
                        meta['Number of likes'])
                # Number of Comments
                f.write('Number of comments: \n --%i \n' %
                        meta['Number of comments'])
                # Comments
                f.write('Comments: \n')
                for c in meta['Comments']:
                    s = c.encode('ascii', 'ignore').decode('windows-1252')
                    f.write("   --" + s + '\n')
            else:
                f.write("ERROR: No data found for the post(ID=%s)." % self.id)

    # Save Media locally
    def save_media(self):
        print("Loading...")
        self.createdir()
        fn = self.id + '.jpg'
        if self.post_meta():
            urllib.request.urlretrieve(
                self.post_meta()['Media'], os.path.join(self.id, fn))
            print("Done.")
            print("\nMedia saved. \n")
        else:
            print('ERROR: No media found for the given post(ID=%s).' % self.id)
