#!/usr/bin/env python3
import os
import datetime
import re
import sys
import argparse
import pandas as pd

is_set       = os.environ.get("GRADING_ROOT")
GRADING_ROOT = is_set if is_set else os.path.join("/comp", "15", "grading")

class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


"""
This function takes an assignment and grading_root and returns the 
assignments duedate and duetime from assignments.conf
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
    if not assignment_found: 
        print("Error: Assignment could not be parsed from assignments.conf")
        exit(0)
    # return assignment duedate and duetime
    return assignment_duedate, assignment_duetime

def check_files(curr_dir, assignment_datetime):
    # initialize return value
    return_value = 0
    files = os.listdir(curr_dir)
    print("{0: <20}| Timestamp: {1}".format("Expected:", assignment_datetime))
    for file in files:
            # ignore hidden files
            if not (re.search("^\.", file)):
                file_date = datetime.datetime.fromtimestamp(os.path.getmtime(curr_dir + "/" + file))
                if (file_date > assignment_datetime):
                    return_value = 1
                    print("{0: <20}| Timestamp: {3} {1}Not OK!{2}".format(file, 
                                                                          colors.FAIL, 
                                                                          colors.ENDC, 
                                                                          file_date.strftime("%Y-%m-%d %H:%M:%S")))
                else:
                    print("{0: <20}| Timestamp: {1} {2}OK!{3}".format(file, 
                                                     file_date.strftime("%Y-%m-%d %H:%M:%S"),
                                                     colors.OKGREEN, 
                                                     colors.ENDC))
    return return_value


def get_final_datetime(duedate, duetime):
    try:
        if (len(duedate.split("/")) == 2):
            year = datetime.date.today().year
            return pd.to_datetime(str(year) + "/" + duedate + " " + duetime)
        else:
            return pd.to_datetime(duedate + " " + duetime)
    except Exception as e:
        print(e)
        exit(0)
    

def check_timestamp(assign, duedate, duetime, path):
    # initialize working directory
    DIRECTORY = os.getcwd() if path is None else path    

    # if no custom duedate and duetime were given
    if (duedate == None) and (duetime == None):
        assignment_duedate, assignment_duetime = parse_assignments(assign, GRADING_ROOT)
    else:
        assignment_duedate = duedate
        assignment_duetime = duetime

    # Concatenate duedate and duetime, convert to Timestamp object.
    assignment_datetime = get_final_datetime(assignment_duedate, assignment_duetime)

    # add 48 hours if duedate and duetime were not specified
    if (duedate == None and duetime == None):
        assignment_datetime = assignment_datetime + datetime.timedelta(days=2)
                    
    # compare student's files datetime to duedatetime
    return check_files(DIRECTORY, assignment_datetime)

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
        help="Overrides student environment"
    )
    args = parser.parse_args()

    # if date or time is given both are required
    if (args.date == None and args.time) or (args.date and args.time == None):
        parser.print_help()
        print("\nArguments '-d' and '-t' are mutually inclusive. You must specify both if you specify one.")
        exit(0)
    
    # Run it!
    exit(1) if check_timestamp(args.assign, args.date, args.time, args.path) else exit(0)

if __name__ == "__main__":
    # run main
    main()