import cmpFunc
import shutil
import string
import subprocess
import sys
import threading
import time
import os

    
# subprocess command run with timeout support
class Command(object):
    def __init__(self,cmd):
        self.cmd = cmd
        self.process = None

    def run(self,cwd_,timeout):
        def target():
            self.process = subprocess.Popen(self.cmd,cwd=cwd_,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            self.out,self.err = self.process.communicate()

        thread = threading.Thread(target=target)
        thread.start()

        thread.join(timeout)
        if thread.is_alive():
            self.process.terminate()
            thread.join()
            self.err = 'TIMEOUT'
        return self.out,self.err
    
def findInputInConfigFile(configFileLines,inputLabel):
    for line in configFileLines:
        if string.find(line,inputLabel) >= 0:
            startIdx = string.find(line,'"')
            endIdx   = string.rfind(line,'"')
            if startIdx < 0 or endIdx < 0:
                print 'Error! Incorrect config file format.'
                sys.exit()
            input = line[startIdx+1:endIdx]
            if len(input) > 0:
                return input
            return -1
    return -1

def checkRequiredInput(configFileLines,inputLabel):
    chk = findInputInConfigFile(configFileLines,inputLabel)
    if chk == -1:
        print 'Error! Input label %s not found in config file.' %inputLabel 
        sys.exit()
    return chk

def getCmndList(configFileLines,inputLabel,IOLabel,requiredIO = False):
    result = {}
    cnt    = 1;
    cmndStr = "%s_%d" %(inputLabel,cnt)
    cmnd = findInputInConfigFile(configFileLines,cmndStr)
    while cmnd != -1:
        cmndIOStr = "%s_%s" %(cmndStr,IOLabel)
        cmndIO    = findInputInConfigFile(configFileLines,cmndIOStr)
        if cmndIO == -1:
            if requiredIO == False:
                cmndIO = ""
            else:
                print 'Error! Config file missing required input/output file name for a command.'
                sys.exit()
        result[cmnd +'_'+str(cnt)] = cmndIO
        cnt += 1
        cmndStr = "%s_%d"%(inputLabel,cnt)
        cmnd = findInputInConfigFile(configFileLines,cmndStr)
    
    if len(result) == 0:
        print 'Error! No specified input for %s in config file.' %inputLabel
        sys.exit()
    return result

currDir = os.getcwd()
configFilePath = ''
configFileName = ''

# Retrive the path of the config file
if (len(sys.argv) == 1):
    configFileName = 'config.in'
    configFilePath = currDir + '/' + configFileName
    if (os.path.isfile(configFilePath) == False):
        print 'Error! No such config file exists'
        sys.exit()
elif (len(sys.argv) == 2):
    configFilePath = sys.argv[1]
    if (os.path.isfile(configFilePath) == False):
        print 'Error! No such config file exists'
        sys.exit()
    configFileName = configFilePath[string.rfind(configFilePath,'/') + 1:]
else:
    print 'Usage: python autoGrade.py <Uses the default config.in file as input>'
    print '       python autoGRade.py path/to/config/file <Uses the config file specified by path>'
    sys.exit()

# Open and process the config file
print 'Loading configuration parameters from input config file...',
sys.stdout.flush()

configFile = open(configFilePath)
configFileLines = configFile.readlines()

studentsRootDir = checkRequiredInput(configFileLines,'STUDENTS_ROOT_DIR')
assignmentDir   = checkRequiredInput(configFileLines,'ASSIGNMENT_DIR')
solutionDir     = checkRequiredInput(configFileLines,'SOLUTION_DIR')
outputDir       = checkRequiredInput(configFileLines,'OUTPUT_DIR')
buildDir        = checkRequiredInput(configFileLines,'BUILD_DIR')

execCommandsDict = getCmndList(configFileLines,'EXEC_COMMAND','OUT')
cmpCommandsDict  = getCmndList(configFileLines,'CMP_COMMAND','FILE',True)
timeOutParamDict = getCmndList(configFileLines,'EXEC_COMMAND','TIMEOUT',True)

print 'done'

# Loop through the students repo folder and find a list of students
print 'Generating a list of students...',
sys.stdout.flush()
studentList = []
for root,dirs,fileNames in os.walk(studentsRootDir):
    for dir in dirs:
        currDirPath = os.path.join(root,dir)
        if string.find(currDirPath,assignmentDir) >= 0:
            endIdx   = string.find(currDirPath,assignmentDir)
            startIdx = string.rfind(currDirPath,'/',0,endIdx - 1)
            studentList.append(currDirPath[startIdx + 1:endIdx - 1])


if len(studentList) == 0:
    print 'Error! No student folder found. Check the STUDENTS_ROOT_DIR and ASSIGNMENT_DIR variables in the config file.'
    sys.exit()
print 'done'

# Check if the build directory exists and create a new empty directory
if (os.path.exists(buildDir)):
    shutil.rmtree(buildDir)
os.makedirs(buildDir)

# Now loop through all the students and copy the submissions to the build directory
print 'Copying student submissions into the build directory...',
sys.stdout.flush()

for student in studentList:
    submissionDirPath = '%s/%s/%s' %(studentsRootDir,student,assignmentDir);
    buildDirPath      = '%s/%s' %(buildDir,student)
    shutil.copytree(submissionDirPath,buildDirPath)
print 'done'

print 'Copying solution into the build directory...',
solnBuildDirPath = '%s/%s' %(buildDir,'Solution')
shutil.copytree(solutionDir,solnBuildDirPath);
print 'done'

# Now execute the commands on the solution file
print 'Running EXEC commands on solution files...',
sys.stdout.flush()

timeOutDict = {}
for cmd in execCommandsDict:
    cmd_ = cmd[:string.rfind(cmd,'_')]
    start = time.time()
    p = subprocess.Popen(string.split(cmd_),cwd=solnBuildDirPath,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p.wait();
    end = time.time()
    timeOutDict[cmd] = end - start;
    out, err = p.communicate()
    if len(execCommandsDict[cmd]) > 0:
        f = open('%s/%s' %(solnBuildDirPath,execCommandsDict[cmd]),'w')
        f.write(out)
        f.close()
    #print timeOutDict
print 'done'

# Check if the build directory exists and create a new empty directory
if (os.path.exists(outputDir)):
    shutil.rmtree(outputDir)
os.makedirs(outputDir)

# Now loop through the students and execute the required commands
print 'Running EXEC commands on student submissions...',
sys.stdout.flush()

buildFile = open('%s/%s' %(outputDir,'buildSummary.log'),'w')
buildFile.write('Build summary for %s \n'%assignmentDir)

for student in studentList:
    buildFile.write('-------------------------------------\n');
    buildFile.write('Student ID = %s\n'%student)
    for cmd in execCommandsDict:
        cmd_ = cmd[:string.rfind(cmd,'_')]
        buildFile.write('************************\n')
        buildFile.write('\t%s\n'%cmd_)
        testDirPath = '%s/%s' %(buildDir,student)
        currCmd = Command(string.split(cmd_));
        out,err = currCmd.run(testDirPath,float(timeOutParamDict[cmd]) * timeOutDict[cmd])
        if (len(execCommandsDict[cmd]) > 0):
            f = open('%s/%s' %(testDirPath,execCommandsDict[cmd]),'w')
            f.write(out)
            f.close()
        buildFile.write('\tError:\n')
        buildFile.write('\t\t%s\n'%err)
        buildFile.write('\tOut:\n')
        buildFile.write('\t\t%s\n'%out.replace('\n','\n\t\t'))
buildFile.close()
print 'done'
print 'Build summary written to buildSummary.log'

# Now Start the comparison between the solutoin and the submission
    
print 'Running CMP commands on student submissions...',
sys.stdout.flush()

cmpFile = open('%s/%s' %(outputDir,'comparisonSummary.log'),'w')
cmpFile.write('Comparison summary for %s \n'%assignmentDir)

for student in studentList:
    cmpFile.write('-------------------------------------\n');
    cmpFile.write('Student ID = %s\n'%student)
    for cmd in cmpCommandsDict:
        cmd_ = cmd[:string.rfind(cmd,'_')]
        cmpFile.write('************************\n')
        cmpFile.write('\t%s\n'%cmd_)
        studentSolnFilePath = '%s/%s/%s' %(buildDir,student,cmpCommandsDict[cmd])
        solnFilePath        = '%s/%s'    %(solnBuildDirPath,cmpCommandsDict[cmd])
        # check if student file exists
        cmpResult = ''
        if os.path.isfile(studentSolnFilePath):
            cmpResult = getattr(cmpFunc,cmd_)(studentSolnFilePath,solnFilePath);
        else:    
            cmpResult = 'FAIL. Student file does not exist.\n'
        cmpFile.write("\t\t%s\n"%cmpResult.replace('\n','\n\t\t'))

cmpFile.close()
print 'done'
print 'Build summary written to comparisonSummary.log'
