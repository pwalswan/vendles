The project contains six files: this readme, two python files, a data input
file, a database DDL file, and a configuration file (etl.properties)

Using PyCharm, I was able to use the File>Open to pick the pythonproject
to have all dependencies work, and to be able to run the program.

1. Setup script to create the database.
I created a Postgres database in Azure for development. I did not create the
database locally, so if it pleases the court I recommend running the DDL
statements in the on an existing postgres database that you have access to,
or you can log in to my Azure postgres database. I will need to whitelist your
ip address for a firewall rule if so. If you use your own postgres database
you will need to update the etl.properties file with your connection profile.
The database DDL file creates tables, and imports the UUID module. I did not
create foreign keys, and opted for a string column instead of boolean for
boolean values for simplicity.

2. Application that performs specific operations
There are two py files to make up the application. The application merely loads
the data into the database to support the query requirement specifications.
It is not a robust API to support insert, update or delete operations.
I don't have a build project file (i.e. maven), so you should be able to create
a new project with those two files. I developed in Python 3.8.

3. Test plan, test data and how you would automate testing
I did not include a test suite due to time. The execution of the Application
will process the data from the input.json file and ingest into the database.
You will find the queries to support the requirements at the end of The
database DDL file. I would need to explore a test framework for python, such
as junit or testng used in Java. The queries in the requirement specifications
could be used as tests, to make sure the data come back as expected, and to
test the data modeling extracted from the JSON. My process is not idempotent
unfortunately, so the data will have to be deleted from each table, or the
tables will need to be dropped and recreated for a subsequent test. Apologies.
