import numpy as np
from os import environ
from imutils.video import VideoStream
import cv2
import pyodbc

def insertIN(placa):
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=LENOVO-HERRERA\SQLEXPRESS;'
                          'Database=RegistroPlacas;'
                          'Trusted_Connection=yes;')
    print("InsertIN")
    cursor = conn.cursor()
    cursor.execute('EXEC InsertarEntrada ?', (placa))
    conn.commit()
    conn.close()



from openalpr import Alpr

alpr_dir = 'C:/Users/DavidHerrera/AppData/Local/Programs/Python/Python37/openalpr'
environ['PATH'] = alpr_dir + ';' + environ['PATH']
alpr = Alpr('us', alpr_dir + '/openalpr.conf', alpr_dir + '/runtime_data')
if not alpr.is_loaded():
    print("Error loading OpenALPR")
    sys.exit(1)

alpr.set_top_n(1)
alpr.set_default_region("eu")

# cap = cv2.VideoCapture("http://91.190.227.198/mjpg/video.mjpg")
cap = cv2.VideoCapture("numPlates.mpg")

cap = VideoStream(src=0).start()
temp = ""
fin = ''
contador = 0
bole = 0
while (True):
    frame = cap.read()
    ret = True
    if ret:
        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.stop()
            break

        cv2.imwrite("img.jpg", frame)

        results = alpr.recognize_file("img.jpg")

        i = 0

        for plate in results['results']:
            if bole == 0:
                print("Matricula encontrada calculando:")


            bole = 1
            i += 1
            for candidate in plate['candidates']:
                if fin == '':
                    print("*", end='')


                if contador > 5 and fin == '':
                    fin = temp
                    insertIN(fin)
                    print()
                    print(fin)
                elif temp == candidate['plate']:
                    contador = contador + 1
                else:
                    fin=""
                    bole=0
                    temp = candidate['plate']
                    contador = 0

    else:
        break;

# When everything done, release the capture
cap.stop()
alpr.unload()
cv2.destroyAllWindows()
