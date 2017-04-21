import multiprocessing.dummy
import time
import scraper

print("Start")
start = time.time()
pool = multiprocessing.dummy.Pool(16)


def get_date(post):
    post = scraper.PostPage(post)
    try:
        return post.meta['Timestamp']
    except KeyError:
        return "FAILED."
print("Loading webpage...")
p = scraper.ProfilePage('fictionalnavy')
posts = []
try:
    posts = p.meta['Recent Posts']
except KeyError:
    print("Failed...")
a = pool.map(get_date, posts)
print("\n")
print("* * "*11)
print("*   POST_ID   *         TIMESTAMP         *")
for i in range(len(posts)):
    print("* " * 22)
    print("* %s * %s  *"%(posts[i], a[i]))

print("* * "*11)
print("\nTIME TAKEN: %f" %(time.time() - start))
