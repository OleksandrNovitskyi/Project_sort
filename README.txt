# Project_sort
sort emploee


The work of the program is designed for reading a CSV table with data on employees and sorting it according to certain filters.
Input data:
1. CSV table with data on employees(! file name without spaces);
2. link to spreadsheets "black list"

Filters:
1. name, surname or forbidden position of the employee on the "black list". The "black list" is formed manually by HR and has three columns - First_name, Last_name and Forbidden word in position.
 The name of the employee is in column 24, the surname is in column 25, the forbidden position is in column 43. 
1.1 Filtering by partial name matching. If a part of the name is entered in the first column of the "black list" (case sensitive), such employees will be filtered out.
!!! Part of the name must contain three letters or more.
1.2 Filtering by last name assumes a complete match.
1.3 Filtering by position requires the presence of at least one forbidden word in the position.
2. The age and race of the employee are determined by the library ``` DeepFace``` using the photo from the profile (link in column 30). 
If link is missing - the person will be saved or deleted based on the value of variable 'DEL_PEOPLE_WITHOUT_AVATAR' in the block ---- INPUT PARAMETERS ----. Value may be 'True' or 'False'
The face_filter function takes the link to a photo and is set to filter workers under age and races. Age and races can be replaced in the ---- INPUT PARAMETERS ----  by replacing the value of the variable '''LIMIT_AGE''' and '''races'''
List of possible races - ['asian', 'indian', 'black', 'white', 'middle eastern', 'latino hispanic']

The result of the program is two CSV files. Name of the first new file consist of the input file name + _filt and second - of the input file name + _deleted. 
Exammple: input file - "MissouriSoftware_Tech_IT.csv"
          result files - "MissouriSoftware_Tech_IT_filt.csv" and "MissouriSoftware_Tech_IT_deleted.csv"
        
                         
To check the program’s functionality, a test is written that checks the differences between the input and first output files.

Soft requirements:
1. Python version 3.0 and higher. The installation is available here - https://www.python.org/downloads/
2. DeepFace library. The library installation is described here - https://github.com/serengil/deepface.

How to use:
In the terminal (command line) go to the folder with a program using the ```cd``` command and enter the command  ```python sort_names.py input_file_name.csv```.
Example:
the saved folder is located at "C:\Users\NOS_HOME\Downloads\Project_sort".
run terminal (command line) - C:\Users\NOS_HOME>
go to the destination folder - C:\Users\NOS_HOME>cd Downloads\Project_sort
result - C:\Users\NOS_HOME\Downloads\Project_sort>
program execution - C:\Users\NOS_HOME\Downloads\Project_sort>python sort_names.py MissouriSoftware_Tech_IT.csv

To stop program execution - press "Ctrl+C"
