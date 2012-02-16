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
import urllib2, httplib, urllib
from urllib2 import Request, urlopen, URLError

# Enable Regular Expressions
import re

# Import POST Multipart
from multipart import post_multipart as post_multipart

# Time/Date object
import datetime

# Allow a random list choice
from random import choice

class HTTPClient(threading.Thread):

  # Attribute to allow thread stopping
  killself = False

  # Flag to signal that an error has occured
  error = False

  # Request counter
  getReqs = 0
  postReqs = 0

  # Bandwidth counters
  rxBytes = 0
  txBytes = 0

  # Get HTML for url as string
  def httpGET(self, url):

    # Increment request counter
    self.getReqs += 1

    # Create request
    req = urllib2.Request(url)
    
    response = None
    page = None
    # Prepare for HTTP Errors
    try:
      # Get a file-like object for the Python Web site's home page.
      response = urllib2.urlopen(req)
      page = response.read()
      self.rxBytes += len(page)
    
    # Handle HTTP errors
    except URLError, e:
      if hasattr(e, 'reason'):
        print '[HTTPClient:getHTML] We failed to reach a server.'
        print '[HTTPClient:getHTML] Reason: ', e.reason
        self.error = True
      elif hasattr(e, 'code'):
        print '[HTTPClient:getHTML] The server couldn\'t fulfill the request.'
        print '[HTTPClient:getHTML] Error code: ', e.code
        self.error = True
    finally:
      if response is not None:
        response.close()
    return str(page)

  # Browse a URL and download all images and linked files
  def browsePage(self, url):

    # Then get HTML pages
    html = self.httpGET(url)

    if self.error != True:

      list = []
      # Grab list of all strings that match the regex
      srcs = re.findall(r'src=\"([\w\.:=/\?-]+)\"', html)
      # add each link to the list
      list.extend(srcs)
      # repeat for hrefs
      hrefs = re.findall(r'link\shref=\"([\w\.:=/\?-]+)\"', html)
      list.extend(hrefs)

      # repeat for video links
      vidIDs = re.findall(r'a\shref=\"/videos/([\d\.:=/\?-]+)\"', html)

      # if video list len > 0
      if len(vidIDs) > 0:
        # Choose a random ID
        randomID = choice(vidIDs)
        #print 'Random Choice: ' + randomID
      else:
        randomID = -1
      
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
        self.httpGET(link)
      
      return randomID

  def httpPOST(self, url):
    # Increment request counter
    self.postReqs += 1

    """
    Post fields and files to an http host as multipart/form-data.
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return the server's response page.
    """
    now = datetime.datetime.now() # Current timestamp

    fields = []
    fields.append(('video[name]', 'PythonTest'))
    fields.append(('video[author]', 'Python Script'))

    # Get current timestamp - set as description
    now = datetime.datetime.now()
    fields.append(('video[description]', str(now)))
    
    # Read file
    f = open('bbc_two.mp4', 'r')    
    data = f.read()
    f.close()
    self.txBytes += len(data)
    
    file = ('video[movie]', 'ELL_PART_5_768k.wmv', data)
    files = []
    files.append(file)

    host = url
    selector = {}

    post_multipart(host, selector, fields, files)

  # Threaded method
  def run ( self ):

    # Define server to access
    server = "http://138.251.198.21:8080"

    while not self.killself:
    
      self.httpPOST(server)
      # Browse a HTML page - returns a video ID if present
      #selected = self.browsePage(server)

      # If No errors in our initial browse (the server is UP)
      if self.error != True:

        # If there are videos to watch
        if selected >= 0:

          # Download (Watch) that video
          #watchStr = server + '/videos/' + selected + '/movie?style=ogg'
          #print 'Watching: [' + watchStr + ']'
          #self.httpGET(watchStr)
        else:
          print 'No uploaded videos to watch'

        # Browse another page
        #self.browsePage(server)

        # POST a video
        #self.httpPOST(server)
      
       # Have a snooze...
      time.sleep(30) # 5 secs between iterations
      self.error = False

# Testing code...
def main():
  print 'Creating a HTTPClient instance'
  newClient = HTTPClient()
  newClient.start()
  
  # Limit to 1 iteration
  time.sleep(1)
  newClient.killself = True 

if __name__ == '__main__':
  main()