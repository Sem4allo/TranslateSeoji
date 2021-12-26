import sys
import requests
from PyQt5.QtWidgets import (QGridLayout, QPushButton, QTextEdit, QInputDialog,
                             QApplication, QWidget, QLineEdit)
import translators as ts


class Obejekt(object):

    def __init__(self):
        self.org = None #Оригинальная строка обьекта с которым работаем
        self.url = None  #Полная строка с сайта

        self.kor = '' #Корейский

        self.tit = None #Название на коре
        self.au = None #Автор на коре
        self.il = None #Иллюстратор на коре
        self.iz = None #Издатель на кор

        self.tit_en = None #Название на англ
        self.au_en = None #Автор на англ
        self.il_en = None #Иллюстратор на англ
        self.iz_en = None #Издатель на англ

        self.tit_ru = None  # Название на ру
        self.au_ru = None  # Автор на ару
        self.il_ru = None  # Иллюстратор на ру
        self.iz_ru = None  # Издатель на ру

    def add_url(self, url):
        self.url = str(requests.get(url).text)

    # выдаёт строку оригинала названия без скобок и того что в них
    def add_org_tit(self):
        title = self.url.find('<div class="pageTit">')
        h2 = self.url.find('</h2>', title, title + 100)
        self.org = (self.url[title + 32:h2])
        if self.org.find('(') != (-1):
            if self.org.find(' (') != (-1):
                scob = self.org[self.org.find(' ('):self.org.find(')') + 1]
            else:
                scob = self.org[self.org.find('('):self.org.find(')') + 1]
            self.org = self.org.replace(scob, '')

        if self.org.find('[') != (-1):
            scob = self.org[self.org.find('['):self.org.find(']') + 1]
            self.org = self.org.replace(scob, '')
            self.org = self.org.replace(' ','',1)
        self.tit = self.org

    #Выдаёт строку автора без вырезов
    def add_org_au(self):
        tmp = self.url
        self.org = (self.url[self.url.find('<dt>제목 </dt>')+200:self.url.find('<dt>제목 </dt>')+1000])
        self.org = self.org[self.org.find('<dd>')+4:self.org.find('</dd>')+5]
        self.url = tmp

    #Для всех
    def delete_simvol(self, simv):
        if self.kor.find(simv) != (-1):
            self.kor = self.kor.replace(simv, '')

    #Для автора и иллюстратора
    def ilust_idi(self):
        #Проверяю есть ли иллюстратор
        if self.org.find('(그림작가)') != (-1):
            #Проверяю где он
            d=len(self.org)+1
            if self.org.find('(그림작가)', self.org.find('(그림작가)')+4) != (-1):#Иллюстратор
                if self.org.find('(그림작가)') < d :
                    d = self.org.find('(그림작가)')

            if self.org.find('기획자 :', self.org.find('(그림작가)')) != (-1):#Организатор
                if self.org.find('기획자 :') < d :
                    d = self.org.find('기획자 :')

            if self.org.find('편집자 :', self.org.find('(그림작가)')) != (-1): #Редактор
                if self.org.find('편집자 :') < d :
                    d = self.org.find('편집자 :')

            if self.org.find('원작자 :', self.org.find('(그림작가)')) != (-1): #Оригинальный автор
                if self.org.find('원작자 :') < d :
                    d = self.org.find('원작자 :')

            if self.org.find('저자 :', self.org.find('(그림작가)')) != (-1): #Автор
                if self.org.find('저자 :') < d :
                    d = self.org.find('저자 :')

            if self.org.find('원작자', self.org.find('(그림작가)')) != (-1): #Автор другой (хз)
                if self.org.find('원작자') < d:
                    d = self.org.find('원작자')

            if self.url.find('  </dd>',self.url.find('(그림작가)'))!=(-1): #Концовка
                if self.org.find('  </dd>') < d :
                    d = self.org.find('  </dd>')

            if d!=len(self.org)+1:
                self.il = self.org[self.org.find('(그림작가)'):d]
                self.il = self.il.replace('(그림작가) : ','')
                if self.il[len(self.il)-1]==' ':
                    self.il=self.il[:len(self.il)-1]
                if self.il[:len(self.il)-1]==' 'and self.il[:len(self.il)-2]==' ':
                    self.il=self.il[:len(self.il)-2]
                if self.il[:len(self.il)-1]==' 'and self.il[:len(self.il)-2]==' ' and self.il[:len(self.il)-3]==' ':
                    self.il=self.il[:len(self.il)-3]

    def autor_idi(self):
        #Проверяю какой автор
        rt = None
        if self.org.find('저자 :') != (-1):
            rt = '저자 :'
        if self.org.find('원작자') != (-1):
            rt = '원작자'
        if self.org.find('원작자 :') != (-1):
            rt = '원작자 :'

        #Есть ли вообще
        if rt != None:
            #Проверяю где он
            d=len(self.org)+1
            if self.org.find('(그림작가)', self.org.find(rt)) != (-1):#Иллюстратор
                if self.org.find('(그림작가)') < d :
                    d = self.org.find('(그림작가)')

            if self.org.find('삽화가', self.org.find(rt)) != (-1):#Иллюстратор
                if self.org.find('삽화가') < d :
                    d = self.org.find('삽화가')

            if self.org.find('기획자 :', self.org.find(rt)) != (-1):#Организатор
                if self.org.find('기획자 :') < d :
                    d = self.org.find('기획자 :')

            if self.org.find('편집자 :', self.org.find(rt)) != (-1): #Редактор
                if self.org.find('편집자 :') < d :
                    d = self.org.find('편집자 :')

            if self.org.find('원작자 :', self.org.find(rt)+4) != (-1): #Оригинальный автор
                if self.org.find('원작자 :') < d :
                    d = self.org.find('원작자 :')

            if self.org.find('저자 :', self.org.find(rt)+3) != (-1): #Автор
                if self.org.find('저자 :') < d :
                    d = self.org.find('저자 :')

            if self.org.find('원작자', self.org.find(rt)+2) != (-1): #Автор другой (хз)
                if self.org.find('원작자') < d:
                    d = self.org.find('원작자')

            if self.url.find(' </dd>',self.url.find(rt))!=(-1): #Концовка
                if self.org.find(' </dd>') < d :
                    d = self.org.find(' </dd>')

            if d != len(self.org) + 1:
                self.au = self.org[self.org.find(rt):d]
                self.au = self.au.replace(rt, '')
                if self.au[len(self.au) - 1] == ' ':
                    self.au = self.au[:len(self.au) - 1]
                if self.au[:len(self.au) - 1] == ' ' and self.au[:len(self.au) - 2] == ' ':
                    self.au = self.au[:len(self.au) - 2]
                if self.au[:len(self.au) - 1] == ' ' and self.au[:len(self.au) - 2] == ' ' and self.au[:len(self.il) - 3] == ' ':
                    self.au = self.au[:len(self.au) - 3]

                if self.au[0] == ' ':
                    self.au = self.au[1:]

                if self.au[0] == ' ' and self.au[1] == ' ':
                    self.au = self.au[2:]

                if self.au[0] == ' ' and self.au[1] == ' ' and self.au[2] == ' ':
                    self.au = self.au[3:]
        else:
            self.au =self.il


    #Выдаёт строку издателя
    def add_org_iz(self):
        tmp = self.url
        iz = self.url.find('<dt>발행처</dt>')
        self.org = self.url[iz:iz+1000]
        self.org = self.org[self.org.find('<dd>'):self.org.find('</dd>')]
        self.org = self.org[self.org.find('<dd>')+17:self.org.find('<a class=')]
        if self.org.find('(') != (-1):
            if self.org.find(' (') != (-1):
                scob = self.org[self.org.find(' ('):self.org.find(')') + 1]
            else:
                scob = self.org[self.org.find('('):self.org.find(')') + 1]
            self.org = self.org.replace(scob, '')
        self.iz = self.org
        self.iz = ts.google(self.iz, from_language='ko' ,to_language='ko')
        self.url = tmp


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ПЕРЕВОДЧИК - А ТЫ НЕ УЧИЛ КОРЕЙСКИЙ!!!")

        self.textEdit_1 = QTextEdit()
        self.btnChangeText = QPushButton("Сылка")
        self.btnChangeText.clicked.connect(self.changetext)

        self.textEdit_2 = QTextEdit()
        self.lineEdit = QLineEdit()

        self.layout = QGridLayout(self)
        self.layout.addWidget(self.textEdit_1, 0, 0)
        self.layout.addWidget(self.btnChangeText, 1, 0)

    def changetext(self):

        url = "https://google-translate20.p.rapidapi.com/translate"
        headers = {
            'x-rapidapi-host': "google-translate20.p.rapidapi.com",
            'x-rapidapi-key': "e610b08e93msh71fbb08a2c3dc7fp1128fcjsnb8bb7d9f09fc"
        }

        text, status = QInputDialog.getText(self, 'Вставь ссылку', 'Вставь ссылку!')

        tit = Obejekt()
        tit.add_url(text)

        # Для названия
        tit.add_org_tit()

        # Для автора и иллюстратора
        tit.add_org_au()
        tit.ilust_idi()
        tit.autor_idi()

        tit.add_org_iz()

        if tit.il != None:
            trnsen = tit.tit + '!' + tit.au + '!' + tit.iz + '!' + tit.il
        else:
            trnsen = tit.tit + '!' + tit.au + '!' + tit.iz

        trnsru = trnsen

        querystring = {"text": trnsen, "tl": "en", "sl": "ko"}
        response = requests.request("GET", url, headers=headers, params=querystring)

        trnsen = response.text[response.text.find('"translation":"') + 15:response.text.find('","pronunciation"')]

        tit.tit_en = trnsen[:trnsen.find('!')]
        tit.au_en = trnsen[trnsen.find('!')+2:trnsen.find('!', trnsen.find('!') + 1)]
        tit.iz_en = trnsen[trnsen.find('!', trnsen.find('!') + 1) + 2:]
        if tit.il != None:
            tit.iz_en = trnsen[trnsen.find('!', trnsen.find('!') + 1) + 2:trnsen.rfind('!')]
            tit.il_en = trnsen[trnsen.find('!', trnsen.find('!', trnsen.find('!', trnsen.find('!') + 1)) + 1)+2:]

        querystring = {"text": trnsru, "tl": "ru", "sl": "ko"}
        response = requests.request("GET", url, headers=headers, params=querystring)

        trnsru = response.text[response.text.find('"translation":"') + 15:response.text.find('","pronunciation"')]

        tit.tit_ru = trnsru[:trnsru.find('!')]
        tit.au_ru = trnsru[trnsru.find('!') + 2:trnsru.find('!', trnsru.find('!') + 1)]
        if tit.il != None:
            tit.il_ru = trnsru[trnsru.find('!', trnsru.find('!', trnsru.find('!', trnsru.find('!') + 1)) + 1) + 2:]

        a_window.addText1("Название:")
        a_window.addText1(tit.tit)
        a_window.addText1(tit.tit_en)
        a_window.addText1(tit.tit_ru)
        a_window.addText1("Автор:")
        a_window.addText1(tit.au)
        a_window.addText1(tit.au_en)
        a_window.addText1(tit.au_ru)
        if tit.il != None:
            a_window.addText1("Илюстратор:")
            a_window.addText1(tit.il)
            a_window.addText1(tit.il_en)
            a_window.addText1(tit.il_ru)
        a_window.addText1("Издатель:")
        a_window.addText1(tit.iz)
        a_window.addText1(tit.iz_en)

    def addText1(self, text):
        self.textEdit_1.insertPlainText(text + '\n')





if __name__ == "__main__":
    app = QApplication(sys.argv)
    a_window = Window()
    a_window.resize(700, 300)
    a_window.show()
    sys.exit(app.exec_())
