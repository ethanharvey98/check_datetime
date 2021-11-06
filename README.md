# check_timestamp

### Tool to automatically check the timestamp of students' submitted files for CS15

    usage: check_timestamp.py [-h] [-d DATE] [-t TIME] [-p PATH]

    optional arguments:
      -h, --help            show this help message and exit
      -d DATE, --date DATE  Date in form of MM/DD e.g. 12/25
      -t TIME, --time TIME  Time in form of HH:MM e.g. 15:00
      -p PATH, --path PATH  Overrides student enviroment
      
Essentially, the program compares the timestamps of the students' submitted files with the duedate and duetime in assignments.conf
