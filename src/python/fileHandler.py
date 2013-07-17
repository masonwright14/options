import glob
import os.path

# fileName: String name of file
#
# result: a list of lines from the file, with newlines removed
def getLines(fileName):
    myFile = open(fileName, 'r')
    result = []
    for line in myFile:
        result.append(line.rstrip('\n'))
    myFile.close()
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

# aPath: the String path name of the directory, e.g. "stockPrices"
#
# result: a list of paths to contents of the directory
def getSubpaths(aPath):
    return glob.glob(aPath + "/*")

# paths: a list of paths
#
# result: a list of base names, i.e. file names without the full path
def getBaseNames(paths):
    result = []
    for path in paths:
        result.append(os.path.basename(path))
    return result

# aPath: the String path name of the directory, e.g. "stockPrices"
#
# result: a list of base names of contents of the directory,
# i.e. file names without the full path
def getDirContents(aPath):
    return getBaseNames(getSubpaths(aPath))
    
if __name__ == '__main__':
    print getSubpaths("stockPrices")
    print getDirContents("stockPrices")
    pass
