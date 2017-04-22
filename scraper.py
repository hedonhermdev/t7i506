# pylint: disable=I0011, C0321, C0111, C0301, C0103
# IMPORTS
import json
import os
import re
import urllib.error
import urllib.request
import time
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
        except (urllib.error.URLError, urllib.error.HTTPError, ConnectionError):  # IMPROVE!
            print("Failed to open the webpage.")
            return json.loads("{}")
        else:
            break


def createdir(foldername):  # Make new Folder
    if not os.path.exists(foldername):
        os.makedirs(foldername)

###FOR POSTS###


class PostPage(object):
    def __init__(self, page_id):
        self.page_id = page_id  # POST_page_id
        self.data = get_data('p/' + self.page_id)
        self.meta = self.post_meta()
    # MEDIA meta

    def post_meta(self):
        try:
            data = self.data['entry_data']['PostPage'][0]['graphql']['shortcode_media']
            d = {
                "Username": '@%s' % data['owner']['username'],
                "Media": data['display_url'],
                "Tagged Users": ['@%s' % node['node']['user']['username'] for node in
                                 data["edge_media_to_tagged_user"]['edges']],
                "Caption": u'%s' % data['edge_media_to_caption']['edges'][0]['node']['text'],
                "Timestamp": time.asctime(time.localtime(data['taken_at_timestamp'])),
                "Likes": data['edge_media_preview_like']['count'],
                "Comments": data['edge_media_to_comment']['count']
            }
            return d
        except KeyError:
            return {}

    # Save data in a text file.

    def writetofile(self):
        createdir(self.meta["Username"] + '/' + self.page_id)
        fn = self.page_id + '.txt'
        with open(os.path.join(self.meta["Username"], self.page_id, fn), 'w') as f:
            if self.meta:
                meta = self.post_meta()
                f.write("   ***    \n")
                # Caption
                f.write("Posted on %s" % meta["Timestamp"])
                cap = meta["Caption"].encode('utf-8', 'ignore')
                f.write('Caption: \n --%s \n' % cap)
                # Number of Likes
                f.write('Number of likes: \n --%i \n' %
                        meta["Likes"])
                # Number of Comments
                f.write('Number of comments: \n --%i \n' %
                        meta["Comments"])
                # Comments
                f.write('Comments: \n')
            else:
                f.write("ERROR: No data found for the post(page_id=%s)." %
                        self.page_id)

    # Save Media locally
    def save_media(self, fn=None):
        createdir(self.meta["Username"] + '/' + self.page_id)
        if fn == None:
            fn = self.page_id + '.jpg'
        if self.meta:
            urllib.request.urlretrieve(
                self.meta['Media'], os.path.join(self.meta['User'], self.page_id, fn))
        else:
            print('ERROR: No media found for the given post(page_id=%s).' %
                  self.page_id)


###FOR PROFILES###


class ProfilePage(object):
    def __init__(self, page_id):
        self.page_id = page_id
        self.data = get_data(self.page_id)
        self.meta = self.profile_meta()

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
            return {}

    def writetofile(self):
        createdir(self.page_id)
        fn = self.page_id + '.txt'
        with open(os.path.join(self.page_id, fn), 'w') as f:
            f.write("   ****    \n")
            f.write("Full Name:\n%s\n\n" % self.meta['User']['Full Name'])
            f.write("Biography:\n%s\n\n" % str(self.meta['User']['Biography'].encode('utf-8', 'ignore')))
            f.write("Website:\n%s\n\n" % self.meta['User']['Website'])
            f.write("FaceBook:\n%s\n\n" % self.meta['User']['FaceBook Page'])
            f.write("Followers:\n%i\n\n" % self.meta['User']['Followers'])
            f.write("Following:\n%i\n\n" % self.meta['User']['Follows'])
    def get_profile_picture(self):
        createdir(self.page_id)
        urllib.request.urlretrieve(self.meta['User']['Profile Picture'], os.path.join(self.page_id, 'profilepicture.jpg'))

    def get_recent_posts(self, n=12):
        post_arr = self.meta['Recent Posts'][:n]
        for post_id in post_arr:
            print("Loading post '%s' ..." % post_id)
            try:
                post = PostPage(post_id)
                post.save_media()
                post.writetofile()
            except KeyError:
                print("Failed. \n")
            else:
                print("Loaded.")
    def get_everything(self):
        try:
            self.writetofile()
            self.get_profile_picture()
            self.get_profile_picture()
            self.get_recent_posts()
        except (KeyError, UnicodeError): # FIXME
            print("UNKNOWN ERROR")
