import sqlite3
import os

__all__ = ['create_dbase', 'check_dbase', 'record_dbase']

def create_dbase():
    with sqlite3.connect('realty.db') as connection:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE offers(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                offer_id INTEGER,
                url TEXT,
                adress TEXT,
                price INTEGER,
                datetime TEXT
            )
        """)

def check_dbase(offer_id):
    with sqlite3.connect('realty.db') as connection:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT offer_id FROM offers WHERE offer_id = (?)
        """,(offer_id, ))
        result = cursor.fetchone()
    return result

def record_dbase(offer):
    with sqlite3.connect('realty.db') as connection:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO offers
            VALUES (NULL, :offer_id, :url, :adress, :price, :datetime)
        """, offer)
        connection.commit()

def main():
    current_directory = os.getcwd()
    if not os.path.exists(current_directory + '/realty.db'):
        create_dbase()

if __name__ == '__main__':
    main()