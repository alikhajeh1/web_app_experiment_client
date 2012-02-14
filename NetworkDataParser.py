# Create a Client class and start it running
def main():
  print 'Starting data parse'

  # Echo the contents of a file
  fileIn = open('../query_result.csv', 'r')
  fileOut = open('../NetData.csv', 'w')
  count = 0;
  prev = 0;
  for line in fileIn:

     
    if count > 0:
      values = line.split(",")

      rxtx = int(values[0]) + int(values[1])
      #print 'rxtx = ' + str(rxtx)

      if prev == 0:
        prev = rxtx
      else:
        diff = rxtx - prev
        prev = rxtx
        #print 'Difference = ' + str(diff)

        # Append to line()
        print 'line = [' + line[:-1] + ']'

        newData = '\t' + str(rxtx) + '\t' + str(diff)
        print 'newData = [' + newData + ']'

        # Concat Strings, removing new line char
        newLine = values[0] + '\t' + values[1][:-1] + '\t' + newData + '\n'
        print 'newLine = [' + newLine + ']'

        # Write line out to new file
        fileOut.write(newLine)

    else:
      print 'First (headers) line'

      values = line.split(",")

      newLine = values[0] + '\t' + values[1][:-1] + '\t' + 'rxtx\tdiff\n'

      # Write headers to file
      fileOut.write(newLine)

    # Increment line counter
    count = count + 1

  # Tidy up
  fileIn.close()
  fileOut.close()

if __name__ == '__main__':
  main()