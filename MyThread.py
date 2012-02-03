import threading

import datetime

now = datetime.datetime.now()

class MyThread ( threading.Thread ):

   def run ( self ):
      print "Current date and time using str method of datetime object:"
      print str(now)
