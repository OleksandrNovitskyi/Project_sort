# Project_sort
sort emploee


The work of the program is designed for reading a CSV table with data on employees and cleaning it according to certain filters.
Input data:
1. CSV table with data on employees(! file name without spaces);
2. link to spreadsheets "black list"

Filters:
1. name or surname of the employee on the "black list". The "black list" is formed manually by HR and has three columns - First_name, Last_name and Forbidden word in position.
 The name of the employee is in column 24, the surname is in column 25. 
1.1 Filtering by partial name matching. If a part of the name is entered in the first column of the "black list" (case sensitive), such employees will be filtered out.
!!! Part of the name must contain three letters or more
2. Filtering by Forbidden word in position (column 43). List of the forbidden words is formed from third column of the "black list". 
3. the age and race of the employee are determined by the library ``` DeepFace``` using the photo from the profile (link in column 30). 
If link is missing - the person will be saved or deleted based on the value of the input parameter (save_pwa / del_pwa).
The face_filter function takes the link to a photo and is set to filter workers under age and races. Age and races can be replaced in the ---- INPUT PARAMETERS ----  by replacing the value of the variable '''limit_age''' and '''races'''
List of possible races - ['asian', 'indian', 'black', 'white', 'middle eastern', 'latino hispanic']

The result of the program isCSV file. Name of new file consist of the input file name + _filt. 
Exammple: input file - "MissouriSoftware_Tech_IT.csv"
          result files - "MissouriSoftware_Tech_IT_filt.csv"
        
                         
To check the program’s functionality, a test is written that checks the differences between the input and output files.

Soft requirements:
1. Python version 3.0 and higher. The installation is available here - https://www.python.org/downloads/
2. DeepFace library. The library installation is described here - https://github.com/serengil/deepface.

How to use:
In the terminal (command line) go to the folder with a program using the ```cd``` command and enter the command  ```python sort_names.py input_file_name.csv save_pwa```.
Example:
the saved folder is located at "C:\Users\NOS_HOME\Downloads\Project_sort".
run terminal (command line) - C:\Users\NOS_HOME>
go to the destination folder - C:\Users\NOS_HOME>cd Downloads\Project_sort
result - C:\Users\NOS_HOME\Downloads\Project_sort>
program execution - C:\Users\NOS_HOME\Downloads\Project_sort>python sort_names.py MissouriSoftware_Tech_IT.csv save_pwa

To stop program execution - press "Ctrl+C"
