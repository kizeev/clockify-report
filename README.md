Script for creating a report from Clockify in `.docx` file.

Steps:
1. install dependencies from the `requirements.txt`
2. generate API-token in the personal account of Clockify
3. create `local_config.py` file in the directory with the script and fill in the data:
	```python
	API_TOKEN: str = ''
	HOURLY_RATE: float = 0
	SENDER_NAME: str = ''  # Name Surname
	LOCALE: str = ''  # like 'de_DE'
	VACATION_TEXT = ''  # like 'Support spiders'
    # default args
    GROUP_BY_DAYS = False
    CONVERT_TO_USD = False
    ADD_GERMAN_LANGUAGE = False
    ADD_VACATION = False
    ADD_EXTRA_EXPENSES_PREMIUMS = False
	```
4. in the `template.docx` file, fill in the fields highlighted in green and turn off the highlighting
5. run the script with parameters from the command line where:
	- required parameters:
	    - `-y` - the year of the report;
	    - `-m` - the month of the report;
	- additional parameters:
	    - `-g` - group by tasks by day. By default, grouping by month;
	    - `-usd` - convert total price to USD. Keep in mind that the conversion works for the last 30 days;
	    - `-de` - add German language to report;
	    - `-v` - add a vacation. User input will be required;
	    - `-e` - add extra expenses/premiums.  User input will be required;
	```bash
	python -m main -y 2023 -m 12
	```
6. check the result in the `path_to_script/output/` directory and edit it if necessary.

