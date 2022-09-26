# Project_sort
sort emploee

The work of the program is designed for reading a CSV table with data on employees and cleaning it according to certain filters.
Filters:
1. name or surname of the employee on the "black list". The "black list" is formed manually by HR and has two columns - First_name and Last_name. The name of the employee is in column 24, the surname is in column 25.
2. there is the word "NFT" in the employee's position (column 43). The word can be replaced in the text of the ``get_short_list'' function by replacing the value of the variable '''forbidden_word'''
3. the age and race of the employee are determined by the library ``` DeepFace``` using the photo from the profile (link in column 30). 
The face_filter function takes the link to a photo and is set to filter workers under 25 and non-Europoid workers.
To change age and race, set two additional input parameters when calling the function
'''face_filter(row[30])''' (line 21) for example '''face_filter(row[30], 35, 'asian')'',
where 35 is the new age limit, 'asian' is the mongoloid race.
List of possible races - ['asian', 'indian', 'black', 'white', 'middle eastern', 'latino hispanic']

The result of the program is the result.csv file

To check the program’s functionality, a test is written that checks the differences between the input and output files.

Soft requirements:
1. Python version 3.0 and higher. The installation is available here - https://www.python.org/downloads/
2. DeepFace library. The library installation is described here - https://github.com/serengil/deepface.

In the terminal (command line) go to the folder with a program using the ```cd``` command and enter the command  ```python sort_names.py```.
Example:
the saved folder is located at "C:\Users\NOS_HOME\Downloads\Project_sort".
run terminal (command line) - C:\Users\NOS_HOME>
go to the destination folder - C:\Users\NOS_HOME>cd Downloads\Project_sort
result - C:\Users\NOS_HOME\Downloads\Project_sort>
program execution - C:\Users\NOS_HOME\Downloads\Project_sort>python sort_names.py

