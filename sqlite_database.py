import sqlite3

conn = sqlite3.connect('sqlite_database.db')
c = conn.cursor()

# c.execute("DROP TABLE hittestress_2012")

c.execute('''
CREATE TABLE  hittestress_2012 (
fid INTEGER PRIMARY KEY,
fid_1 INTEGER,
OBJECTID INTEGER,
Shape_Leng NUMERIC,
Shape_Area NUMERIC,
jrstatcode VARCHAR,
bu_code VARCHAR,
bu_naam VARCHAR,
jrwk VARCHAR,
wk_code VARCHAR,
wk_naam VARCHAR,
jrgm VARCHAR,
gm_code VARCHAR,
gm_naam VARCHAR,
jaar INTEGER,
_count INTEGER,
_sum INTEGER,
_mean NUMERIC,
PET_gem INTEGER,
Class INTEGER,
PC4 INTEGER);''')

conn.commit()
conn.close()
