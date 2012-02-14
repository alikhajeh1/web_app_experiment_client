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
  MAX_THREAD_COUNT = 1  # Maxium number of threads to run

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

  def killThreads(self):
    # kill current threads
    for th in self.threads:
      print 'Killing thread'
      th.killself = True # set flag and threads will kill their self

  """
  Method to find the global Maximum number of threads that we can run

  Works similar to TCP slow start -> Builds to a Maximum number by doubling thread count each time
  If errors occur
    Set the maxmum limit as the previous level
  """
  def slowStart(self):
    print 'slowStart'

    while not self.kill_received:

      # Create Threads to fill MAX_THREAD_COUNT
      for i in xrange(self.MAX_THREAD_COUNT - len(self.threads)):
        print 'Creating thread'
        th = HTTPClient()

        # Start thread and add to list
        th.start()
        self.threads.append(th)

      # Snooze for 5 secs before evaluating
      time.sleep(5)
    
      # Loop through all threads, checking for errors
      print 'Evaluating threads'
      for th in self.threads:
        
        print 'Thread reporting error: ' + str(th.error)

        # If error, then kill all threads
        if th.error == True:
          self.MAX_THREAD_COUNT = len(self.threads) / 2 # Previous level
          print 'Maximum threads: ' + str(self.MAX_THREAD_COUNT)
          self.killThreads()

          print 'selfStart finished. MaxThreads: ' + str(self.MAX_THREAD_COUNT)

          # Can never be less than one thread, so check
          if self.MAX_THREAD_COUNT < 1:
            print 'Setting thread count to 1'
            self.MAX_THREAD_COUNT = 1
          return
        
        else: # No errors
          # Double MAX_THREAD_COUNT
          self.MAX_THREAD_COUNT = self.MAX_THREAD_COUNT * 2
      
  def behaviour(self):

    self.slowStart()
    print 'MAX_THREAD_COUNT: ' + str(self.MAX_THREAD_COUNT)

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
        
        # Kill current threads
        self.killThreads()        

        # open x number of threads at this level
        # where x is defined by the threadDict level
        x = float(threadDict[level])
        
        # Convert level to percentage
        x = x / 100
        # Multiply percentage by MAX_THREAD_COUNT
        threads = int(self.MAX_THREAD_COUNT * x)
        # catch zero threads
        if threads == 0:
          threads = 1

        print 'Launching ' + str(threads) + ' threads'
        return

        for i in xrange(threads):
          print 'Creating thread'
          newClient = HTTPClient()

          # Start thread and add to list
          newClient.start()
          self.threads.append(newClient)
      
      else:
        print 'No changes to be made'

      # Have a snooze...
      time.sleep(60)

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