# pylint: disable=I0011, C0321, C0111, C0301, C0103
# IMPORTS
import json
import os
import re
import urllib.error
import urllib.request

from bs4 import BeautifulSoup, SoupStrainer


def get_data(page_id):
    while True:
        try:
            url = urllib.request.urlopen(
                'http://www.instagram.com/' + page_id)
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

def createdir(foldername):
    if not os.path.exists(foldername):
        os.makedirs(foldername)

###FOR POSTS###


class PostPage(object):
    def __init__(self, page_id):
        self.page_id = '/p' + page_id  # POST_page_id
        self.data = get_data(page_id)
    # MEDIA meta

    def post_meta(self):
        try:
            data = self.data['entry_data']['PostPage'][0]["media"]
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

    # Save data in a text file.

    def writetofile(self):
        createdir(self.page_id)
        fn = self.page_id + '.txt'
        with open(os.path.join(self.page_id, fn), 'w') as f:
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
                f.write("ERROR: No data found for the post(page_id=%s)." %
                        self.page_id)

    # Save Media locally
    def save_media(self):
        print("Loading...")
        createdir(self.page_id)
        fn = self.page_id + '.jpg'
        if self.post_meta():
            urllib.request.urlretrieve(
                self.post_meta()['Media'], os.path.join(self.page_id, fn))
            print("Done.")
            print("\nMedia saved. \n")
        else:
            print('ERROR: No media found for the given post(page_id=%s).' %
                  self.page_id)


###FOR PROFILES###


class ProfilePage(object):
    def __init__(self, page_id):
        self.page_id = page_id
        self.data = get_data(self.page_id)

    def profile_meta(self):
        try:
            data = self.data['entry_data']['ProfilePage'][0]['user']
            return {
                'User': {
                    'Full Name': data['full_name'],
                    'Profile Picture': data['profile_pic_url_hd'],
                    'Biography': data['biography'],
                    'Follows': data['follows']['count'],
                    'Followers': data['followed_by']['count'],
                    'Website': data['external_url'],
                    'FaceBook Page': data['connected_fb_page']
                },
                'Recent Posts': [post['code'] for post in data['media']['nodes']]
            }
        except KeyError:
            return 0
            