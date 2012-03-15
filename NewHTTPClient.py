"""
New, Simpler, HTTP Client

Class to define interaction with remote HTTP server
  - no threading - runs in execution thread for maximum responsivness
  - mimics behaviour of a browser by downloading all linked files (js, css, etc)

@author: James Smith (jws7) @ St Andrews
"""
# Allow sleeping
import time

# Time/Date object
import datetime

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

class HTTPClient():

  # Request counter
  getReqs = 0
  postReqs = 0

  # Bandwidth counters
  rxBytes = 0
  txBytes = 0

  # Get HTML for url as string
  def httpGET(self, url):

    print 'GETting ' + url

    # Increment request counter
    self.getReqs += 1

    # Create request
    req = urllib2.Request(url)
    
    response = None
    page = None
    # Prepare for HTTP Errors
    try:
      # Get a file-like object for the URL requested.
      response = urllib2.urlopen(req)
      page = response.read()

      # Increment byte counter
      self.rxBytes += len(page)
    
    # Handle HTTP errors
    except URLError, e:
      if hasattr(e, 'reason'):
        print '[HTTPClient:httpGET] We failed to reach a server.'
        print '[HTTPClient:httpGET] Reason: ', e.reason
      elif hasattr(e, 'code'):
        print '[HTTPClient:httpGET] The server couldn\'t fulfill the request.'
        print '[HTTPClient:httpGET] Error code: ', e.code
        print '[HTTPClient:httpGET] Attempted to access ' + url
        self.error = True
    finally:
      if response is not None:
        response.close() # close connection to URL
    return page # return file obj

  # Browse a URL and download all images and linked files
  # Simulate Browser behaviour
  def browsePage(self, url):

    # GET URL Page
    html = str(self.httpGET(url)) # convert to string for parsing
    #print html

    # Now download all attached links (css, javascript, etc)    
    list = []
    # Grab list of all strings that match the regex
    srcs = re.findall(r'src=\"([\w\.:=/\?-]+)\"', html)
    # add each link to the list
    list.extend(srcs)
    # repeat for hrefs
    hrefs = re.findall(r'link\shref=\"([\w\.:=/\?-]+)\"', html)
    list.extend(hrefs)
    print 'Found ' + str(len(list)) + ' links to download'

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
        link = url + s
      self.httpGET(link)
  
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
    fields.append(('video[name]', 'NewHTTPClient uploading ELL_PART_5_768k.wmv'))
    fields.append(('video[author]', 'NewHTTPClient'))

    # Get current timestamp - set as description
    now = datetime.datetime.now()
    fields.append(('video[description] Upload occured at ', str(now)))
    
    # Read file
    f = open('ELL_PART_5_768k.wmv', 'r')    
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

    # Define list of server to access
    servers = ['http://138.251.198.24:8080',  'http://138.251.198.24:8081', 'http://138.251.198.24:8082', 'http://138.251.198.24:8083', 'http://138.251.198.24:8084', 'http://138.251.198.24:8085', 'http://138.251.198.24:8086', 'http://138.251.198.24:8087']

    # Comment this line out to run on remote servers
    #servers = ['http://jws7-laptop/~jws7/simple%20jws7/']

    while True:

      now = datetime.datetime.now()
      print "[Client:run] Current date and time:" + str(now)

      # Choose a server
      server = choice(servers)

      # POST a video
      self.httpPOST(server)
      print 'Finished posting a video'
    
      # Browse a HTML page - returns a video ID if present
      selected = self.browsePage(server)
      print 'Finished browsing a page'
      

      # Update on current status
      print 'Recieved ' + str(self.rxBytes) + ' Bytes over ' + str(self.getReqs) + ' GET Reqs'
      print 'Transmitted ' + str(self.txBytes) + ' Bytes over ' + str(self.postReqs) + ' POST Reqs'
      # reset stats
      self.rxBytes = 0
      self.txBytes = 0
      self.getReqs = 0
      self.postReqs = 0

       # Have a snooze...
      time.sleep(5) # 5 secs between iterations
      
# Testing code...
def main():
  print 'Creating a HTTPClient instance'
  newClient = HTTPClient()
  newClient.run()
  
if __name__ == '__main__':
  main()