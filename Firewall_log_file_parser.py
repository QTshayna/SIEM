from mysql import connector
from mysql.connector import errorcode

def loglinestodict(path):# gets a log and creates a dictionary
    open_file=open(path,'r')
    read_line=open_file.readlines()
    log_dic={}
    #dic_list=[]
    for line in read_line:
        val= line.split()
        log_dic['datetime']=val[0]+''+val[1]
        log_dic['source_IP']=val[2]
        log_dic['Dst_IP']=val[3]
        log_dic['port']=val[4]
        log_dic['protocal']=PortNumToProt(val[4])
        #dic_list.append(log_dic)
        #return log_dic


    return log_dic








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
                                      host='192.168.43.128', database='SIEM')
        return cnx, cnx.cursor(buffered=True)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        return None

def main():
    log='Port_scan.txt'
    print(loglinestodict(log))
    num='22'

    print PortNumToProt(num)
    ConnectToDB()


if __name__=='__main__':
    main()
