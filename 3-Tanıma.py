import cv2
import numpy as np
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import xlrd, xlwt
from datetime import datetime
from datetime import date

style_string = "font: bold on; borders: bottom dashed"
style = xlwt.easyxf(style_string)
style1 = xlwt.easyxf(num_format_str='D-MMM-YY')

wb= xlwt.Workbook(encoding="utf-8")
ws = wb.add_sheet('Gelenler', cell_overwrite_ok=True)
bir_col = ws.col(0)
bir_col.width = 256 * 20
iki_col = ws.col(1)
iki_col.width = 256 * 20
uc_col = ws.col(2)
uc_col.width = 256 * 20
tarih_col = ws.col(4)
tarih_col.width = 256 * 13

df = pd.read_excel('sinif_listesi.xls')
ad = df['Ad']
soyad = df['Soyad']
no = df['Numara']
sinif = df['Sinif']
uzunluk=len(df)

ws.write(0,4,datetime.now(),style1)
ws.write(0,0,'Numara',style=style)
ws.write(0,1,'Ad',style=style)
ws.write(0,2,'Soyad',style=style)
ws.write(0,3,'Sinif',style=style)
for z in range(0,uzunluk):
    ws.write(z+1,0,str(no[z]))
    ws.write(z+1,1,ad[z])
    ws.write(z+1,2,soyad[z])
    ws.write(z+1,3,int(sinif[z]))
    ws.write(z+1,4,"-") 

recognizer = cv2.face.LBPHFaceRecognizer_create() 
recognizer.read('ogrenme/ogrenme.yml')
cascadePath = "haarcascade_frontalface_default.xml" 
faceCascade = cv2.CascadeClassifier(cascadePath);

cam = cv2.VideoCapture(1) 
font = cv2.FONT_HERSHEY_SIMPLEX 
while True:
    ret, im =cam.read()
    gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    faces=faceCascade.detectMultiScale(gray, 1.2,5)
    for(x,y,w,h) in faces:
        cv2.rectangle(im,(x,y),(x+w,y+h),(150,0,0),2)
        Id, conf = recognizer.predict(gray[y:y+h,x:x+w])

        for i in range(0,uzunluk): 
            if Id== no[i]: 
                ws.write(i+1,4,"+",style=style) 

        cv2.putText(im,str(Id),(x+5,y+h-5), font, 0.5,(0,0,255),1,cv2.LINE_AA)
    cv2.imshow('YUZ TANIMA UYGULAMASI',im);

    if(cv2.waitKey(1)==ord('q')):
        wb.save('Yoklama/gelenler '+str(date.today())+'.xls')
        break;
cam.release()
cv2.destroyAllWindows()
