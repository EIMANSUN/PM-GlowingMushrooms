#Standard imports
from asyncio import start_server
import json
import time
import multiprocessing as mp

#Dependancies
import pandas as pd
import board
import neopixel
 
#Modules
from googleSheetsAPI import glowingMushroomsAPI
from  ledController import ledConfig

# Setup
requestDelay = 10
ledConfigPath = "source/json/ledConfig.json"
ledConfigDiffPath = "source/json/ledConfigDiff.json"
updateStatusPath = "source/json/updateStatus.json"
apiState = 0
try:
    gm = glowingMushroomsAPI('service_account.json', 'PM-GlowingMuhrooms', 'config')
except:
    apiState = 1
finally:
    print(f"API State - {apiState}")


#Reset update status
updateStatus = {"Update":0}
with open(updateStatusPath, 'w') as outfile:
    json.dump(updateStatus, outfile)
    print(f"Saved - {updateStatusPath} by Main")

def initializeGoogleAPI():
    internetCheck = 0
    failCount = 0
    while internetCheck == 0:
        try:
            latestLedConfig = gm.getLatestLedConfig()
            internetCheck = 1
        except:
            print("Failed to load data")
            internetCheck = 0
            failCount += 1
            time.sleep(10)
        finally:
            if internetCheck == 1:
                gm.saveJsonDataFrame(latestLedConfig, ledConfigPath)
                print("LED config downloaded")
            if failCount == 100:
                latestLedConfig = pd.read_json(ledConfigPath)

        return latestLedConfig

def loopGoogleAPI(latestLedConfig, currentLedConfig):
    while True:
        time.sleep(requestDelay)
        while True:
            try:
                latestLedConfig = gm.getLatestLedConfig()
                break
            except:
                print("Failed to load data")
                time.sleep(10)

        if not gm.checkCounts(currentLedConfig, latestLedConfig):
            #Restart ledController to be made
            pass
        else:
            diffConfig = gm.checkDiffrence(currentLedConfig, latestLedConfig)
            if not diffConfig.empty:
                print(diffConfig)
                #Save LED Config diffrences json
                gm.saveJsonDataFrame(diffConfig, ledConfigDiffPath)

                # Save json indicating the chage exists
                updateStatus = {"Update":1}
                with open(updateStatusPath, 'w') as outfile:
                    json.dump(updateStatus, outfile)
                print(f"Saved - {updateStatusPath} by Google sheets API")

                #Update main LED Config json
                gm.saveJsonDataFrame(latestLedConfig, ledConfigPath)
            
        currentLedConfig = latestLedConfig

def setupLED(ledConfigPath):
    with open(ledConfigPath) as json_file:
        data = json.load(json_file)

    ledCount = len(data['LedNum'])

    ledConfigList = []
    for i in range(ledCount):
        print(i)
        singleLedConfig = {}
        for key, value in data.items():
            singleLedConfig[key] = value[str(i)]
        ledConfigList.append(ledConfig(singleLedConfig))

    print(ledConfigList)
    pixels = neopixel.NeoPixel(board.D18, ledCount)

    return pixels, ledCount, ledConfigList

def loopLED(pixels, ledCount, ledConfigList, ledConfigDiffPath, updateStatusPath):
    updateCounter = 0
    while True:
        startTime = time.time()
        #Check for UPDATE
        ledUpdateStatus = 0
        if updateCounter >= 50:
            with open(updateStatusPath) as json_file:
                status = json.load(json_file)
                if status['Update'] == 1:
                    ledUpdateStatus = 1
                    with open(ledConfigDiffPath) as json_file:
                        data = json.load(json_file)
                    print(f"Loaded - {updateStatusPath} by LED Controller")

                    ledId = data['LedNum'].values()

                    diffLedConfig = {}
                    for i in ledId:
                        singleLedConfig = {}
                        for key, value in data.items():
                            singleLedConfig[key] = value[str(i)]
                        diffLedConfig[str(i)] = singleLedConfig
                    print(diffLedConfig)
                    updateCounter = 0

        for x in range(0, ledCount):
            if ledUpdateStatus == 1:
                if str(x) in diffLedConfig:
                    print(f"Led No - {x} updated to {diffLedConfig[str(x)]}")
                    ledConfigList[x].ledParam = diffLedConfig[str(x)]

            pixels[x] = (ledConfigList[x].getRed(), ledConfigList[x].getGreen(), ledConfigList[x].getBlue())

        if ledUpdateStatus == 1:
            updateStatus = {"Update":0}
            with open(updateStatusPath, 'w') as outfile:
                json.dump(updateStatus, outfile)
            print(f"Saved - {updateStatusPath} by LED Controller")

        updateCounter += 1
        endTime = (time.time() - startTime) * 1000
        print(f"{endTime} ms")

if __name__ == '__main__':

    #Initialise google sheets api
    if apiState == 0:
        latestLedConfig = initializeGoogleAPI()
        currentLedConfig = latestLedConfig

    #Setup LED's
    setup = setupLED(ledConfigPath)
    pixels = setup[0]
    ledCount = setup[1]
    ledConfigList = setup[2]

    if apiState == 0:
        p1 = mp.Process(target=loopGoogleAPI, args=(latestLedConfig, currentLedConfig))


    p2 = mp.Process(target=loopLED, args=(pixels, ledCount, ledConfigList, ledConfigDiffPath, updateStatusPath))

    if apiState == 0:
        p1.start()

    p2.start()







