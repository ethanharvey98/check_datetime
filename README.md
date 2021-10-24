# check_timestamp

### Tool to automatically check the timestamp of students' submitted files for CS15

    usage: check_timestamp [-h] [-d DUEDATE & -t DUETIME] [-p PATH]

    optional arguments:
      -h, --help                Show this help message and exit
      -d, --duedate DUEDATE     Date in form of MM/DD e.g. 12/25
      -t, --duetime DUETIME     Time in form of HH:MM e.g. 15:00
      -p, --path PATH           Overrides student enviroment
      
Essentially, the program compares the timestamps of the students' submitted files with the duedate and duetime in assignments.conf
