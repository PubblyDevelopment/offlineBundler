import glob
from pathlib import Path
import os
import shutil
from shutil import *
import fileinput
import strreplace as strr

class OfflineBundler:
    def __init__(self, mn, en):
        self.mapName = mn
        self.errors = []
        self.cwd = os.getcwd()
        self.targetPath = self.cwd + "/map/" + mn
        self.engineNo = open(en,"r").read()

    def checkIfEntryPointExists(self):
        if not os.path.isfile(self.targetPath + "/entryPoint.txt"):
            self.errors.append("Fatal: Entry point doesn't exist or isn't correctly formatted. Looking for \"entryPoint.txt\"");
        else:
            self.entryPoint = open(self.targetPath + "/entryPoint.txt", "r").read()

    def copyToStagingArea(self):
        print ()
        if not os.path.exists("stagingArea"):
            try:
                shutil.copytree(self.targetPath, self.targetPath+ "/stagingArea", ignore=ignore_patterns("entryPoint.*", "test.py"))
            except:
                self.errors.append("Fatal: Copy of node folders failed for some reason.")
        else:
            self.errors.append("Fatal: Old staging area folder already exists.")

    def checkJSONExistsNewerEngine(self):
        self.units = next(os.walk(self.targetPath))[1]
        self.units.remove("stagingArea")

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
                            self.errors.append("Fatal: Using wrong engine. This file appears to be " + version + ".")
                    except:
                        self.errors.append("Fatal: Something went wrong. Missing JSON, maybe?")

                if "MainXML" in f:
                    unitXML = self.stagePath + u + "/" + f

            if not unitJSON:
                self.errors.append("Fatal: JSON file missing at " + self.stagePath + u)
                break;
            if not unitXML:
                self.errors.append("Fatal: XML file missing at " + self.stagePath + u)
                break;

            if self.isNewer(unitJSON, unitXML):
                self.errors.append("Warning: JSON outdated at " + u)


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
        for u in self.units:

            # Copy run html to each unit
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
                self.errors.append("Fatal: Constructing run files failed.")

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
            print ("Errors found: ")
            for e in self.errors:
                print ("* " + e)

    def doTheThing(self):
        #self.checkIfEntryPointExists()
        #self.copyToStagingArea()
        self.checkJSONExistsNewerEngine()
        self.buildRunHTML()
        self.copyEngineShared()
        self.getErrors()

    '''

    cwd = os.getcwd()
    for path, dirs, files in os.walk(cwd):
        print (path)
    '''

offObj = OfflineBundler("test","latest.txt")
offObj.doTheThing()