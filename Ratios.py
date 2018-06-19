import Utility 
import ReadExcel

class TickerFundamentals:
    tickerName = ''
    data = []
    variables = []
    price = []
    priceAvg = []
    ones = []
    
    """This initialization method will get data from getData once so sql is not continually queried"""
    def __init__(self, tickerName, getData = None):
        self.tickerName = tickerName
        temp = ReadExcel.readExcel(tickerName)
        self.variables = temp[0]
        self.data = temp[1:]
        
        i = 0
        while(i < len(self.data)):
            temp = self.data[i]
            numEmpty = 0
            for j in temp:
                if(j == ""):
                    numEmpty += 1
                    
            if(numEmpty > 10):
                del self.data[i]
                continue 
                
            if(temp[0] == ""):
                del self.data[i]
                continue
            i += 1

    """Will return an array of variable (Revenues-T, EPS-T, etc) for all dates"""
    def getVariable(self, variable):
        variableArray = []
        
        j = 0 
        """Go back 10 years or until j < len(data) """
        while(j < len(self.data) and j < 40):
            count = 0
            tempVar = ""
            for i in self.variables:
                if(i == variable):
                    tempVar = self.data[j][count]
                count += 1
            
            variableArray.append(tempVar)
            j += 4
        
        return variableArray
    
    def numShares(self):
        return self.getVariable("Weighted Average Shares-Q")
    
    def getEquity(self):
        return self.getVariable("Shareholders Equity-QB")
    
    def getDebt(self):
        debt = self.getVariable("Total Debt-QB")
        assets = self.getVariable("Total Assets-QB")
        
        try:
            return Utility.myFloat(debt[0]) / Utility.myFloat(assets[0])
        except:
            return 0
        
    def getGoodwill(self):
        goodwill = self.getVariable("Goodwill and Intangible Assets-QB")
        assets = self.getVariable("Total Assets-QB")
        
        try:
            return Utility.myFloat(goodwill[0]) / Utility.myFloat(assets[0])
        except:
            return 0

    def getCashDebt(self):
        cash = self.getVariable("Cash and Equivalents-QB")
        investments = self.getVariable("Investments-QB")
        debt = self.getVariable("Total Debt-QB")
        deposits = self.getVariable("Deposit Liabilities-QB")
        cashDebt = []

        for i in range(0, len(cash)):
            cashDebt.append(Utility.myFloat(cash[i]) + Utility.myFloat(investments[i]) - Utility.myFloat(debt[i]) - Utility.myFloat(deposits[i]))
        
        return cashDebt
    
    """Gets R&D + 10% of SGA which will later be capitalized """
    def getRD_SGA(self):
        rd = self.getVariable("Research and Development (R&D) Expenses-T")
        sga = self.getVariable("Selling, General and Administrative (SG&A) Expenses-T")
        rdaArray = []
        
        if(len(rd) < 1 or len(sga) < 1): 
            rd = self.getVariable("Research and Development Expense-T")
            sga = self.getVariable("Selling, General and Administrative Expense-T")
        
        for i in range(0, len(rd)):
            rdaArray.append(Utility.myFloat(rd[i]) + Utility.myFloat(sga[i]) * 0.10)

        return rdaArray

    """Returns capitalized RD & SGA with a 4 year amortization period. Will return an array with [RD & SGA Cap, Amorization]"""
    def getCapitalizedRDSGA(self):
        rdaArray = self.getRD_SGA()
        RDSGA = []
        
        """If data does not go far back enough, amortizationLength is = rdaArray length """
        amortizationLength = 4
        if(len(rdaArray) <= 4):
            for i in range(0, len(rdaArray)):
                RDSGA.append([0,0])
            return RDSGA
        
        i = 0 
        amortizationPercentage = 1 / amortizationLength
        while(i < len(rdaArray) - amortizationLength):
            RDA_SGA_Capitalization = 0
            amortization = 0
            
            """Capitalize previous RDA/SGA. Then find amortization back 4 years """
            for j in range(1, amortizationLength + 1):
                RDA_SGA_Capitalization += Utility.myFloat(rdaArray[i + j]) * (1 - amortizationPercentage * j)
                amortization += Utility.myFloat(rdaArray[i + j]) * (amortizationPercentage)
                
            RDSGA.append([RDA_SGA_Capitalization, amortization])
            i += 1
            
        """Now approximate both RDA_SGA_Cap and amortization back so that it is same length as rdaArray"""
        years = len(RDSGA) - 1 
        try:
            cagrCap = (RDSGA[0][0]/RDSGA[years][0])**(1/years)
            cagrAmor = (RDSGA[0][1]/RDSGA[years][1])**(1/years)
        except: 
            cagrCap = 1.02
            cagrAmor = 1.02
            
        i = len(RDSGA) - 1
        while(len(RDSGA) < len(rdaArray)):
            RDSGA.append([RDSGA[i][0] / cagrCap, RDSGA[i][1] / cagrAmor])
            i += 1
        
        return RDSGA
    

    def getNOPLAT(self):
        NOPLATarray = []
        rdaArray = self.getRD_SGA()
        RDAmortization = self.getCapitalizedRDSGA()
        
        EBIT = self.getVariable("EBIT-T")

        """NOPLAT is calculated as EBIT + current research + SG&A - RDSGA amortiziation 
        LESS adjusted taxes. (Effective Tax Rate not actual paid)  """
        for i in range(0, len(EBIT)):
            _ , RDamor = RDAmortization[i] 
            taxRate = .21
            NOPLAT = (Utility.myFloat(EBIT[i]) + Utility.myFloat(rdaArray[i]) - RDamor) * (1 - taxRate)
            NOPLATarray.append(NOPLAT)
