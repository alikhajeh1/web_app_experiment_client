"""
Client

@author: James Smith (jws7) @ St Andrews
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

# Import HTTPClients
from HTTPClient import *
from HighHTTPClient import *

class Client(threading.Thread):

  kill_received = False # Boolean to allow interruption

  # Thread list - hold the currently running HTTP Clients
  threads = []

  # Override constructor
  def __init__(self):
    # Call superclass constructo
    threading.Thread.__init__(self)
    # A flag to notify the thread that it should finish up and exit
    self.kill_received = False
    # Create list
    self.threads = []

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
      # otherwise take action...
      if result.lower() != 'current':
        print 'Take action'
        # Extract values -> values[0]=id, values[1]=time, values[2]=level
        values = result.split(',')
        level = values[2]
        print 'Moving to level: ' + level

        # kill current threads
        for th in self.threads:
          print 'Killing thread'
          th.killself = True # set flag and threads will kill their self

        # open x number of threads at this level
          # where x is defined by the threadDict
        x = int(threadDict[level])
        print 'Launching ' + str(x) + ' threads'
        for i in xrange(x):
          print 'Creating thread'

          # Choose client level
          if level == 'HIGH':
            print 'Creating High thread'
            newClient = HighHTTPClient()
            
          elif level == 'MEDIUM':
            print 'Creating Medium thread'
            newClient = HTTPClient()

          elif level == 'LOW':
            print 'Creating Low thread'
            newClient = LowHTTPClient()

          # Start thread and add to list
          newClient.start()
          self.threads.append(newClient)

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
     
      # and all HTTP clients
      for th in client.threads:
        th.killself = True # set flag and threads will kill their self

      client.kill_received = True
  
if __name__ == '__main__':
  main()