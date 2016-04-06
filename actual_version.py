# -*- coding: UTF-8 -*-
import urllib2
import re
import MySQLdb
inserted=0
address = 'http://simferopol.cri.olx.ua/q-%D1%82%D0%B5%D0%BB%D0%B5%D1%84%D0%BE%D0%BD/'
website = urllib2.urlopen(address)
website_html = website.read()
try:
    website = urllib2.urlopen(address)
except urllib2.HTTPError, e:
    print "Cannot retrieve URL: HTTP Error Code", e.code
except urllib2.URLError, e:
    print "Cannot retrieve URL: " + e.reason[1]
# print website_html
pars1 = 'href="(\S+\html)\S+" title="">\s+\<img class="fleft"? src="?'
pars2 = '(\S+jpg)"?\ alt="?([А-Я0-9- йцукенгшщзхъэждлорпавыфячсмитьбю!?,.a-zA-Z&quot;]*)'
#pars3 = '<p class="pding10 lheight20 large">\s+([^\\<br\\>\n\t]*)</p>'
pars3 = '<p class="pding10 lheight20 large">\s+([^p]*)[^</p>]'
#<p class="pding10 lheight20 large">\s+\1</p>       #----this is it!
pars4 = '<meta name=\\"description\\" content=\\"((\d+\s\d+)\sгрн.:)|((\d+)\sгрн.:)|(Обмен):|((\d+)s\$)'
newparse = re.findall(pars1 + pars2, website_html)

# Open database connection
db = MySQLdb.connect("192.168.0.73", "root", "1234567", "my_db")

# prepare a cursor object using cursor() method
cursor = db.cursor()
# Drop table if it already exist using execute() method.
cursor.execute("DROP TABLE IF EXISTS data1")
# Create table as per requirement
sql = """CREATE TABLE data1 (
         id INT(11) NOT NULL AUTO_INCREMENT,
         PARSE_NAME  TEXT,
         HTML_LINK CHAR(150),
         JPG_LINK CHAR(150),
         PRIVATE TEXT,
         PRICE TEXT,
         PRIMARY KEY (id))"""
cursor.execute(sql)  # creating table!!!
cursor.execute('SET NAMES UTF8;')
# Prepare SQL query to INSERT a record into the database.
for i in newparse:
    website_personal = urllib2.urlopen(i[0]).read()
    description = re.findall(pars3, website_personal)
    price = re.findall(pars4, website_personal)
    for info in description:
        info_new=info#re.sub('<br />', '', (re.sub('[\(\)\{\}\n]', '', info)))
        sql_insert = """INSERT INTO data1(PARSE_NAME, HTML_LINK, JPG_LINK, PRIVATE, PRICE) VALUES ("%s","%s","%s","%s","%s");""" % (
            i[2], i[0], i[1], info_new, price)
        #sql_insert = """INSERT INTO data1(PARSE_NAME, HTML_LINK, JPG_LINK, PRIVATE) VALUES ("%s","%s","%s","%s");""" % (
            #i[2], i[0], i[1], info)
        try:
            # Execute the SQL command
            # cursor.executemany(sql, sss)
            cursor.execute(sql_insert)
            # Commit your changes in the database
            db.commit()
            inserted+=1
        except Exception as e:
            # Rollback in case there is any error
            print e
            db.rollback()
            db.close()
print "Elements total inserted: ",inserted
