"""
Client Subclass - Customise behaviour for High Usage scenarios

@author: James Smith (jws7) @ St Andrews
"""
from HTTPClient import *
class HighHTTPClient(HTTPClient):

  """
  Overriding method from superclass
  """
  def browsePage(self, url):
    print '[HighHTTPClient:browsePage] in browsePage method'
    print 'Browsing: ' + url

# Test Functionality
def main():
  highClient = HighHTTPClient()       # Call Constructor in Client
  highClient.browsePage("http://google.com") # Call overriding behaviour method

if __name__ == '__main__':
  main()