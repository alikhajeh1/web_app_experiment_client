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
import urllib2, httplib
from urllib2 import Request, urlopen, URLError

# Enable Regular Expressions
import re

class HTTPClient(threading.Thread):

  # Attribute to allow thread stopping
  killself = False

  def getHTMLWithAuth(self, url, username, password):
    print 'Tasked to get: ' + url + " using Auth"

    # Set up the Auth parameters
    # create a password manager
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()

    # Add the username and password.
    # If we knew the realm, we could use it instead of None.
    top_level_url = url
    password_mgr.add_password(None, top_level_url, username, password)
    handler = urllib2.HTTPBasicAuthHandler(password_mgr)

    # create "opener" (OpenerDirector instance)
    opener = urllib2.build_opener(handler)

    # use the opener to fetch a URL
    opener.open(url)

    # Install the opener.
    # Now all calls to urllib2.urlopen use our opener.
    urllib2.install_opener(opener)

    # Make Normal URL Request now
    return self.getHTML(url)

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
      elif hasattr(e, 'code'):
        print 'The server couldn\'t fulfill the request.'
        print 'Error code: ', e.code
    
    else:  # If no errors
      # Read from the object, storing the page's contents in 's'.
      page = response.read()
      response.close()
      return str(page)



  # Browse a URL and download all images and linked files
  def browsePage(self, url):
    html = self.getHTMLWithAuth(url, "username", "password")

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
      self.browsePage("http://138.251.198.23/videos")
     
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