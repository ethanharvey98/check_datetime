# check_timestamp

### Tool to automatically check the timestamp of students' submitted files for CS15

    usage: check_timestamp [-h] [-d DUEDATE & -t DUETIME] [-u UTLN]

    optional arguments:
      -h, --help            Show this help message and exit
      --duedate DUEDATE     Date in form of MM/DD e.g. 12/25
      --duetime DUETIME     Time in form of HH:MM e.g. 15:00
      --utln UTLN           Overrides student enviroment
      
Essentially, the program compares the timestamps of the students' submitted files with the due date and time in assignments.conf
