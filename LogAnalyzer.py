import mysql
from mysql import connector
from mysql.connector import errorcode
from mysql.connector import Error


def ConnectToDB():
    try:
        cnx = mysql.connector.connect(user='root', password='toor',
                                      host='192.168.43.128', database='siem')
        return cnx, cnx.cursor(buffered=True)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        return None

def PortInDB():
    cnx,cursor=ConnectToDB()
    query = (""" SELECT DISTINCT * FROM fwlogs where PORT =445 OR PORT = 4445""")
    cursor.execute(query)
    cnx.commit()
    result=cursor.fetchall()
    for r in result :
        print r



def PortScan():
    cnx, cursor = ConnectToDB()
    query = (""" SELECT DISTINCT SRC_IP DST_IP * FROM fwlogs where PORT =445 OR PORT = 4445""")
    cursor.execute(query)
    cnx.commit()
    result = cursor.fetchall()
    for r in result:
        print r


def main():
    PortInDB()



if __name__=='__main__':
    main()
