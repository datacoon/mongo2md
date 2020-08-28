# Natural monopolies database example

Follow steps:
1. Install "mongo2md" via pip installation or with command "python setup.py install"
2. Restore collection "naturalmon". Use "mongorestore" command in "naturalmon" directory. It should restore naturalmon collection
3. Run "mongo2md prepare -o  examples/naturalmon fas naturalmon" 
4. Edit file "tables.csv", add displayName and description of the table
5. Edit file "naturalmon_fields.csv" and add description for each field 
6. Run "mongo2md document examples/naturalmon" 
7. Review "markdown/tables.md" file
