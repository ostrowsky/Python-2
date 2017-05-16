import pymysql.cursors

conn = pymysql.connect(host='localhost',
                             user='root',
                             password='4309344',
                             db='test',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)