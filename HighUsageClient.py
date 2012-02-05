
from Client import *

"""
Client Subclass - Customise behaviour for High Usage scenarios

@author: James Smith
"""
class HighUsageClient(Client):

  """
  Overriding method from superclass
  """
  def behaviour(self):
    print '[HighUsageClient:behaviour:] in method'

# Test Functionality
def main():
  highClient = HighUsageClient() # Call Constructor in Client
  highClient.behaviour()         # Call overriding behaviour method

if __name__ == '__main__':
  main()