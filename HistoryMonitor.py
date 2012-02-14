
"""
Browse history file and act on any recent Timestamps

@author: James Smith
"""

# Import FileIO methods
from FileIO import read as read

# Time/Date object
import datetime
from datetime import timedelta

def checkHistory():
  print 'checkHistory method'
  history = read("history.csv")
  entries = history.split('\n')

  # Now define a Timestamp string for the last hour
  now = datetime.datetime.now()
  lastHour = now - timedelta(hours=1)
  print 'Last hour: ' + str(lastHour)

  for entry in entries[1:]: # Ignore headers

    # Extract values -> values[0]=id, values[1]=time, values[2]=level
    values = entry.split(',') 

    # If current entry was in the last hour but less than now
    if values[1] > str(lastHour):
      if values[1] < str(now):
        print 'Entry ' + values[0] + ' in the last hour'
        return entry
  
  # If we have found no entry in the last hour  
  # return a signal
  print 'No entries in the last hour'
  return 'current'

def main():
  checkHistory()

if __name__ == '__main__':
  main()