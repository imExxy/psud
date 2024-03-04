from app import app
import sqlite3
from app import db
import pandas as pd
from app.models import RealEstate

maindf = pd.read_csv('D:/xxx/Documents/cian_parsing.csv', sep=";", encoding='windows-1251')
maindfcols = maindf.columns



con = sqlite3.connect("app.db")
cur = con.cursor()


# Создание таблицы, запрос CREATE TABLE
#
# cur.execute("CREATE TABLE movie(title, year, score)")

# Цикл, в котором вы перебираете датафрейм и вставляете в данные в строки таблицы

# INSER

columns = maindf.columns.tolist()


"""for i in columns:
    con.execute(f'INSERT INTO maint VALUES ()')"""

#maindf.to_sql('maint', cur, if_exists='replace', index=False)
#cur.commit()


#cur.execute('show tables;')

L = maindf.shape[0]
print(L)
author = ""
author_type = ""
link = ""
city = ""
deal_type = ""
accommodation_type = ""
floor = 0
floors_count = 0
rooms_count = 0
total_meters = 0
price_per_m2 = 0
price_per_month = 0
commissions = 0
district = ""
street = ""
house_number = ""
underground = ""

for i in range(L):
    #print(author, author_type, link)

    ad_obj = RealEstate(
        author = maindf['author'][i],
        author_type = maindf['author_type'][i],
        link = maindf['link'][i],
        city = maindf['city'][i],
        deal_type = maindf['deal_type'][i],
        accommodation_type = maindf['accommodation_type'][i],
        floor = int(maindf['floor'][i]),
        floors_count = int(maindf['floors_count'][i]),
        rooms_count = int(maindf['rooms_count'][i]),
        total_meters = float(maindf['total_meters'][i]),
        price_per_m2 = int(maindf['price_per_m2'][i]),
        price_per_month = int(maindf['price_per_month'][i]),
        commissions = int(maindf['commissions'][i]),
        district = maindf['district'][i],
        street = maindf['street'][i],
        house_number = maindf['house_number'][i],
        underground = maindf['underground'][i]
    )
    with app.app_context():
        db.session.add(ad_obj)
        db.session.commit()



#res = cur.execute('select * from maint;')
#print(res.fetchone())