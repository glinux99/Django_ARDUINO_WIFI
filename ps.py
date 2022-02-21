import mysql.connector
import webbrowser
import urllib.request
from datetime import datetime
while True:
  clock=str(datetime.now().time())
  clock=clock.split(':')
  heure=int(clock[0])
  minute = int(clock[1])
  conn = mysql.connector.connect(host="localhost",
                               user="root", password="linux99", 
                               database="travail_db")
  cursor = conn.cursor()
  reqx="SELECT date_alum, date_ext, id_int FROM gateway_view_lp"
  cursor.execute(reqx)
  persx= cursor.fetchall()

  cursor.execute(reqx)
  persx= cursor.fetchall()
  for persx in persx:
    print(persx)
    heurex=persx[0].split(':')
    heure_alum=int(heurex[0])
    minute_alum =int(heurex[1])
    heurey=persx[1].split(':')
    heure_ext = int(heurey[0])
    minute_ext =int(heurey[1])
    if(heure==heure_alum and minute== minute_alum):
        query="UPDATE gateway_view_lp set status= %s WHERE id_int= %s"
        cursor.execute(query, (1, persx[2],))
        conn.commit()
    if(heure==heure_ext and minute== minute_ext):
        query="UPDATE gateway_view_lp set status= %s WHERE id_int= %s"
        cursor.execute(query, (0, persx[2],))
        conn.commit() 
    



req= "SELECT id_int FROM gateway_view_lp WHERE status=0"
cursor.execute(req)
pers= cursor.fetchall()
req2="SELECT id_int FROM gateway_view_lp WHERE status=1"
cursor.execute(req2)
pers1= cursor.fetchall()
a=[]

try:
   for perso in pers1:
       a.append(perso)
       b=(str(a).replace('(','').replace(')','').replace('[','').replace(']','').replace(',','').split(' '))
       #urllib.request.urlopen('http://192.168.43.181/lp_alum'+b[0])
   a=[]
   b=""
   for perso in pers:
       a.append(perso)
       b=(str(a).replace('(','').replace(')','').replace('[','').replace(']','').replace(',','').split(' '))
       #urllib.request.urlopen('http://192.168.43.181/lp_ext'+b[0])

except Exception as e:
    exit('Probleme d\'url probablement, veuillez modifier l\'url du esp8266: \n'+type(e).__name__ + ': ' + str(e))
      #urllib.request.urlopen('http://192.168.43.181/lp'+tab)    
# Opérations à réaliser sur la base ...
conn.close()
