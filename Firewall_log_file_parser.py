import mysql
from mysql import connector
from mysql.connector import errorcode
from mysql.connector import Error

def loglinestodict(path):# gets a log and creates a dictionary
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
        dic_list.append(log_dic)
    return dic_list


def PortNumToProt(num):
    PORTS = {'21': 'FTP', '22': 'SSH', '23': 'TELNET', '25': 'SMTP', '67': 'DHCP', '53': 'DNS', '80': 'HTTP', '445'
    : 'SMB', '443': 'HTTPS'}
    for key,value in PORTS.iteritems():
        if key == num :#in PORTS.keys:
            return value
    else :
        return 'unknown'

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


def InsertToDB(log, cnx, cursor):
    for i in log:

        add_log = ("""INSERT INTO fwlogs
                (ID, DATE, SRC_IP, DST_IP, PORT, PROTOCOL, ACTION)
                VALUES (NULL, %(DATE)s, %(SRC_IP)s, %(DST_IP)s, %(PORT)s, %(PROTOCOL)s, %(ACTION)s)""")
        cursor.execute(add_log, i)
        cnx.commit()




def main():
    log='Port_scan.txt'
    print(loglinestodict(log))
    num='22'
    print PortNumToProt(num)
    ConnectToDB()
    cnx,cursor =ConnectToDB()
    loglinestodict('Ping_Sweep.txt')
    InsertToDB(loglinestodict('Ping_Sweep.txt'), cnx, cursor)


if __name__=='__main__':
    main()
