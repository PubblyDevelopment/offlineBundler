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
        self.targetPath = os.getcwd() + "/map/" + mn
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
            print(self.stagePath + u)
            shutil.copy('run.html', self.stagePath + u)

            '''
            with fileinput.FileInput("run.html", inplace="True") as file:
                for line in file:
                    print ("please do something :)")
                    print(strr.replaceAll(
                        line, [
                            ["{REL_ROOT}", "."],
                            ["{ENGINE}", self.engineNo]
                        ]))
            '''

            #self.jsonFiles[u]

        # Replace some shiittttttt
        '''
        with fileinput.FileInput("practice.html", inplace="True", backup='.bak') as file:
            for line in file:
                # line is "asdf {REL_ROOT} {ENGINE}"
                line = strr.replaceAll(
                    line, [
                        ["{REL_ROOT}","."],
                        ["{ENGINE}", self.engineNo]
                        #["podfgdsfgop", "dfgsdfgsdfpoop"]

                    ])

        print (self.unitJSON)
        '''

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
        self.getErrors()

    '''

    cwd = os.getcwd()
    for path, dirs, files in os.walk(cwd):
        print (path)
    '''

offObj = OfflineBundler("test","latest.txt")
offObj.doTheThing()