import json

ledConfigPath = "source/json/ledConfig.json"
ledConfigDiffPath = "source/json/ledConfigDiff.json"
updateStatusPath = "source/json/updateStatus.json"

# with open(updateStatusPath) as json_file:
#     data = json.load(json_file)
#     print(data['Update'])

# with open(ledConfigDiffPath) as json_file:
#     data = json.load(json_file)
#     print(data)

#     print(len(data))


with open(ledConfigDiffPath) as json_file:
    data = json.load(json_file)


ledId = data['LedNum'].values()

diffLedConfig = {}
for i in ledId:
    print(i)
    singleLedConfig = {}
    for key, value in data.items():
        singleLedConfig[key] = value[str(i)]
    diffLedConfig[str(i)] = singleLedConfig


print(diffLedConfig['7'])