#             print(str(EBIT[i]) + " : " + str(rd[i]) + " : " + str(sga[i]))
#             print(NOPLAT)
        return NOPLATarray
        
    def getInvestedCapital(self):  
        investedCapital = []
        RDAmortization = self.getCapitalizedRDSGA()
        cash = self.getVariable("Cash and Equivalents-QB")
        currentAssets = self.getVariable("Current Assets-QB")
        currentLiabilities = self.getVariable("Current Liabilities-QB")
        ppe = self.getVariable("Property, Plant & Equipment Net-QB")
        goodwill = self.getVariable("Goodwill and Intangible Assets-QB")
        shareholdersEquity = self.getVariable("Shareholders Equity-QB")
        investments = self.getVariable("Investments-QB")
        totalDebt = self.getVariable("Total Debt-QB")
        nonCurrent = self.getVariable("Investments Non-Current-QB")
        totalAssets = self.getVariable("Total Assets-QB")
        totalLiabilities = self.getVariable("Total Liabilities-QB")
        
        """----------------------------------------------------------------
        Invested Capital is capital used to 
        There are two methods to calculate invested capital:
        
        1) Invested Capital w/ Goodwill = Current Assets - Current Liabilities - Excess Cash + Fixed Assets (PPE) + Goodwill + PV of Op Leases
                                        
                                        
        2) Invested Capital w/ Goodwill = Shareholders Equity + Total Debt - Cash * .95 + PV of Op Leases
        ----------------------------------------------------------------"""
        for i in range(0, len(cash)):
            researchCap, researchAmor = RDAmortization[i] 
            investedCapital1 = Utility.myFloat(currentAssets[i]) - Utility.myFloat(currentLiabilities[i]) - (0.80 * Utility.myFloat(cash[i])) + Utility.myFloat(ppe[i]) \
            + Utility.myFloat(goodwill[i]) + researchCap - researchAmor 
            
            investedCapital2 = Utility.myFloat(totalAssets[i]) - Utility.myFloat(totalLiabilities[i]) + Utility.myFloat(totalDebt[i]) + researchCap - researchAmor - \
            (.80 * Utility.myFloat(cash[i])) - Utility.myFloat(nonCurrent[i])
            if(investedCapital2 < 0): 
                investedCapital2 = Utility.myFloat(totalDebt[i]) + researchCap - researchAmor - (.80 * Utility.myFloat(cash[i])) - Utility.myFloat(nonCurrent[i])
                
#             """If investedCapital1 is much smaller than investedCapital2, investedCapital1 may not have Investments  """
#             if(investedCapital1 < investedCapital2 * 0.75):
#                 investedCapital1 = (0.9) * Utility.myFloat(cash[i]) + Utility.myFloat(investments[i])
    
            
            investedCapital.append([investedCapital1, investedCapital2])
        
#         for i in investedCapital:
#             print(i)
            
        return investedCapital
    
    def getFCF(self):
        FCF = []
        netIncome = self.getVariable("Net Income-T")
        capEX = self.getVariable("Capital Expenditure-TC")
        operatingCashFlow = self.getVariable("Operating Cash Flow-TC")
        stockBasedCompensation = self.getVariable("Share Based Compensation-TC")
        getFCF = self.getVariable("Free Cash Flow-TC")
        
        for i in range(0, len(netIncome)):
            FCFtemp = Utility.myFloat(operatingCashFlow[i]) + Utility.myFloat(capEX[i])- Utility.myFloat(stockBasedCompensation[i])
            FCFtemp = Utility.myFloat(getFCF[i]) - Utility.myFloat(stockBasedCompensation[i])
            FCF.append(FCFtemp)

        return FCF
        
    def getROIC(self):
        """ROIC is calculated as NOPLAT/Invested Capital"""
        NOPLAT = self.getNOPLAT()
        investedCapital = self.getInvestedCapital()
        dates = self.getVariable("dates")
        
