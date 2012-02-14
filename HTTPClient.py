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

class HTTPClient(threading.Thread):

  # Attribute to allow thread stopping
  killself = False

  # Flag to signal that an error has occured
  error = False

  # Get HTML for url as string
  def getHTML(self, url):
    print 'Tasked to get: ' + url

    # Create request
    req = urllib2.Request(url)
    
    # Prepare for HTTP Errors
    try:
      # Get a file-like object for the Python Web site's home page.
      response = urllib2.urlopen(req)
    
    # Handle HTTP errors
    except URLError, e:
      if hasattr(e, 'reason'):
        print 'We failed to reach a server.'
        print 'Reason: ', e.reason
        self.error = True
      elif hasattr(e, 'code'):
        print 'The server couldn\'t fulfill the request.'
        print 'Error code: ', e.code
        self.error = True

    else:  # If no errors
      # Read from the object, storing the page's contents in 's'.
      page = response.read()
      response.close()
      return str(page)

  # POST HTTP Request
  def postReq(self, url):
    
    print 'Doing a POST Request to [' + url + ']...'

    # Do auth
    #self.setupAuth(url, "username", "password")

    print 'Parsing data...'
    f = open('/Users/jws7/Movies/BBC iPlayer/repository/cache/bbc_two.mp4', 'r')    
    data = f.read()
    f.close()
    print 'Read ' + str(len(data)) + ' bytes'
    
    values = {}
    values['video[author]'] = 'Python Script'
    values['video[name]'] = 'Python testing...'
    values['video[movie]'] = data
    print 'dict created'
    print values.items()

    print 'making request...'
    # URL encode data and build request
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    
    # Now same as before
    response = urllib2.urlopen(req)
    page = response.read()
    print 'response received:'
    print '[' + page + ']'

  # Browse a URL and download all images and linked files
  def browsePage(self, url):

    # Do auth
    #self.setupAuth(url, "username", "password")

    # Then get HTML pages
    html = self.getHTML(url)

    if self.error != True:

      list = []
      # Grab list of all strings that match the regex
      srcs = re.findall(r'src=\"([\w\.:=/\?-]+)\"', html)
      # add each link to the list
      list.extend(srcs)
      # repeat for hrefs
      hrefs = re.findall(r'link\shref=\"([\w\.:=/\?-]+)\"', html)
      list.extend(hrefs)

      # repeat for hrefs
      vidIDs = re.findall(r'a\shref=\"/videos/([\d\.:=/\?-]+)\"', html)

      # if list len > 0
      if len(vidIDs) > 0:
        # Choose a random ID
        # Import random choice method
        from random import choice
        randomID = choice(vidIDs)
        print 'Random Choice: ' + randomID
      else:
        randomID = -1

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
      
      return randomID
    else:
      print 'Error getting html'

  def post(self, url):

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
    fields.append(('video[description]', str(now)))
    
    # Read file
    print 'Parsing data...'
    f = open('bbc_two.mp4', 'r')    
    data = f.read()
    f.close()
    print 'Read ' + str(len(data)) + ' bytes'
    
    file = ('video[movie]', 'bbc_two.mp4', data)
    files = []
    files.append(file)

    host = url
    selector = {}

    print post_multipart(host, selector, fields, files)

  # Threaded method
  def run ( self ):

    server = "http://138.251.198.21:8080"

    while not self.killself:
      
      print 'Running'

      # Read index page & select a video ID at random
      selected = self.browsePage(server)

      if self.error != True:

        # If there are videos to watch
        if selected >= 0:
          print 'RandomID: ' + selected

          # Download (Watch) that video
          watchStr = server + selected + '/movie'
          print 'Watching: [' + watchStr + ']'
          self.getHTML(watchStr)
        else:
          print 'No uploaded videos to watch'

        # Browse another page
        self.browsePage(server)

        # POST a video
        self.post(server)
      
       # Have a snooze...
      time.sleep(2)

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