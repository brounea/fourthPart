import dbutill
from datetime import date

#############################################
def create_tbl():
    connection = dbutill.getConnection()
    sql_tbl = "create table IF NOT EXISTS users (user_id int not null primary key,user_name varchar(45) not null,creation_date varchar(50))"
    try:
        cursor = connection.cursor()
        cursor.execute(sql_tbl)
    finally:
        # Close connection.
        connection.close()

#############################################
def user_exist(id):
    exist = False
    connection = dbutill.getConnection()
    try:
        cursor = connection.cursor()
        sql_sel = "SELECT user_name FROM pF3IWeqcGm.users WHERE user_id= %s "
        cursor.execute(sql_sel, id)
        if cursor.fetchone() is not None:
            exist = True
    finally:
        # Close connection.
        connection.close()
        return exist

#############################################
def user_create(user_id,user_name):
    if not user_exist(user_id):
        connection = dbutill.getConnection()
        try:
            cursor = connection.cursor()
            sql_ins = "insert into pF3IWeqcGm.users (user_id,user_name,creation_date) values (%s, %s, %s )"
            cursor.execute(sql_ins, (user_id,user_name,date.today()))
            connection.commit()
        finally:
            # Close connection.
            connection.close()
            return True
    else:
        return False
#############################################
def user_update(user_id,user_name):
    if user_exist(user_id):
        connection = dbutill.getConnection()
        try:
            cursor = connection.cursor()
            sql_ins = "update pF3IWeqcGm.users SET user_name = %s where user_id = %s "
            cursor.execute(sql_ins, (user_name,user_id))
            connection.commit()
        finally:
            # Close connection.
            connection.close()
            return True
    else:
        return False

#############################################
def get_user_name(id):
    connection = dbutill.getConnection()
    name = ''
    try:
        cursor = connection.cursor()
        sql_sel = "SELECT user_name FROM pF3IWeqcGm.users WHERE user_id= %s "
        cursor.execute(sql_sel, id)
        dataset = cursor.fetchone()
        name = dataset['user_name']
    finally:
        # Close connection.
        connection.close()
        return name
#############################################
def user_delete(id):
    exist = False
    connection = dbutill.getConnection()
    try:
        cursor = connection.cursor()
        sql_sel = "DELETE FROM pF3IWeqcGm.users WHERE user_id= %s "
        cursor.execute(sql_sel, id)
        connection.commit()
        if cursor.rowcount > 0 :
            exist = True
    finally:
        # Close connection.
        connection.close()
        return exist


