#This file contains comparison functions for student submissions. The prototype for such functions should always be:
#def myfunc(studentFileName,solnFileName,AdditionalData)
#This function should always return a string summarizing the comparison result
#Additional data is a structure which contains any additional data needed to comapre the two files
import string

def Assignment1_2013_CMP_GenData(studentFileName,solnFileName,additionalData = None):
    result = ''
    solnFile = open(solnFileName)
    solnFileLines = solnFile.readlines()
    solnFile.close()
    studentSolnFile = open(studentFileName)
    studentSolnFileLines = studentSolnFile.readlines()
    studentSolnFile.close();
    #Check if the solution and generated data have the same number of lines
    result += 'Checking the number of lines...'
    if len(studentSolnFileLines) == len(solnFileLines):
        result += 'OK\n'
        for i in range(len(studentSolnFileLines)):
            result += 'Checking output line %d...' %i
            studentNumVal = float(string.split(studentSolnFileLines[i])[-1])
            solnNumVal    = float(string.split(solnFileLines[i])[-1])
            if abs(studentNumVal - solnNumVal)/abs(solnNumVal) < 0.1:
                result += 'OK\n'
            else:
                result += 'Failed. Student:%.6f Soln:%.6f\n' %(studentNumVal,solnNumVal)
    else:
        result += 'Failed\n'
    return result

    
def Assignment1_2013_CMP_ProccData(studentFileName,solnFileName,additionalData = None):
    result = ''
    solnFile = open(solnFileName)
    solnFileLines = solnFile.readlines()
    solnFile.close()
    studentSolnFile = open(studentFileName)
    studentSolnFileLines = studentSolnFile.readlines()
    studentSolnFile.close();
    #Check if the solution and generated data have the same number of lines
    result += 'Checking the number of lines...'
    if len(studentSolnFileLines) == len(solnFileLines):
        result += 'OK\n'
        for i in range(len(studentSolnFileLines)):

            result += 'Checking output line %d...' %i
            studentNumVal = float(string.split(studentSolnFileLines[i])[-1])
            solnNumVal    = float(string.split(solnFileLines[i])[-1])
            if i == len(studentSolnFileLines) - 1:
                if studentNumVal < solnNumVal or abs(studentNumVal - solnNumVal)/abs(solnNumVal) < 3:
                    result += 'OK\n'
                else:
                    result += 'Failed. Student:%.6f Soln:%.6f\n' %(studentNumVal,solnNumVal)

            else:
                if abs(studentNumVal - solnNumVal)/abs(solnNumVal) < 0.1:
                    result += 'OK\n'
                else:
                    result += 'Failed. Student:%.6f Soln:%.6f\n' %(studentNumVal,solnNumVal)
    else:
        result += 'Failed\n'
    return result


def Assignment1_2014_CMP_NumLines(studentFileName,solnFileName,additionalData = None):

    f = open(studentFileName);
    lineCnt = 0;
    for line in f:
        if string.find(line,"Python") == 0:
            lineCnt = int(string.split(line)[4])
            break;
    if lineCnt == 0:
        return "Error! No Python file.\n"
    result = ""
    if lineCnt <= 100:
        result = "Number of lines = %d . Bellow limit.\n" % lineCnt
    elif lineCnt <=125:
        result = "Number of lines = %d . Above limit - 2." % lineCnt
    elif lineCnt <=150:
        result = "Number of lines = %d . Above limit - 4." % lineCnt
    elif lineCnt <=175:
        result = "Number of lines = %d . Above limit - 6." % lineCnt
    else:
        result = "Number of lines = %d . Above limit - 8." % lineCnt
    
    return result


def Assignment1_2014_CMP_ORF(studentFileName,solnFileName,additionalData = None):
    
    f_student = open(studentFileName)
    f_soln = open(solnFileName)
    studentLines = f_student.readlines();
    if len(studentLines) == 0:
        return "Error! File is empty.\n"
    solnLines = f_soln.readlines();
    studentHeader = studentLines[0];
    result = ""
    if string.find(studentHeader,'S288C_reference_sequence_R64-1-1_20110203.fsa') < 0:
        result += "File does not include correct file name in the header.\n"
    match = True
    for i in range(len(solnLines)):
        if i >= len(studentLines):
            result += "Student file has %d lines while solution has %d lines.\n" %(len(studentLines),len(solnLines))
            break;
        if solnLines[i][0] != '>':
            if studentLines[i][0] != '>':
                solnSpec = string.split(solnLines[i]);
                studentSpec = string.split(studentLines[i]);
                if len(solnSpec) != len(studentSpec):
                    match = False;
                    break;
                error = 0.
                for j in range(len(solnSpec)):
                    if studentSpec[j].isdigit():
                        error += int(solnSpec[j]) - int(studentSpec[j])
                    else:
                        match = False;
                        break
                if abs(error) > 1e-10:
                    match = False
                    break;
            else:
                match = False
                break;
    
    if match == False:
        result += "NO MATCH.\n"
    else:
        result += "MATCH.\n"
    return result

