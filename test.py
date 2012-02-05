# Enable Regular Expressions
import re

# Import FileIO methods
from FileIO import read as read

# Testing code...
def main():
  url = "practice.html"
  html = read(url)
  print html

  list = []
  # Grab list of all strings that match the regex
  srcs = re.findall(r'src=\"([\w\.:=/\?-]+)\"', html)
  # add each link to the list
  list.extend(srcs)
  # repeat for hrefs
  hrefs = re.findall(r'link\shref=\"([\w\.:=/\?-]+)\"', html)
  list.extend(hrefs)
  
  # debug
  for s in srcs:
    print 'src: [' + s + ']'
  for s in hrefs:
    print 'hrefs: [' + s + ']'
  
  # download all links
  for s in list:
    link = '' # empty string
    if url.endswith('/'):
      link = url[:-1]
    else:
      link = url
    if s.startswith('http'):
      link = s
    else:
      link = link + s
    
    print link

if __name__ == '__main__':
  main()