import time
from multiprocessing.dummy import Pool as ThreadPool

import scraper

start = time.time()
pool = ThreadPool(4)
p = scraper.ProfilePage('fictionalnavy')
arr =[scraper.PostPage(x) for x in p.meta['Recent Posts']]

result = pool.map(scraper.PostPage.writetofile, arr)
pool.close()
end = time.time() - start
print(end)
pool.join()
