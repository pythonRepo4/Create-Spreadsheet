from Variables import * #@UnresolvedImport
import xlrd 
import Utility
import os
import Download
"""-----------------------------------------------------------------------------------

 Will get quarterly and ttm data from stock row files. Will put this into a dataArray 
 column that looks as follows:
 
 [MM/DD/YYYY, quarterly, ttm], etc
 
 Afterwards should call sql method insertSQL(CSCO,data)
-----------------------------------------------------------------------------------"""
def readExcel(tickerName):
    fileVariables = Variables()
    directory = fileVariables.directory
    endings = fileVariables.ending
    fileEnding = fileVariables.returnFileEnding(tickerName)
        
    """Opens each excel file and puts them in sheets array """
    sheets = []
    for i in fileEnding:
        fileNameTemp = directory + i
        if(os.path.isfile(fileNameTemp) == False):
            Download.downloadAll(tickerName)
        tempBook = xlrd.open_workbook(fileNameTemp)
        sheets.append(tempBook.sheet_by_index(0))
        
    """Get dates from first sheet. These dates will be used for all other sheets"""
    i = 0
    j = 0
    dates = []
    dates.append("dates")
    
    firstSheet = sheets[0]
    while(j < firstSheet.ncols):
        tempDate = firstSheet.cell_value(0,j)
        j+=1
        if(tempDate != ' ' and tempDate != ''):
            dateTuple = xlrd.xldate_as_tuple(tempDate,0)
            dates.append(str(dateTuple[0]) + "/" + str(dateTuple[1]) + "/" + str(dateTuple[2]))
      
    """Now, get all other data from all sheets. """
    """Add dates and other data to totalArray """
    j = 0
    totalArray = []
    totalArray.append(dates)
     
    """Goes through each sheet"""
    for iterator in range(0,len(sheets)):
        sheet = sheets[iterator]
        ending = endings[iterator]
        i = 1
        """Goes down row in each sheet and then across each column to get all data"""
        while(i < sheet.nrows):
            tempData = []
            j = 0 
            while(j < sheet.ncols):
                """Will add file ending (-Q, -T, -QB etc) for variable name which is 
                j = 0.""" 
                if(j == 0):
                    tempData.append(str(sheet.cell_value(i,j)) + ending)
                else:
                    tempData.append(sheet.cell_value(i,j))
                j += 1
            i += 1
            totalArray.append(tempData)
     
#     for i in totalArray:
#         print(len(i))
#         print(i)
      
    """Now make sure length of all arrays are the same"""
    longestArray = 0
    for i in totalArray:
        if(len(i) > longestArray):
            longestArray = len(i)
          
    for i in totalArray:
        appendNumber = longestArray - len(i)
        for j in range(0,appendNumber):
            i.append('')
        
#     for i in totalArray:
# #         print(len(i))
#         print(i)
#      
    return Utility.invert(totalArray)
