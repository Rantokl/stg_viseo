import pyodbc
from datetime import date
import time
import threading
import psycopg2
import datetime
from rpc import mailsend
from database import dbconnex
server = 'localhost'
database = 'analytic_odoo'
username = 'postgres'
password = ''


def vehicle_info(card):
    #connect_string= f"""DRIVER={{ODBC Driver 17 for SQL Server}};SERVER=10.68.222.61,1433;DATABASE=ZKAccess;UID=sa;PWD=ZK+2023."""
    #print(type(card))
    # connex = psycopg2.connect(database='viseo13_20240426',
    #                       user = 'postgres',
    #                       password='1234',
    #                       host='localhost',
    #                       port='5432')


    
    # curs = connex.cursor()
    
    curs, connex = dbconnex()
    query = """SELECT fv.id, fv.driver_id, vtr.name 
                FROM fleet_vehicle fv INNER JOIN viseo_tag_rfid vtr on vtr.id = fv.tag_rfid 
                WHERE vtr.name = %s 
            """
    curs.execute(query,(card,))

    
    

    vehicles = curs.fetchall()
    if vehicles:
        vehicle_id = vehicles[0][0]
        email_id = vehicles[0][1]
        curs.execute("""SELECT vtr.name, fv.license_plate
                        FROM fleet_vehicle fv INNER JOIN fleet_vehicle_model vtr on vtr.id = fv.model_id 
                        WHERE CAST(fv.id AS INTEGER) = CAST(%s AS INTEGER);
                        """,(vehicle_id,))


        models = curs.fetchall()

        model = models[0][0]
        plaque = models[0][1]
        curs.execute("SELECT name, email, phone, mobile FROM res_partner WHERE id = %s",(email_id,))
        emails = curs.fetchall()
        email = emails[0][1]
        phone = emails[0][2]
        mobile = emails[0][3]
        connex.close()
        return vehicle_id,model,plaque, email, phone,mobile
    else:
        print("Card not attributee")
        vehicle_id = None
        model = None
        plaque = None
        email = None
        mobile = None
        return vehicle_id,model,plaque, email, mobile
    
    
        
    

