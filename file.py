def writeToFile(fileName,data):
        with open(fileName,"w") as f:
            f.write(data)
    
def appendToFile(fileName,data):
    with open(fileName,"a") as f:
        f.write(data)

def readFromFileData(fileName):
    try:
        with open(fileName,"r") as f:
            return f.read()
    except FileNotFoundError as e:
            writeToFile(fileName,"")

def readFromFileLines(fileName):
    try:
        with open(fileName,"r") as f:
            return f.readlines()
    except FileNotFoundError as e:
            writeToFile(fileName,"")