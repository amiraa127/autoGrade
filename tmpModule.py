def cmpFunc(studentFileName,solnFileName,additionalData = None):
    import string
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
