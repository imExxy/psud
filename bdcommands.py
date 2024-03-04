from app import app
import sqlite3
from app.models import RealEstate
import pandas as pd

con = sqlite3.connect("app.db")
cur = con.cursor()

#cur.execute('delete from maint;')
#con.commit()
with app.app_context():
  testvar2 = 5
  res3 = RealEstate.query.filter(RealEstate.id == testvar2).all()
  print(res3)
  print(type(res3))
testvar = 5
res = cur.execute(f'select * from real_estate where id = {testvar};')
res2 = res.fetchall()

print(res2)
print(type(res))
print(type(res2))
# .format(testvar = testvar)
#print(res.fetchall())
cur.close()