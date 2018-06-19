from Variables import * #@UnresolvedImport
from urllib import request #@UnresolvedImport

"""-----------------------------------------------------------------------------

Will delete all files of tickerName in ExcelData folder

--------------------------------------------------------------------------------"""
def deleteAll(tickerName):
    fileVariables = Variables()
    directory = fileVariables.directory
    fileEnding = fileVariables.returnFileEnding(tickerName)

    for i in fileEnding:
        try:
            os.remove(directory+i)
        except:
            pass
        
"""-----------------------------------------------------------------------------

Downloads earnings data from stockrow.com. Also adds file ending to excel files. 

--------------------------------------------------------------------------------"""
def downloadAll(tickerName):
    fileVariables = Variables()
    directory = fileVariables.directory
    fileEnding = fileVariables.returnFileEnding(tickerName)
    urlList = fileVariables.returnUrlList(tickerName)
    
    if not os.path.exists(directory):
        os.makedirs(directory)
     
    counter = 0
    for i in urlList:
        try:
            request.urlretrieve(i,directory + fileEnding[counter])
            counter += 1
         
        except:
            print(i + " download failed")