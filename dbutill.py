import pymysql.cursors
def getConnection():
    connection = pymysql.connect(host='remotemysql.com',
                                 user='pF3IWeqcGm',
                                 password='NxesvVNzBj',
                                 database='pF3IWeqcGm',
                                 charset='utf8mb4',
                                 port=3306,
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

