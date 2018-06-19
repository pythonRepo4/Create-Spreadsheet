import Ratios
import Utility
import Download
"""-----------------------------------------------------------------------------
spreadSheet(tickerName) will first download past financial data from www.stockrow.com.
It will then get historical data and calculate data points such as gross margins, reinvestment rate,
FCF per share, etc. This is for historical data in a DCF spreadsheet. 

Data is provided with a delimiter (:) or with spaces.  
-----------------------------------------------------------------------------"""
def spreadSheet(tickerName):
       
    ticker = Ratios.TickerFundamentals(tickerName)
    temp = Utility.invert(ticker.spreadSheet())
    spreadSheet = []
    
    for i in temp:
        add = ""
        for j in i:
            add = str(j) + ":" + add
        spreadSheet.append(add)
    
    spreadSheet[0] = "Dates:" + spreadSheet[0]
    spreadSheet[1] = "Revenues:" + spreadSheet[1]
    spreadSheet[2] = "Gross Margin:" + spreadSheet[2]
    spreadSheet[3] = "RD & SGA / Gross Margin:" + spreadSheet[3]
    spreadSheet[4] = "Op Margin:" + spreadSheet[4] 
    spreadSheet[5] = "Reinvestment Rate:" + spreadSheet[5]
    spreadSheet[6] = "Profit Margin:" + spreadSheet[6] 
    spreadSheet[7] = "Net Income per Share:" + spreadSheet[7]
    spreadSheet[8] = "FCF per Share:" + spreadSheet[8]
    spreadSheet[9] = "Cash/Debt per Share:" + spreadSheet[9]
    spreadSheet[10] = "Approx ROIC (No Op Lease):" + spreadSheet[10]
            
    print(str(tickerName))
    print('Historical Data with Delimiter ":" ')
    for i in spreadSheet:
        print(i)
    print("")

    arrays = []
    for i in spreadSheet:
        arrays.append(i.split(":"))
    print("Historical Data Displayed in Table ")    
    Utility.makeTable(Utility.invert(arrays))


""" 

"""

spreadSheet("FB")