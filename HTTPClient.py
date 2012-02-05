"""
HTTP Client

Class to define interaction with remote HTTP server
  - threaded to allow simulation of multiple clients
  - mimics behaviour of a browser by downloading all linked files (js, css, etc)

@author: James Smith
"""
# Allow sleeping
import time

# Allow multi-threading
import threading

class HTTPClient(threading.Thread):

  # Attribute to allow thread stopping
  killself = False

  # Threaded method
  def run ( self ):
    while not self.killself:
      print 'Running'

      """
      Browser behaviour goes here...

      """

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