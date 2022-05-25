import gspread
import pandas as pd

class glowingMushroomsAPI:
    def __init__(self, keyPath, workBook, workSheet):

        self.serviceAccount = gspread.service_account(filename = keyPath)

        self.workBook = self.serviceAccount.open(workBook)
        self.workSheet = self.workBook.worksheet(workSheet)

    def getLatestLedConfig(self):
        return pd.DataFrame(self.workSheet.get_all_records())

    def saveJsonDataFrame(self, dataFrame, path):
        dataFrame.to_json(path)
    
    def checkCounts(self, currentDataFrame, lattestDataFrame):
        if len(currentDataFrame) == len(lattestDataFrame):
            return True
        else:
            return False
    
    def checkDiffrence(self, currentDataFrame, lattestDataFrame):
        diffDataFrame = (currentDataFrame - lattestDataFrame)
        diffDataFrame['Diffrence'] = diffDataFrame.sum(axis=1)
        diffDataFrame = (diffDataFrame.loc[diffDataFrame['Diffrence'] != 0]).drop('Diffrence', axis=1)
        countRows = len(diffDataFrame)
        if countRows > 0:
            diffIndex = diffDataFrame.index
            diffDataFrame = lattestDataFrame.filter(items = diffIndex, axis=0)
        
        return diffDataFrame

if __name__ == '__main__':
    pass

