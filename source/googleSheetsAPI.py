import gspread
import pandas as pd
import time

class glowingMushroomsAPI:
    def __init__(self, keyPath, workBook, workSheet):

        self.serviceAccount = gspread.service_account(filename = keyPath)

        self.workBook = self.serviceAccount.open(workBook)
        self.workSheet = self.workBook.worksheet(workSheet)

    def getLatestLedConfig(self):
        return pd.DataFrame(self.workSheet.get_all_records())

    def saveLatestConfig(self, dataFrame, path):
        dataFrame.to_json(path)
    
    def checkCounts(self, currentDataFrame, lattestDataFrame):
        if len(currentDataFrame) == len(lattestDataFrame):
            return True
        else:
            return False
    
    def checkDiffrence(self, currentDataFrame, lattestDataFrame):
        diffDataFrame = (currentDataFrame - lattestDataFrame)
        diffDataFrame['Diffrence'] = diffDataFrame.sum(axis=1)
        diffDataFrame= (diffDataFrame.loc[diffDataFrame['Diffrence'] != 0]).drop('Diffrence', axis=1)
        return diffDataFrame




ledConfigPath = "source/json/ledConfig.json"


gm = glowingMushroomsAPI('service_account.json', 'PM-GlowingMuhrooms', 'config')
latestLedConfig = gm.getLatestLedConfig()

gm.saveLatestConfig(latestLedConfig, ledConfigPath)

print(len(latestLedConfig))

print(gm.checkCounts(latestLedConfig, latestLedConfig))

print(gm.checkDiffrence(latestLedConfig, latestLedConfig))

# while True:
#     print(gm.getLatestLedConfig())
#     #time.sleep(10)