#         for i in NOPLAT:
#             print(i)
#             
#         print(" ")
#         
#         for i in investedCapital:
#             print(i)

        returnROIC = []
        returnROICavg = []
        
        i = 0
        while(i + 1 < len(investedCapital)):
            try:
                ROIC1 = NOPLAT[i] / investedCapital[i + 1][0]
            except:
                ROIC1 = 0 
             
             
            try:
                ROIC2 = NOPLAT[i] / investedCapital[i + 1][1]
            except:
                ROIC2 = 0 
                 
            """Append date, ROIC1, ROIC2
            If NOPLAT is less than or equal to 0, return 0 for ROIC
            """
            if(NOPLAT[i] <= 0):
                returnROIC.append([0, 0])
                returnROICavg.append(0)
            else:
                returnROIC.append([ROIC1, ROIC2])
                returnROICavg.append((ROIC1+ROIC2)/2)
            
            dates.append(self.data[i][0])
            
            i += 1
            
    #     for i in returnROIC:
    #         print(i)
    #     
    #     for i in returnROICavg:
    #         print(i)
     
        return [returnROIC, returnROICavg]
    
    def reinvestment(self):
        reinvestment = []
        rd = self.getRD_SGA()
        rdCapitalization = self.getCapitalizedRDSGA()
        CAPEX = self.getVariable("Capital Expenditure-TC")
        deprAmortization = self.getVariable("Depreciation & Amortization-TC")
        currentAssets = self.getVariable("Current Assets-QB")
        currentLiabilities = self.getVariable("Current Liabilities-Q")
        cash = self.getVariable("Cash and Equivalents-QB")
        
        """Reinvestment of Capital is as follows: CAPEX - depreciation + RD - RDamor + change in working cap - change in excess cash"""
        for i in range(0, len(rd)- 1): 
            _, rdAmor = rdCapitalization[i]
            reinvestment.append(-1 * Utility.myFloat(CAPEX[i]) - Utility.myFloat(deprAmortization[i]) + Utility.myFloat(rd[i]) - Utility.myFloat(rdAmor)
                     + Utility.myFloat(currentAssets[i]) - Utility.myFloat(currentLiabilities[i]) 
                     - (Utility.myFloat(currentAssets[i+1]) - Utility.myFloat(currentLiabilities[i+1])) - ((.8) * Utility.myFloat(cash[i]) - (.8) * Utility.myFloat(cash[i+1])))

        reinvestment.append(reinvestment[-1])
        return reinvestment
    
    """-----------------------------------------------------------------------------
    Returns revenues, gross margin, operating margin, net income, 
    -----------------------------------------------------------------------------"""
    def spreadSheet(self):
        spreadSheet = []

        fcf = self.getFCF()
        NOPLAT = self.getNOPLAT()
        RD_SGA = self.getRD_SGA()
        _ ,roic = self.getROIC()
        numShares = self.numShares()
        reinvestment = self.reinvestment()
        cashDebt = self.getCashDebt()
        date = []
       
        i = len(roic)
        while(i < len(fcf)):
            roic.append(roic[-1])
            i += 1
        
        revenues = self.getVariable("Revenue-T")
        gross = self.getVariable("Gross Profit-T")
        operating = self.getVariable("Operating Income-T")
        netIncome = self.getVariable("Net Income-T")
        averagePrice = self.getVariable("Average Price")

        """Get first dates"""
        j = 0 
        while(j < len(self.data)):
            """Get date (first date)"""
            count = 0 
            for i in self.variables:
                if(i == 'dates'):
                    temp = self.data[j][count]
                    break
                count += 1
            date.append(temp)
            j += 4
        
        """ 
        0 - dates
        1 - revenues
        2 - gross margin
        3 - RD & SGA / Gross Margin 
        4 - op margin 
        5 - reinvestment rate
          - profit margin
        6 - net income per share
        7 - fcf per share
          - cash/debt
        8 - ROIC
          - AveragePrice
        """
        for i in range(0, len(revenues)):
            spreadSheet.append([date[i], Utility.myFloat(revenues[i]),
                                str(round(Utility.myFloat(gross[i])/Utility.myFloat(revenues[i]), 4)), 
                                str(round(Utility.myFloat(RD_SGA[i])/Utility.myFloat(gross[i]), 4)), 
                                str(round(Utility.myFloat(operating[i])/Utility.myFloat(revenues[i]), 4)), 
                                str(round(Utility.myFloat(reinvestment[i])/Utility.myFloat(NOPLAT[i]) , 4)),
                                str(round(Utility.myFloat(netIncome[i])/Utility.myFloat(revenues[i]), 4)),
                                str(round(Utility.myFloat(netIncome[i])/Utility.myFloat(numShares[i]), 4)),
                                str(round(Utility.myFloat(fcf[i])/Utility.myFloat(numShares[i]), 4)), 
                                str(round(Utility.myFloat(cashDebt[i])/Utility.myFloat(numShares[i]), 4)), 
                                str(round(roic[i], 4)) ])
         
        return spreadSheet
    


             
 
# t = TickerFundamentals("FB")
# value = t.getVariable("Free Cash Flow-TC")
# for i in value:
#     print(i)
     
     
    