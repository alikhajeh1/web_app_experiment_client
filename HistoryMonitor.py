
"""
Browse history file and act on any recent Timestamps
"""

# Import FileIO methods
from FileIO import read as read

# Time/Date object
import datetime
now = datetime.datetime.now()

def checkHistory():
  print 'checkHistory method'
  history = read("history.csv")
  lines = history.split('\n')
  for s in lines[1:]:
    values = s.split(',')
    print 'id=' + values[0] 
    print 'time=' + values[1] 
    print 'level=' + values[2]
    print str(now) < values[1] # Comparison of Timestamps - True if
    if str(now) < values[1]:
      print 'Entry in future'
    else:
      print 'Entry in past' 

def main():
  checkHistory()

if __name__ == '__main__':
  main()