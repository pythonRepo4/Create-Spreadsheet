
import os

'''-----------------------------------------------------------------------------------

This class holds multiple variables such as directory, fileEnding

-----------------------------------------------------------------------------------'''
class Variables:
    def __init__(self):
        pass
    
    preDirectory = str(os.getcwd()) + "\\"
    keyword = 'DCF SpreadSheet\\'
    length = preDirectory.find(keyword)  + len(keyword)
    preDirectory = preDirectory[0:length]
    
    directory = preDirectory + "download\\"

    def returnUrlList(self, tickerName):
        
        """Yahoo finance is not working as of 20 May 2017 """
            
        urlList = ["https://stockrow.com/api/companies/" + tickerName + "/financials.xlsx?dimension=MRQ&section=Income%20Statement",  #Quarterly Income Statement
            
                   "https://stockrow.com/api/companies/" + tickerName +  "/financials.xlsx?dimension=MRT&section=Income%20Statement",  #TTM Income Statement
            
                   "https://stockrow.com/api/companies/" + tickerName + "/financials.xlsx?dimension=MRQ&section=Balance%20Sheet",      # Quarterly Balance Sheet
            
                   "https://stockrow.com/api/companies/" + tickerName + "/financials.xlsx?dimension=MRQ&section=Cash%20Flow",      # Quarterly Cash Flow
            
                   "https://stockrow.com/api/companies/" + tickerName + "/financials.xlsx?dimension=MRT&section=Cash%20Flow",      # TTM Cash flow
            
                   "https://stockrow.com/api/companies/" + tickerName + "/financials.xlsx?dimension=MRQ&section=Metrics",     #Quarterly Metrics
            
                   "https://stockrow.com/api/companies/" + tickerName + "/financials.xlsx?dimension=MRT&section=Metrics",      #TTM Metrics
            
                   "https://stockrow.com/api/companies/" + tickerName + "/financials.xlsx?dimension=MRQ&section=Growth"      #Quarterly Growth
            ]
        
        return urlList
    
    ending = ["-Q",        #Quarterly Income Statement
                  "-T",        #TTM Income Statement
                  "-QB",       #Quarterly Balance Sheet
                  "-QC",       #Quarterly Cash Flow
                  "-TC",       #TTM Cash Flow
                  "-QM",       #QuarterlyMetrics
                  "-TM",       #TTM Metrics
                  "-QG"]       #Quarterly Growth
    
    fileEnding = ["-Q.xlsx",        #Quarterly Income Statement
                  "-T.xlsx",        #TTM Income Statement
                  "-QB.xlsx",       #Quarterly Balance Sheet
                  "-QC.xlsx",       #Quarterly Cash Flow
                  "-TC.xlsx",       #TTM Cash Flow
                  "-QM.xlsx",       #Quarterly Metrics
                  "-TM.xlsx",       #TTM Metrics
                  "-QG.xlsx"]       #Quarterly Growth
    
    def returnFileEnding(self, tickerName):
        returnVar = []
        
        for i in range(0,len(self.fileEnding)):
            returnVar.append(tickerName + self.fileEnding[i])
            
        return returnVar
    
    
    
