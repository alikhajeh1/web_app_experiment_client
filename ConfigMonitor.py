
"""
Browse Config files and act on any recent changes

@author: James Smith
"""

# Import FileIO methods
from FileIO import read as read
from FileIO import write as write

# Time/Date object
import datetime
now = datetime.datetime.now()

# Import Regular Expressions
import re

# Declare a dict to hold the file changes
changeDict = {}
# and Thread dict to hold thread counts for levels
threadDict = {}

# Convert timestamp string into id string
def getID(time):
  YY = time[2:4]
  MM = time[5:7]
  DD = time[8:9]
  hh = time[11:13]
  mm = time[14:16]
  ss = time[17:19]
  return YY + MM + DD + hh + mm + ss

# Add entry to History file if not present
def addIfNotPresent(id, time, level):
  print 'Checking history for ID:' + id

  if id not in changeDict:
    print 'Not found. Addding'
    tuple = (id, time, level)
    print tuple
    changeDict[id] = tuple

    # Now add to history file
    csv = read("history.csv")
    print csv
    line = id + ',' + time + ',' + level.upper()
    print line
    csv = csv + '\n' + line
    write("history.csv", csv)

  print changeDict.items()
  return changeDict # Can pass current changeDict back to Client

"""
Method to parse the config file

Example of a change entry:

<change>
    <time>2012-02-01 09:00:00</time>
    <level>Medium</level>
  </change>
"""
def parseConfig():
  print 'parseConfig method'
  config = read("config.xml")
  print config
  changes = config.split('<change>')
  for s in changes[1:]:
    print 'found change'
    
    # Extract timestamp and convert to id
    time = re.search(r'\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}', s)
    print 'time = ' + time.group()
    id = getID(time.group())
    print 'id = ' + id

    # Extract level
    level = re.search(r'<level>([\w.:]+)</level>', s)
    print 'level = [' + level.group(1) + ']'

    # add to history file
    addIfNotPresent(id, time.group(), level.group(1))

  # Now deal with the pre-defined levels
  levels = config.split('<level ')
  for s in levels[1:]:
    # Extract Level a value
    level = re.search(r'id=\"([\w.:]+)\"', s)
    print 'level = ' + level.group(1)

    # Get thread count
    threads = re.search(r'<threads>(\d+)</threads>', s)
    if threads:  
      print 'threads = [' + threads.group(1) + ']'

      #Now add threads value to dict
      threadDict[level.group(1).upper()] = threads.group(1)
      print threadDict.items()


def main():
  parseConfig()

if __name__ == '__main__':
  main()