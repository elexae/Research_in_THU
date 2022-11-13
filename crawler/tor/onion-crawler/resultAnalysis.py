import os

rootDir = './results'
resultDirList = os.listDir(rootDir)

for resultDir in resultDirList:
    flowDir = os.path.join(resultDir, 'inflow')
    logsDir = os.path.join(resultDir, 'logs')
    errorSitesFile = os.path.join(logsDir, 'errorSitesFULL.txt')
    entryIpFile = os.path.join(logsDir, 'entryIps.txt')
        