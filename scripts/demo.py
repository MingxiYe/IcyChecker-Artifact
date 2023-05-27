import os,re,json,sys

demoOutputPath = os.path.abspath(os.path.dirname(os.getcwd()))
demoOutputPath = os.path.join(demoOutputPath, "demo/output")
inners = ["0x01f8c4e3fa3edeb29e514cba738d87ce8c091d3f"]

for jsonFile in os.listdir(demoOutputPath):
    jsonPath = os.path.join(demoOutputPath, jsonFile)
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
                if key in mutAlloc[add]["storage"] \
                   and value != mutAlloc[add]["storage"][key]:
                    flag = True
        if not flag:
            continue
        # output result
        print("=================detection result overview===============")
        print("SI Pattern  : control flow hijack")
        print("=================the original transaction================")
        print("From        : ", loadDict["inputMessage"]["from"])
        print("To          : ", loadDict["inputMessage"]["to"])
        print("Message Data: ", loadDict["inputMessage"]["input"])
        print("=================the generated transaction===============")
        print("From        : ", loadDict["additMessageFrom"])
        print("To          : ", loadDict["additMessageTo"])
        print("Decoded Data: ", loadDict["additMessageData"])