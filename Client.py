import urllib
import httplib
import re

from MyThread import *

"""
HTTP Client class
@author: James Smith (jws7) @ St Andrews
"""

"""
Simple method to return a string of a HTML page
"""
def getHTML(url):
  print 'Tasked to get: ' + url
  str = "Page"
  # Get a file-like object for the Python Web site's home page.
  f = urllib.urlopen(url)
  # Read from the object, storing the page's contents in 's'.
  s = f.read()
  f.close()
  return s

def getReq(url):
  conn = httplib.HTTPConnection(url)
  conn.request("GET", "/index.html")
  r1 = conn.getresponse()
  print r1.status, r1.reason
  data1 = r1.read()
  conn.close()
  return data1

"""
Browse a URL and download all images and linked files

"""
def browsePage(url):
  html = getHTML(url)
  print html

  # Grab list of all strings that match the regex
  srcs = re.findall(r'src=\"([\w\.:=/\?-]+)\"', html)
  for s in srcs:
    print s
    getHTML(url[:-1] + s)
    # now for each download...

  hrefs = re.findall(r'href=\"([\w\.:=/\?-]+)\"', html)
  for s in hrefs:
    print s
    # and download...
  

def main():
  #print getURL("http://www.yahoo.com")
  #print getReq("138.251.198.2/test/")
  browsePage("http://138.251.198.2/test/")
  #doPOST("book.com")
  #for x in xrange ( 2 ):
  #  MyThread().start()

if __name__ == '__main__':
  main()