import psycopg2
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "locallibrary.settings")
from django.conf import settings
print(settings)
#settings.configure()
# try:
#     #conn = psycopg2.connect(host="localhost",database="locallibrary", user="postgres", password="cwise",port='5432')
#     conn = psycopg2.connect(
#                     database = settings.DATABASES['default']['NAME'], 
#                     host = settings.DATABASES['default']['HOST'] or 'localhost', 
#                     port = settings.DATABASES['default']['PORT'] or '5432', 
#                     user = settings.DATABASES['default']['USER'], 
#                     password = settings.DATABASES['default']['PASSWORD'])
#     print ("Connecting to database %s successful...")
#     cur = conn.cursor()
#     print('PostgreSQL database version:')
#     cur.execute('SELECT version()')
#     
#     # display the PostgreSQL database server version
#     db_version = cur.fetchone()
#     print(db_version)
#     cur.close()
# except (Exception, psycopg2.DatabaseError) as error:
#     print(error)
# finally:
#     if conn is not None:
#         conn.close()
#         print('Database connection closed.')
#     # close the communication with the PostgreSQL