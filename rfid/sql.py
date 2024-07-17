
import pyodbc
from datetime import date
import time
import threading
import psycopg2
import datetime
from rpc import mailsend
from vehicle import vehicle_info

#from whats import sendmes

from rdv import rdvvehicle

from database import dbconnex

server = 'localhost'
database = 'odoo_rfid'
username = 'postgres'
password = ''



countb =0
card = 0
last_id = None
lock = threading.Lock()
connect_string= f"""DRIVER={{ODBC Driver 17 for SQL Server}};SERVER=10.68.222.61,1433;DATABASE=ZKAccess;UID=sa;PWD=ZK+2023."""

# connex = psycopg2.connect(database='viseo13_20240426',
#                           user = 'postgres',
#                           password='1234',
#                           host='localhost',
#                           port='5432')

    
# curs = connex.cursor()
curs, connex = dbconnex()

while True:
    conn = pyodbc.connect(connect_string)
    cursor = conn.cursor()
    #print("connexion success!!")
    try:

        query2 = "SELECT COUNT(*) FROM acc_monitor_log WHERE  CAST(time AS DATE) = CAST(getdate() AS DATE) "
    #cursor.execute(query)
        cursor.execute(query2)
    #tables = cursor.fetchall()
        count = cursor.fetchone()

    
        count = count[0]
        if countb == count :
            time.sleep(1)
            
        else:
            if count ==0:
                pass
            countb = count
            print("data changed!!!", datetime.datetime.now())
            #print("number ", countb)
            query= "SELECT TOP 1 card_no, time, device_name, event_point_name FROM acc_monitor_log WHERE CAST(time AS DATE) = CAST(getdate() AS DATE) ORDER BY id DESC "
            cursor.execute(query)
            rows = cursor.fetchall()
            # try:
            if card == rows[0][0]:
                print("Vehicle already passed!!! at : ", datetime.datetime.now(), "Location: ", rows[0][2] )
                time.sleep(1)
            else:   
                print("card id: ", rows[0][0])
                print("Time: ",rows[0][1])
                print("Location: ",rows[0][2])
                
                card = rows[0][0]
                tt = rows[0][1]
                loc = rows[0][2]
                if card == '' or card == '0':

                    print("card without identifiant")
                else:
                    if loc == "Main":
                        vehicle_id, mdl, plq,eml, phone = vehicle_info(card)
                        
                        if mdl :
                            email, mobile, message = rdvvehicle(vehicle_id)
                            if message is None:
                                message = "Bonjour, bienvenue dans l'enceinte Viseo Andraharo."
                                #sms(mobile[1:])
                                #sendmes(mobile,message)
                                mailsend(card,loc, tt, vehicle_id,mdl, plq,email)
                            else:
                                #sms(mobile[1:])
                                #sendmes(mobile,message)
                                mailsend(card,loc, tt, vehicle_id,mdl, plq,email)
                                time.sleep(2)
                        else :
                            print("Vehicule: None, card not attributed!!!")
                            time.sleep(2)
            #print("id : ",cc)
                    else:
                        vehicle_id, mdl, plq,eml, phone = vehicle_info(card)
                        if mdl :

                            email, mobile, message = rdvvehicle(vehicle_id)
                            if message is None:
                                message = "Bonjour, bienvenue dans l'enceinte Viseo Andraharo."
                                #sms(mobile[1:])
                                #sendmes(mobile,message)
                                #sendsms(mobile)
                            else:
                                #sms(mobile[1:])
                                #sendmes(mobile,message)
                                mailsend(card,loc, tt, vehicle_id,mdl, plq,email)
                                time.sleep(2)
                            #sendsms(mobile,sms)
                            #mailsend(card,loc, tt, vehicle_id,mdl, plq,email)
                            #time.sleep(2)
                        else :
                            print("Vehicle: None, card not attributed!!!")
                            time.sleep(2)
            # except:
            #     print('Error in code')            
            
        conn.close()
        
        
    
    except pyodbc.Error as e:
        print(f'Erreur:{e}')
        
        
    

