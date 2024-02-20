import psycopg2

def dbconnex(self):
    connex = psycopg2.connect(database='mobile_101023',
                               user='etech',
                               password='3Nyy22Bv',
                               host='10.68.132.2',
                               port='5432')
    curs = connex.cursor()

    return curs, connex