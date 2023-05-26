import os,re,json,sys

def getDAppResult(dappPath):
    outputFolder = os.path.join(dappPath, "output")

    # reading from address.txt
    addressPath = os.path.join(dappPath, "address.txt")
    inners = []
    f = open(addressPath, 'r')
    line = f.readline()
    while line:
        addr = line[:len(line) - 1].lower()
        inners.append(addr)
        line = f.readline()
    f.close

    result = {"HOOK":[], "TOD":[], "ENV":[]}
    for jsonFile in os.listdir(outputFolder):
        jsonPath = os.path.join(outputFolder, jsonFile)
        try:
            with open(jsonPath, 'r') as loadF:
                loadDict = json.load(loadF)
                # see if inner is state-inconsistent
                flag = False
                oriAlloc = loadDict["oriAlloc"]
                mutAlloc = loadDict["mutAlloc"]
                for add, state in oriAlloc.items():
                    if add not in inners or "storage" not in state:
                        continue
                    for key, value in state["storage"].items():
                        if value != mutAlloc[add]["storage"][key]:
                            flag = True
                if not flag:
                    continue
                if loadDict["BugType"] == "ENV":
                    result["ENV"].append(loadDict["inputMessage"]["to"])
                elif loadDict["BugType"] == "HOOK":
                    result["HOOK"].append(loadDict["inputMessage"]["to"])
                elif loadDict["BugType"] == "TOD":
                    result["TOD"].append(loadDict["inputMessage"]["to"])
                elif loadDict["BugType"] == "MANI":
                    result["TOD"].append(loadDict["inputMessage"]["to"])
        except Exception:
            continue
    
    result["ENV"] = list(set(result["ENV"]))
    result["HOOK"] = list(set(result["HOOK"]))
    result["TOD"] = list(set(result["TOD"]))
    return result

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("python3 getResult.py <path/to/resultFolderPath>")
        sys.exit(1)
    resultFolderPath = os.path.abspath(sys.argv[1])
    numResult = {"HOOK":0, "TOD":0, "ENV":0}
    
    for dappName in os.listdir(resultFolderPath):
        dappPath = os.path.join(resultFolderPath, dappName)
        dappResult = getDAppResult(dappPath)
        for key, value in dappResult.items():
            numResult[key] += len(list(set(dappResult[key])))

    formatResult = {"Re-entrancy":numResult["HOOK"], \
                    "Front-Running":numResult["TOD"], \
                    "Bad Randomness":numResult["ENV"]}
    print(json.dumps(formatResult, indent = 4))