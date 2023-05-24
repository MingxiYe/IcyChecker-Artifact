import os,sys

def runIcyChecker(dappPath, substateDir):
    absDappPath = os.path.abspath(dappPath)
    substateDir = os.path.abspath(substateDir)
    blockInfoTxt = os.path.join(absDappPath, "blockInfo.txt")
    artifactPath = os.path.abspath(os.path.dirname(os.getcwd()))
    subCLIexe = os.path.join(artifactPath, "IcyChecker/build/bin/substate-cli")

    blockInfo = []
    txtF = open(blockInfoTxt, 'r')
    line = txtF.readline()
    while line:
       blockInfo.append(line.strip('\n'))
       line = txtF.readline()
    txtF.close()
    if len(blockInfo) == 0:
        return
    
    cmd = subCLIexe \
          + " replay-SI " \
          + blockInfo[0] + " " \
          + blockInfo[len(blockInfo) - 1] \
          + " --dappDir " + dappPath \
          + " --substateDir " + substateDir \
          + " --rich-info"

    os.system(cmd)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("python3 runIcyCheckerInBatch.py <path/to/substateDir>")
        sys.exit(1)
    artifactPath = os.path.abspath(os.path.dirname(os.getcwd()))
    datasetPath = os.path.join(artifactPath, "dataset")
    for dappFolder in os.listdir(datasetPath):
        if dappFolder != "address.dapp.0xprotocol":
            continue
        dappPath = os.path.join(datasetPath, dappFolder)
        runIcyChecker(dappPath, os.path.abspath(sys.argv[1]))