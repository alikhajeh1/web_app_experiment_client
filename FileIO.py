import re
import datetime

now = datetime.datetime.now()
# Change dict
changeDict = {}
# Thread dict
threadDict = {}

# Read a file to string
def write(filename, str):
  print 'Write File method'
  f = open(filename, 'w')
  f.write(str)
  f.close()

# Write string out to file
def read(filename):
  # Open the file for reading
  f = open(filename, 'r')
  print 'Opened ' + filename + '...'
  str = f.read()
  return str

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


"""
Method to add new changes to our list
"""
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

def getID(time):
  YY = time[2:4]
  MM = time[5:7]
  DD = time[8:9]
  hh = time[11:13]
  mm = time[14:16]
  ss = time[17:19]
  return YY + MM + DD + hh + mm + ss

def checkHistory():
  print 'checkHistory method'
  history = read("history.csv")
  lines = history.split('\n')
  for s in lines[1:]:
    values = s.split(',')
    print 'id=' + values[0] 
    print 'time=' + values[1] 
    print 'level=' + values[2]
    print str(now) < values[1] # Comparison of Timestamps

def main():
  parseConfig()
  checkHistory()

if __name__ == '__main__':
  main()