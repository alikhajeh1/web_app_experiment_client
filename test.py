# Import FileIO methods
from FileIO import read as read

# Testing code...
def main():
  print 'Creating a HTTPClient instance'
  newClient = HTTPClient()
  newClient.start()
  
  # Have a snooze...
  time.sleep(1)
  newClient.killself = True

if __name__ == '__main__':
  main()