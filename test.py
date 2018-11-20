import glob
from pathlib import Path
import os
import shutil
from shutil import *
import fileinput
import strreplace as strr

## BIG TODO:
## CHECK IF MULTIPLE ENGINES EXIST, DELETE/IGNORE OLD, USE NEW

class OfflineBundler:
    def __init__(self, mn, en):
        self.mapName = mn
        self.errors = []
        self.cwd = os.getcwd()
        self.targetPath = self.cwd + "/map/" + mn
        self.engineNo = open(en,"r").read()
        self.units = next(os.walk(self.targetPath))[1]
        if 'stagingArea' in self.units:
            self.units.remove('stagingArea')     

    def checkIfEntryPointExists(self):
        if not os.path.isfile(self.targetPath + "/entryPoint.txt"):
            self.errors.append("Fatal: Entry point doesn't exist or isn't correctly formatted. Looking for \"entryPoint.txt\"");
        else:
            self.entryPoint = open(self.targetPath + "/entryPoint.txt", "r").read()

    def copyToStagingArea(self):
        #print (self.cwd)
        #if not os.path.exists("stagingArea"):
            #try:
        shutil.copytree(self.targetPath, self.targetPath + "/stagingArea", ignore=ignore_patterns("entryPoint.*", "test.py", "*.sh", "*.html"))
            #except:
            #    self.errors.append("Fatal: Copy of node folders failed for some reason.")
        #else:
            #self.errors.append("Fatal: Old staging area folder already exists.")

    def checkJSONExistsNewerEngine(self):

        self.stagePath = self.targetPath + "/stagingArea/"
        self.jsonFiles = {}

        for u in self.units:
            filesToCheck = os.listdir(self.stagePath + u)
            unitJSON = ""
            unitXML = ""
            for f in filesToCheck:
                if ".json" in f and "modified" not in f:
                    unitJSON = self.stagePath + u + "/" + f
                    try:
                        self.jsonFiles[u] = unitJSON
                        version = (f[f.index("1"):f.index(".json")])
                        if version != self.engineNo:
                            self.errors.append("Fatal: Outdated engine (" + version + ") at\n" + self.stagePath + u)
                    except:
                        self.errors.append("Fatal: Something went wrong. Missing JSON, maybe?")

                if "MainXML" in f:
                    unitXML = self.stagePath + u + "/" + f

            if not unitJSON:
                self.errors.append("Fatal: JSON file missing at\n" + self.stagePath + u)
            else:
                if self.isNewer(unitJSON, unitXML):
                    self.errors.append("Warning: JSON outdated at\n" + u)
            if not unitXML:
                self.errors.append("Fatal: XML file missing at\n" + self.stagePath + u)
                break;

            


        '''

            unitJSON = ""
            unitXML = ""
            for f in filesToCheck:
                if ".json" in f and "modified" not in f: 
                    unitJSON = path + f
                if "MainXML" in f:
                    unitXML = path + f
            if not unitJSON:
                self.errors.append("Fatal: JSON file missing at " + path)
                break;
            if not unitXML:
                self.errors.append("Fatal: XML file missing at " + path)
                break;
        '''

        #print (isNewer(os.getcwd()+"/stagingArea/", filesToCheck[1], filesToCheck[3]))
        #print (os.getcwd() + filesToCheck[1])
        #print(isNewer(filesToCheck[1],filesToCheck[2]))

    def isNewer(self, new, old):
        result = os.path.getmtime(new)-os.path.getmtime(old)
        if (result is 0):
            self.errors.append("The files were created at the same exact time. Weird.")
        else:
            return (result < 0)

    def buildRunHTML(self):
        print ("i hate you")
        for u in self.units:
            print (self.cwd + "/run.html")
            shutil.copy(self.cwd + '/run.html', self.stagePath)

            with open(self.jsonFiles[u], 'r') as someFile:
                jsonData = someFile.read()

            print (self.stagePath + "run.html")

            try:
                with fileinput.FileInput(self.stagePath + "run.html", inplace="True") as file:
                    for line in file:
                        print(strr.replaceAll(
                            line, [
                                ["{REL_ROOT}", ".."],
                                ["{ENGINE}", self.engineNo],
                                ["{PUBBLY_JSON}", jsonData]
                            ]), end='')
            except:
                self.errors.append("Fatal: Constructing run files failed.")

            os.rename(self.stagePath + "run.html", self.stagePath + u + ".html")

            # Overwrite new run file with appropriate info
        '''
            try:
                with fileinput.FileInput(self.stagePath + u + "/run.html", inplace="True") as file:
                    for line in file:
                        print(strr.replaceAll(
                            line, [
                                ["{REL_ROOT}", ".."],
                                ["{ENGINE}", self.engineNo],
                                ["{PUBBLY_JSON}", jsonData]
                            ]), end='')
            except:
                self.errors.append("Fatal: Constructing run files failed.")

            os.rename(self.stagePath + u + '/run.html', self.stagePath + u + '/' + u + '.html')


        
            # Copy run html to each unit'''
        '''
            
            try:
                shutil.copy(self.cwd + '/run.html', self.stagePath + u)
            except:
                self.errors.append("Fatal: Copying over run files failed.")

            # Grab the appropriate JSON file
            with open(self.jsonFiles[u], 'r') as someFile:
                jsonData = someFile.read()

            # Overwrite new run file with appropriate info
            try:
                with fileinput.FileInput(self.stagePath + u + "/run.html", inplace="True") as file:
                    for line in file:
                        print(strr.replaceAll(
                            line, [
                                ["{REL_ROOT}", ".."],
                                ["{ENGINE}", self.engineNo],
                                ["{PUBBLY_JSON}", jsonData]
                            ]), end='')
            except:
                self.errors.append("Fatal: Constructing run files failed.")'''

    def copyEngineShared(self):
        #try:
            #print(os.getcwd() + "/engine/" + self.engineNo)
            #print(self.stagePath)
        shutil.copytree(self.cwd + "/engine/", self.stagePath + "/engine")
        #except:
        #    self.errors.append("Fatal: Engine not found.")

    def getErrors(self):
        if (len(self.errors) is 0):
            print ("Success! File made at: DO THIS LATER LOL")
        else:
            print (str(len(self.errors)) + " errors found: ")
            for e in self.errors:
                print ("* " + e)

    def doTheThing(self):
        #self.checkIfEntryPointExists()
        #self.copyToStagingArea()
        self.checkJSONExistsNewerEngine()
        self.buildRunHTML()
        #self.copyEngineShared()
        self.getErrors()

    '''

    cwd = os.getcwd()
    for path, dirs, files in os.walk(cwd):
        print (path)
    '''

offObj = OfflineBundler("EpicQuest","latest.txt")
offObj.doTheThing()