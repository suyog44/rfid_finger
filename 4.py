import serial
import sqlite3
import time

con = sqlite3.connect('attend.db')


def read_rfid():
    ser = serial.Serial("/dev/ttyUSB3")
    ser.baudrate = 9600
    data = ser.read(12)
    ser.close()
    return data


def connectDB(data, command):
    cur = con.cursor()

    etime = time.strftime("%Y-%m-%d %a %H:%M:%S", time.localtime())

    if (command == "verify"):
        cur.execute("SELECT name FROM enrolldb WHERE card = ?", [data])
        result = cur.fetchone()
        if not result:
            print "Card not found in Database."
            return False
        else:
            print "Card found in Database."
            tmp = str(result)
            slen = len(tmp)
            name2 = tmp[3:slen-3]
            cur.execute("INSERT INTO attendb (name, card, timing)"
                        "VALUES(?, ?, ?)",
                        (name2, data, etime))
            con.commit()
            cur.close()
            return True

    if (command == "insert"):
        name = raw_input("Enter Full Name:")
        cur.execute("INSERT INTO enrolldb (name, card, timing)"
                    "VALUES(?, ?, ?)", (name, data, etime))
        con.commit()
        cur.close()

if __name__ == '__main__':
    while True:
        id = read_rfid()
        if(connectDB(id, 'verify') == False):
            connectDB(id, 'insert')
        '''print "Tag: ", str(int(id[-8:], 16)), "Date:", thetime'''
