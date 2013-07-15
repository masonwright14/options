
# fileName: String name of file
#
# result: a list of lines from the file, with newlines removed
def getLines(fileName):
    myFile = open(fileName, 'r')
    result = []
    for line in myFile:
        result.append(line.rstrip('\n'))
    return result

# fileName: String name of file
#
# result: list of lists, where each item in the outer list
# represents one line from the file, and each item in each inner list
# is a string that results from splitting the row on commas
def getRowsAfterHeader(fileName):
    lines = getLines(fileName)
    del lines[0]
    result = []
    for line in lines:
        result.append(line.split(","))
    return result
