import json
import requests
import pymysql

# Connect to the database
db = pymysql.connect(autocommit=True,
                     host='localhost',
                     user='root',
                     password='',
                     database='tp2_mongo',
                     charset='utf8',
                     cursorclass=pymysql.cursors.DictCursor)
print(db)

cursor = db.cursor()


def conexionUrl(id):

    url = "https://restcountries.eu/rest/v2/callingcode/" + id

    # Consulta http
    resp = requests.get(url)

    if (resp.status_code != 404):

        # Lectura de json
        data = json.loads(resp.content)

        # Asignacion de datos
        codigoPais = data[0]['callingCodes'][0],
        nombrePais = data[0]['name'],
        capitalPais = data[0]['capital'],
        region = data[0]['region'],
        latitud = data[0]['latlng'][0],
        longitud = data[0]['latlng'][1],

        pais = cursor.execute(
            "SELECT * FROM pais WHERE codigoPais = %s", codigoPais[0])
        if(pais):
            cursor.execute('UPDATE pais SET nombrePais= %s,capitalPais= %s,region=%s,latitud=%s,longitud=%s WHERE codigoPais = %s',
                           (nombrePais[0], capitalPais[0], region[0], latitud[0], longitud[0], codigoPais[0]))
            print("Tabla Pais Actualizada", " Codigo Pais actualizado: " , codigoPais[0])
        else:
            cursor.execute('INSERT INTO pais(codigoPais,nombrePais,capitalPais,region,latitud,longitud) values (%s,%s,%s,%s,%s,%s)',
                           (codigoPais[0], nombrePais[0], capitalPais[0], region[0], latitud[0], longitud[0]))
            print("Pais agregado Correctamente" , " Code: " , codigoPais[0])
        
               
for i in range(301):
    if (i == 300):
        print("Carga Completada")
    else: 
        conexionUrl(str(i))
 
