import os
import datetime
import re
import sys
import argparse

"""
This function takes an assignement and grading_root and returns the 
assignements duedate and duetime from assignments.conf
"""
def parse_assignments(assign, GRADING_ROOT):
    # open assignments.conf
    assignments_file = open(GRADING_ROOT+"/assignments.conf", "r")
    lines = assignments_file.readlines()
    assignments_file.close()
    # parse assignments.conf
    continued_line = False
    assignment_to_add = ""
    assignment_string_array = []
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
    assignment_duedate = None
    assignment_duetime = None
    assignment_found = False
    for assignment_dictionary in assignment_dictionary_array:
        if assignment_dictionary["assign"] == assign:
            assignment_found = True
            try: assignment_duedate = assignment_dictionary["duedate"]
            except: print("Error: Assignment duedate not found")
            try: assignment_duetime = assignment_dictionary["duetime"]
            except: print("Error: Assignment duetime not found")
    # print errors if assignment not found
    if not assignment_found: print("Error: Assignment not found")
    # return assignment duedate and duetime
    return assignment_duedate, assignment_duetime

def check_timestamp(assign, duedate, duetime, path):
    # initialize CURRENT_DIRECTORY and GRADING_ROOT
    if (path == None): CURRENT_DIRECTORY = os.getcwd()
    else: CURRENT_DIRECTORY = path
    #GRADING_ROOT = os.environ.get("GRADING_ROOT")
    GRADING_ROOT = "/comp/15/grading"

    # initialize return value
    return_value = 0
    files = os.listdir(CURRENT_DIRECTORY)
    # if no custom duedate and duetime were given
    if (duedate == None) and (duetime == None):
        assignment_duedate, assignment_duetime = parse_assignments(assign, GRADING_ROOT)
    else:
        assignment_duedate = duedate
        assignment_duetime = duetime
    if (not assignment_duedate == None) and (not assignment_duetime == None):
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
                    if (datetime.datetime.fromtimestamp(os.path.getmtime(CURRENT_DIRECTORY+"/"+file))>assignment_datetime):
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
                    if (datetime.datetime.fromtimestamp(os.path.getmtime(CURRENT_DIRECTORY+"/"+file))>assignment_datetime):
                        return_value = 1
                        print("{} was modified after assignment deadline.".format(file))

    return return_value

def main():
    # python library argparse
    parser = argparse.ArgumentParser()
    requiredArgs = parser.add_argument_group('required arguments')
    requiredArgs.add_argument(
        "-a",
        dest="assign",
        required=True,
        help="Assignment name e.g. hw1"
    )
    parser.add_argument(
        "-d",
        "--date",
        dest="date",
        required="--time" in sys.argv,
        help="Date in form of MM/DD e.g. 12/25"
    )
    parser.add_argument(
        "-t",
        "--time",
        dest="time",
        required="--date" in sys.argv,
        help="Time in form of HH:MM e.g. 15:00"
    )
    parser.add_argument(
        "-p",
        "--path",
        dest="path",
        help="Overrides student enviroment"
    )
    args = parser.parse_args()
    # if date or time is given both are required
    if (args.date == None and args.time) or (args.date and args.time == None):
        print("\nusage: check_timestamp.py [-h] -a ASSIGN [-d DATE] [-t TIME] [-p PATH]")
        sys.exit(2)
    check_timestamp(args.assign, args.date, args.time, args.path)

if __name__ == "__main__":
    # run main
    main()