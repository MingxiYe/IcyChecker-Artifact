import os,sys

subFolder = ["0-1Msubstate", \
             "1-2Msubstate", \
             "2-3Msubstate", \
             "3-4Msubstate", \
             "4-5Msubstate", \
             "5-6Msubstate", \
             "6-7Msubstate", \
             "7-8Msubstate", \
             "8-9Msubstate", \
             "9-10Msubstate", \
             "10-11Msubstate", \
             "11-12Msubstate", \
             "12-13Msubstate", \
             "13-14Msubstate", \
             "14-15Msubstate"]

def getCMDs(substateDir, start, end):
    artifactPath = os.path.abspath(os.path.dirname(os.getcwd()))
    subCLIexe = os.path.join(artifactPath, "IcyChecker/build/bin/substate-cli")
    
    ## check if substateDir is properly set
    flag = False
    for folder in os.listdir(substateDir):
        if folder in subFolder:
            flag = True

    CMDs = []
    if not flag:
        cmd = subCLIexe \
            + " replay-SI " \
            + start + " " \
            + end \
            + " --dappDir " + dappPath \
            + " --substateDir " + substateDir \
            + " --rich-info"
        CMDs.append(cmd)
        return CMDs

    for i in range(int(start) // 1000000, (int(end) // 1000000) + 1):
        cmd = ""
        if i == int(start) // 1000000:
            cmd = subCLIexe \
                + " replay-SI " \
                + start + " " \
                + str((i+1)*1000000) \
                + " --dappDir " + dappPath \
                + " --substateDir " + os.path.join(substateDir, f"{i}-{i+1}Msubstate") \
                + " --rich-info"
        elif i == int(end) // 1000000:
            cmd = subCLIexe \
                + " replay-SI " \
                + str(i*1000000) + " " \
                + end \
                + " --dappDir " + dappPath \
                + " --substateDir " + os.path.join(substateDir, f"{i}-{i+1}Msubstate") \
                + " --rich-info"
        else:
            cmd = subCLIexe \
                + " replay-SI " \
                + str(i*1000000) + " " \
                + str((i+1)*1000000) \
                + " --dappDir " + dappPath \
                + " --substateDir " + os.path.join(substateDir, f"{i}-{i+1}Msubstate") \
                + " --rich-info"
        CMDs.append(cmd)
    return CMDs 


def runIcyChecker(dappPath, substateDir):
    absDappPath = os.path.abspath(dappPath)
    substateDir = os.path.abspath(substateDir)
    blockInfoTxt = os.path.join(absDappPath, "blockInfo.txt")

    blockInfo = []
    txtF = open(blockInfoTxt, 'r')
    line = txtF.readline()
    while line:
       blockInfo.append(line.strip('\n'))
       line = txtF.readline()
    txtF.close()
    if len(blockInfo) == 0:
        return
    
    CMDs = getCMDs(substateDir, blockInfo[0], blockInfo[len(blockInfo) - 1])
    for cmd in CMDs:
        os.system(cmd)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("python3 runIcyCheckerInBatch.py <path/to/substateDir>")
        sys.exit(1)
    artifactPath = os.path.abspath(os.path.dirname(os.getcwd()))
    datasetPath = os.path.join(artifactPath, "dataset")
    for dappFolder in os.listdir(datasetPath):
        if dappFolder != "address.dapp.cowswap":
            continue
        dappPath = os.path.join(datasetPath, dappFolder)
        runIcyChecker(dappPath, os.path.abspath(sys.argv[1]))