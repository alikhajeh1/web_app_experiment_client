"""
Client

Class to define interaction with remote HTTP server
  - threaded to allow simulation of multiple clients
  - mimics behaviour of a browser by downloading all linked files (js, css, etc)

@author: James Smith
"""

# Allow sleeping
import time

# Allow multi-threading
import threading

# Time/Date object
import datetime
now = datetime.datetime.now()

# Import ConfigMonitor attributes
from ConfigMonitor import *

# Import ConfigMonitor attributes
from HistoryMonitor import *

class Client(threading.Thread):

  kill_received = False # Boolean to allow interruption

  # Override constructo
  def __init__(self):
    # Call superclass constructo
    threading.Thread.__init__(self)
    # A flag to notify the thread that it should finish up and exit
    self.kill_received = False

  # Threaded method - default calls the behaviour method (which can be overriden)
  def run ( self ):
      self.behaviour()

  def behaviour(self):
    # Loop until interrupted by Ctrl + C
    while not self.kill_received:
      print '[Client:behaviour] in method'
      print "[Client:behaviour] Current date and time:" + str(now)

      # Now parse the Config File and show the current thread level counts
      parseConfig()
      print "[Client:behaviour] High Thread count: " + threadDict['HIGH']
      print "[Client:behaviour] Medium Thread count: " + threadDict['MEDIUM']
      print "[Client:behaviour] Low Thread count: " + threadDict['LOW']

      # Now check history file for any recent timestamps (past hour)
      result = checkHistory()

      # If that result is the "current" signal - stay at the current level
      if result != 'current':
        print 'Take action'
        


      # Have a snooze...
      time.sleep(5)

  def __init__(self):
    threading.Thread.__init__(self) # if overridding constructor - call super
    print '[Client:Constructor:] in method Constructor'

# Create a Client class and start it running
def main():
  client = Client()         # Call Constructor
  client.start()            # Start thread
  
  # Enable keyboard interrupts
  while not client.kill_received:
    try:
      client.join(1)
    except KeyboardInterrupt:
     print "Ctrl-c received! Sending kill to threads..."
     client.kill_received = True 
  
if __name__ == '__main__':
  main()