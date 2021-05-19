import sqlite3, os
from sqlite3.dbapi2 import Cursor

def open_database():
    db = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db/database.db'))
    cursor = db.cursor()
    return db, cursor

def close_database(db):
    db.close()

def if_exist(discordid):
    db, cursor = open_database()

    res = cursor.execute("SELECT id FROM discord WHERE discordid = '%s'" % discordid).fetchone()
    
    close_database(db)

    return res != None

def get_db_info(discordid):
    db, cursor = open_database()

    email, password = cursor.execute("SELECT email, password FROM discord WHERE discordid = '%s'" % discordid).fetchone()
    
    close_database(db)

    return email, password