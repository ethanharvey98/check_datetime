# check_timestamp

### Tool to automatically check the timestamp of students' submitted files for CS15

    usage: check_timestamp [-d DUEDATE & -t DUETIME] [-u UTLN]

    optional arguments:
      --duedate DUEDATE     Overrides assignement due date
      --duetime DUETIME     Overrides assignement due time
      --utln UTLN           Overrides student enviroment
      
Essentially, the program compares the timestamps of the students' submitted files with the due date and time in assignments.conf
