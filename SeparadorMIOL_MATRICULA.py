from csv import reader
from fileinput import close
from multiprocessing.pool import CLOSE
from PyPDF2 import PdfFileWriter, PdfFileReader
import re
import os
from getpass import getuser

import PyPDF2

pdf = 'M:\\HOTFOLDERS\\SEPARADOR INSTANTANEO\\InformePdfMultiple.pdf' # Ruta de donde se van a leer los pdfs
String = "INFORME DE INSPECCIÓN"

abrirPDF=open(pdf, "rb")
inputpdf = PdfFileReader(abrirPDF)
empieza_informe = []
termina_informe = []
matriculas = []
NumPages = inputpdf.getNumPages()
user = getuser()

for current_page in range(0, NumPages):
    page = inputpdf.getPage(current_page)
    Text = page.extractText() 
    if re.search(String, Text):
       empieza_informe.append(current_page)
       termina_informe.append(current_page)

       sbstr_matricula = Text.split("  /  ")
       matricula = sbstr_matricula[0].split("VEHÍCULO")
       matriculas.append(matricula[1].replace('\n',''))

termina_informe.pop(0)
termina_informe.append(NumPages)

def crearArchivos(index, limit, matricula_index):

    output = PdfFileWriter()
    for i in range(index, limit):
        output.addPage(inputpdf.getPage(i))
        if i+1 in termina_informe:
            try:
                os.mkdir('M:\\HOTFOLDERS\\SEPARADOR INSTANTANEO\\%s' % user) # Ruta donde se va a crear la carpeta con los pdfs separados
                print('Se ha creado el directorio donde se guardarán los pdf: %s' % user)
            except OSError as e:
                print('-------------------------------------')
            with open("M:\\HOTFOLDERS\\SEPARADOR INSTANTANEO\\" + user +"\\%s.pdf" % matriculas[matricula_index], "wb") as outputStream: # Ruta donde se van a guardar los pdfs con el nombre de la matricula (matriculas[matricula_index] es el array que contiene las matriculas)
                output.write(outputStream)
                outputStream.close()
                print('Creado correctamente: %s' % matriculas[matricula_index])
         
for i in range(len(empieza_informe)):
    crearArchivos(empieza_informe[i], termina_informe[i], i)

abrirPDF.close()

os.remove('M:\\HOTFOLDERS\\SEPARADOR INSTANTANEO\\InformePdfMultiple.pdf')