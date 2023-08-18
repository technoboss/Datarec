from dotenv import dotenv_values

secrets = dotenv_values('.env')

API_KEY = secrets['API_KEY']
DB_PASSWORD = secrets['DB_PASSWORD']


# ----------------------------------------------------------------
# import os 
# with open('.env','r') as file:
#     line = file.readline()
#     os.environ[line[:line.find('=')]] = line[line.find('=') + 1]
# -----------------------------------------------------------------
# print(os.environ)    # print all the environment variable
# print(os.environ['JAVA_HOME']) # print specific env variable
# print(os.environ.get('JAVA_HOME', 'NO JAVEHOME)) # Error handling
