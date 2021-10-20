import os
import datetime
import re

def check_timestamp(duedate=None, duetime=None, utln=None):

    EXIT = 0
    #ASSIGNMENT = os.environ.get("HW")
    ASSIGNMENT = "hw2_MetroSim"
    #UTLN = os.environ.get("STUDENT")
    UTLN = "/Users/ethanharvey/Desktop/check_timestamp/"
    #GRADING_ROOT = os.environ.get("GRADING_ROOT")
    GRADING_ROOT = "/Users/ethanharvey/Desktop/check_timestamp/grading"

    files = os.listdir(UTLN)
    file1 = open(GRADING_ROOT+"/assignments.conf", "r")
    lines = file1.readlines()
    
    continued_line = False
    assignment_to_add = ""
    assignment_string_array = []
    # parse assignments.conf
    for line in lines:
        if not ((re.search("^#", line)) or (re.search("^\n", line))):
            if (re.search("\\\\\\n", line)):
                continued_line = True
                assignment_to_add = assignment_to_add + line
            else:
                continued_line = False
                assignment_to_add = assignment_to_add + line
            if not (continued_line):
                assignment_string_array.append(assignment_to_add)
                assignment_to_add = ""
    # create a dictionary for each assignment
    assignment_dictionary_array = []
    for assignment in assignment_string_array:
        assignment = assignment.replace("\\", " ")
        param_dictionary = {}
        for param in assignment.split():
            param_dictionary[param.split("=")[0]]=param.split("=")[1]
        assignment_dictionary_array.append(param_dictionary)
    # find the assignment duedate
    for assignment in assignment_dictionary_array:
        if assignment["assign"] == ASSIGNMENT:
            assignment_duedate = assignment["duedate"]
            assignment_duetime = assignment["duetime"]
    # compare student's files datetime to duedatetime
    year = datetime.date.today().year
    if (len(assignment_duedate.split("/")) == 2):
        assignment_datetime = datetime.datetime(
            year,
            int(assignment_duedate.split("/")[0]),
            int(assignment_duedate.split("/")[1]),
            int(assignment_duetime.split(":")[0]),
            int(assignment_duetime.split(":")[1])
            )
        for file in files:
            if (datetime.datetime.fromtimestamp(os.path.getmtime(UTLN+file))>assignment_datetime):
                EXIT = 1
                print("{} was modified after assignment deadline.".format(file))
    elif (len(assignment_duedate.split("/")) == 3):
        assignment_datetime = datetime.datetime(
            int(assignment_duedate.split("/")[2]),
            int(assignment_duedate.split("/")[0]),
            int(assignment_duedate.split("/")[1]),
            int(assignment_duetime.split(":")[0]),
            int(assignment_duetime.split(":")[1])
            )
        for file in files:
            if (datetime.datetime.fromtimestamp(os.path.getmtime(UTLN+file))>assignment_datetime):
                EXIT = 1
                print("{} was modified after assignment deadline.".format(file))

    return EXIT
        
print(check_timestamp())
