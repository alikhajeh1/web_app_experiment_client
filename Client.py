
import threading
import datetime

now = datetime.datetime.now()

"""
Client

Class to define interaction with remote HTTP server
  - threaded to allow simulation of multiple clients
  - mimics behaviour of a browser by downloading all linked files (js, css, etc)

@author: James Smith
"""

class Client(threading.Thread):

  # Threaded method - default calls the behaviour method (which can be overriden)
  def run ( self ):
      self.behaviour()

  def behaviour(self):
    print '[Client:behaviour] in method'
    print "[Client:behaviour] Current date and time:" + str(now)

  def __init__(self):
    threading.Thread.__init__(self) # if overridding constructor - call super
    print '[Client:Constructor:] in method Constructor'

def main():
  #client = Client()         # Call Constructor
  #client.behaviour()         # Call behaviour method
  for x in xrange ( 2 ):
    Client().start()

if __name__ == '__main__':
  main()