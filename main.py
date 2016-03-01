from bs4 import BeautifulSoup as Soup
import requests
from sortedcontainers import SortedSet
import threading,sys

start = 1
end = 15000
num = 300

ss = SortedSet(key=lambda a:-a[0])
ws = SortedSet()

_threads = 7
thread = []

def check_list():
	while True:
		if len(ss) > num:
			del(ss[num:])
		if len(ws) > num:
			del(ws[num:])
		time.sleep(5)

def call(start,end,cnt,ss,ws):
    for page in range(start,end+1,cnt):
        sys.stdout.flush()
        url = "http://codeforces.com/blog/entry/%s" % page
        r = requests.get(url,allow_redirects = False)
        if r.status_code != 200:
            print("Blog Entry %s Not Found" % page)
        else:
            soup = Soup(r.text)
            for comment in soup.find_all("div",{"class":"comment"}):
                name = comment.find("a",{"class":"rated-user"}).text
                rating = int(comment.find("span",{"class","commentRating"}).text)
                _id = int(comment.find("table").attrs["commentid"])
                ws.add((rating,_id,page,name))
                ss.add((rating,_id,page,name))


checker = threading.Thread(target=check_list)

for i in range(_threads):
    thread.append(threading.Thread(target=call,args=(start+i,end,_threads,ss,ws)))
    thread[-1].start()

for t in thread:
    t.join()

print("BEST")
for item in ss:
    print("[user:%s] %s http://codeforces.com/blog/entry/%s#comment-%s" % (item[3],item[0],item[2],item[1]))
print("WORST")
for item in ws:
    print("[user:%s] %s http://codeforces.com/blog/entry/%s#comment-%s" % (item[3],item[0],item[2],item[1]))
