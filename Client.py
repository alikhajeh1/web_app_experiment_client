import urllib

def getURL(url):
  print 'Tasked to get: ' + url
  str = "Page"
  # Get a file-like object for the Python Web site's home page.
  f = urllib.urlopen(url)
  # Read from the object, storing the page's contents in 's'.
  s = f.read()
  f.close()
  return s

def main():
  print getURL("http://www.yahoo.com")

if __name__ == '__main__':
  main()