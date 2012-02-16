"""
Client

@author: James Smith (jws7) @ St Andrews
"""
# Allow command line args
import sys

# Allow sleeping
import time

# Allow multi-threading
import threading

# Time/Date object
import datetime

# Import HTTPClients
from HTTPClient import *

class SimpleClient(threading.Thread):

  kill_received = False # Boolean to allow interruption
  MAX_THREAD_COUNT = 1  # Maxium number of threads to run

  # Thread list - hold the currently running HTTP Clients
  threads = []

  # Override constructor
  def __init__(self, number):
    # Call superclass constructo
    threading.Thread.__init__(self)
    print '[Client:Constructor:] in method Constructor'

    # Set Thread number
    self.MAX_THREAD_COUNT = number
    # A flag to notify the thread that it should finish up and exit
    self.kill_received = False
    # Create list
    self.threads = []

  # Method to kill all currently running threads
  def killThreads(self):
    # kill current threads
    print 'Killing all active threads'
    for th in self.threads:
      th.killself = True # set flag and threads will kill their self
      
  # Threaded method - default calls the behaviour method (which can be overriden)
  def run ( self ):
    # Print the maximum thread count
    print 'MAX_THREAD_COUNT: ' + str(self.MAX_THREAD_COUNT)

    # Create threads
    number = self.MAX_THREAD_COUNT - len(self.threads)
    print 'Creating ' + str(number) + ' active threads'
    for i in xrange(number):
        
      # Start thread and add to list
      th = HTTPClient()
      th.start()
      self.threads.append(th)
        
    # Loop until interrupted by Ctrl + C
    while not self.kill_received:

      # Print current date and time and current thread count
      now = datetime.datetime.now()
      print "[Client:run] Current date and time:" + str(now)
      print "[Client:run] Current concurrent thread count:" + str(len(self.threads))  

      # Get & reset counters
      getsPerMinute = 0
      postsPerMinute = 0
      for th in self.threads:
        getsPerMinute += th.getReqs
        th.getReqs = 0

        postsPerMinute += th.postReqs
        th.postReqs = 0
      
      getsPerMinute = getsPerMinute / len(self.threads)
      postsPerMinute = postsPerMinute / len(self.threads)
      print "[Client:run] Operating at " + str(getsPerMinute) + " GET/m and  " + str(postsPerMinute) + " POST/m"

      # Repeat for bandwidth
      rxBytes = 0
      txBytes = 0
      for th in self.threads:
        rxBytes += th.rxBytes
        th.rxBytes = 0

        txBytes += th.txBytes
        th.txBytes = 0
      
      rxBytes = rxBytes / len(self.threads)
      txBytes = txBytes / len(self.threads)
      rxBytes = rxBytes / 1000000
      txBytes = txBytes / 1000000
      print "[Client:run] Downloading at " + str(rxBytes) + " MB/m and Uploading at " + str(txBytes) + " MB/m"

      # Have a snooze...
      time.sleep(60)

# Create a Client class and start it running
def main():

  # Setup number of threads default
  number = 2
  # Adjust if given a command line argument
  if (len(sys.argv) > 1):
    number = int(sys.argv[1])
    print 'Starting client with ' + str(number)

  client = SimpleClient(number)         # Call Constructor
  client.start()            # Start thread
  
  # Enable keyboard interrupts
  while not client.kill_received:
    try:
      client.join(1)
    except KeyboardInterrupt:
      print "Ctrl-c received! Sending kill to threads..."
     
      # and all HTTP clients
      client.killThreads()
      # and the main client
      client.kill_received = True
  
if __name__ == '__main__':
  main()