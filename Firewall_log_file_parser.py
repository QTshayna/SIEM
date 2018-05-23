import mysql
from mysql import connector
from mysql.connector import errorcode
from mysql.connector import Error



def reset_db():
   # empty=("""INSERT INTO fwlogs
    #(DROP DATABASE seim)""")


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
            print("err")
        return None


def loglinestodict(path,cursor,cnx):# gets a log and creates a dictionary
    open_file=open(path,'r')
    read_line=open_file.readlines()
    log_dic={}

    dic_list=[]
    for line in read_line:
        val= line.split()
        log_dic['DATE']=val[0]+' '+val[1]
        log_dic['SRC_IP']=val[2]
        log_dic['DST_IP']=val[3]
        log_dic['PORT']=val[4]
        log_dic['PROTOCOL']=PortNumToProt(val[4])

        log_dic['ACTION']=val[5]
        InsertToDB(log_dic,cnx,cursor)
        #dic_list.append(log_dic)
    return dic_list


def PortNumToProt(num):
    PORTS = {'21': 'FTP', '22': 'SSH', '23': 'TELNET', '25': 'SMTP', '67': 'DHCP', '53': 'DNS', '80': 'HTTP', '445'
    : 'SMB', '443': 'HTTPS'}
    for key,value in PORTS.iteritems():
        if key == num :#in PORTS.keys:
            return value
    else :
        return 'unknown'




def InsertToDB(log, cnx, cursor):
    add_log = ("""INSERT INTO fwlogs
            (ID, DATE, SRC_IP, DST_IP, PORT, PROTOCOL, ACTION)
            VALUES (NULL, %(DATE)s, %(SRC_IP)s, %(DST_IP)s, %(PORT)s, %(PROTOCOL)s, %(ACTION)s)""")
    cursor.execute(add_log, log)
    cnx.commit()




def main():
    cnx, cursor = ConnectToDB()
    log = loglinestodict('Port_scan.txt', cursor, cnx)  # loglinestodict(log,cnx,curser)
    InsertToDB(log,cnx,cursor)

    num='22'
    print PortNumToProt(num)


if __name__=='__main__':
    main()
