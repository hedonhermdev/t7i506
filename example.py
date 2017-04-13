import time
import threading
import queue
import scraper

p = scraper.ProfilePage('9gag')

[scraper.PostPage(x) for x in p.meta["Recent Posts"]]


