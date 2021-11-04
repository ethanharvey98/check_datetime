import os
import datetime
import re
import sys
import argparse

def check_timestamp(duedate, duetime, path):
    
    ASSIGNMENT = os.environ.get("HW")
    if (path == None): CURRENT_DIRECTORY = os.getcwd()
    else: CURRENT_DIRECTORY = path
    GRADING_ROOT = os.environ.get("GRADING_ROOT")
    
    return_value = 0
    files = os.listdir(CURRENT_DIRECTORY)
    
    # If no custom duedate and duetime were given
    if (duedate == None and duetime == None):
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
        assignment_duedate = ""
        assignment_duetime = ""
        for assignment in assignment_dictionary_array:
            if assignment["assign"] == ASSIGNMENT:
                assignment_duedate = assignment["duedate"]
                assignment_duetime = assignment["duetime"]
        if (assignment_duedate == ""):
            print("Error: Assignment duedate not found")
        if (assignment_duetime == ""):
            print("Error: Assignment duetime not found")
    else:
        assignment_duedate = duedate
        assignment_duetime = duetime
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
        # add 48 hours if duedate and duetime were not specified
        if (duedate == None and duetime == None):
            assignment_datetime = assignment_datetime + datetime.timedelta(days=2)
        for file in files:
            # ignore hidden files
            if not (re.search("^\.", file)):
                if (datetime.datetime.fromtimestamp(os.path.getmtime(CURRENT_DIRECTORY+file))>assignment_datetime):
                    return_value = 1
                    print("{} was modified after assignment deadline.".format(file))
    elif (len(assignment_duedate.split("/")) == 3):
        assignment_datetime = datetime.datetime(
            int(assignment_duedate.split("/")[2]),
            int(assignment_duedate.split("/")[0]),
            int(assignment_duedate.split("/")[1]),
            int(assignment_duetime.split(":")[0]),
            int(assignment_duetime.split(":")[1])
            )
        # add 48 hours if duedate and duetime were not specified
        if (duedate == None and duetime == None):
            assignment_datetime = assignment_datetime + datetime.timedelta(days=2)
        for file in files:
            # ignore hidden files
            if not (re.search("^\.", file)):
                if (datetime.datetime.fromtimestamp(os.path.getmtime(CURRENT_DIRECTORY+file))>assignment_datetime):
                    return_value = 1
                    print("{} was modified after assignment deadline.".format(file))

    return return_value

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d',
        '--date',
        dest='date',
        required='--time' in sys.argv,
        help='Date in form of MM/DD e.g. 12/25'
    )
    parser.add_argument(
        '-t',
        '--time',
        dest='time',
        required='--date' in sys.argv,
        help='Time in form of HH:MM e.g. 15:00'
    )
    parser.add_argument(
        '-p',
        '--path',
        dest='path',
        help='Overrides student enviroment'
    )
    args = parser.parse_args()
            
    if (args.date == None and args.time) or (args.date and args.time == None):
        print('\nusage: check_timestamp.py [-h] [-d DATE] [-t TIME] [-p PATH]')
        sys.exit(2)
        
    check_timestamp(args.date, args.time, args.path)

if __name__ == "__main__":
    
    main()