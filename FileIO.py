"""
Simple auxiliary class to provide FileIO methods
"""

# Write string out to file
def write(filename, str):
  print 'Write File method'
  f = open(filename, 'w')
  f.write(str)
  f.close()

# Read a file to string
def read(filename):
  # Open the file for reading
  f = open(filename, 'r')
  print 'Opened ' + filename + '...'
  str = f.read()
  return str