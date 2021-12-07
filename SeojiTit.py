import requests
import translators as ts


class Obejekt(object):

    def __init__(self):
        self.org = None #Оригинальная строка обьекта с которым работаем
        self.url = None  #Полная строка с сайта

        self.kor = '' #Корейский

        self.au = None #Автор на коре
        self.il = None #Иллюстратор на коре
        self.iz = None #Издатель на кор

    def add_url(self):
        self.url = input()
        self.url = str(requests.get(self.url).text)

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
        self.kor = self.org

    #Выдаёт строку автора без вырезов
    def add_org_au(self):
        tmp = self.url
        self.org = (self.url[self.url.find('<dt>제목 </dt>')+200:self.url.find('<dt>제목 </dt>')+1000])
        self.org = self.org[self.org.find('<dd>')+4:self.org.find('</dd>')+5]
        self.url = tmp

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


def main():
    tit = Obejekt()

    #Для названия
    tit.add_url()
    tit.add_org_tit()

    #Вывод названия
    print(tit.org)
    print(ts.google(tit.org, to_language='en'))
    print(ts.google(tit.org, to_language='ru'))
    print(' ')

    #Для автора и иллюстратора
    tit.add_org_au()
    tit.ilust_idi()
    tit.autor_idi()

    
    #Вывод автора
    print('Автор:')
    print(tit.au)
    if tit.au!=None:
        print(ts.google(tit.au, to_language='en'))
    print(' ')

    if tit.il!=None: #Проверяю есть ли иллюстратор
        print('Иллюстратор:')
        print(tit.il)
        print(ts.google(tit.il, to_language='en'))
        print('')

    if tit.il != None:
        print('Издатель:')
        tit.add_org_iz()
        print(ts.google(tit.iz, to_language='ko'))
        print(ts.google(tit.iz, to_language='en'))

if __name__ == "__main__":
    main()
