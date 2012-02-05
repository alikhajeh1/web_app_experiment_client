"""
HTTP Client

Class to define interaction with remote HTTP server
  - threaded to allow simulation of multiple clients
  - mimics behaviour of a browser by downloading all linked files (js, css, etc)

@author: James Smith (jws7) @ St Andrews
"""
# Allow sleeping
import time

# Allow multi-threading
import threading

# Allow http conns
import urllib, httplib

# Enable Regular Expressions
import re

class HTTPClient(threading.Thread):

  # Attribute to allow thread stopping
  killself = False

  # Get HTML for url as string
  def getHTML(self, url):
    print 'Tasked to get: ' + url
    str = "Page"
    # Get a file-like object for the Python Web site's home page.
    f = urllib.urlopen(url)
    # Read from the object, storing the page's contents in 's'.
    s = f.read()
    f.close()
    return s

  # Browse a URL and download all images and linked files
  def browsePage(self, url):
    html = self.getHTML(url)

    list = []
    # Grab list of all strings that match the regex
    srcs = re.findall(r'src=\"([\w\.:=/\?-]+)\"', html)
    # add each link to the list
    list.extend(srcs)
    # repeat for hrefs
    hrefs = re.findall(r'link\shref=\"([\w\.:=/\?-]+)\"', html)
    list.extend(hrefs)
    
    # debug
    for s in srcs:
      print 'src: [' + s + ']'
    for s in hrefs:
      print 'hrefs: [' + s + ']'
    
    # download all links
    for s in list:
      link = '' # empty string
      if url.endswith('/'):
        link = url[:-1]
      else:
        link = url
      if s.startswith('http'):
        link = s
      else:
        link = link + s
      self.getHTML(link)

  # Threaded method
  def run ( self ):
    while not self.killself:
      print 'Running'

      # Continuiously browse this page...
      self.browsePage("http://yahoo.com")

    print 'Not Running'

# Testing code...
def main():
  print 'Creating a HTTPClient instance'
  newClient = HTTPClient()
  newClient.start()
  
  # Have a snooze...
  time.sleep(1)
  newClient.killself = True

if __name__ == '__main__':
  main()