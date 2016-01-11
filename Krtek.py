#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

KRTEK.py - program glowny gry Krtek

autor: Ewa Baranowska
last edited: 11.01.2016


# wymiary okna automatyczne!!


# nowa gra zrobić?
# posprzatac
# te napisy po czesku

"""
import sys, time, random
from PyQt4 import QtGui, QtCore



# GLOWNA APLIKACJA
class Krtek(QtGui.QMainWindow):
    
    #konstruktor
    def __init__(self):
        
        super(Krtek, self).__init__()
        
        self.initUI()

    def initUI(self):
    
        self.rozmiarOkna = 600
    
        # USTAWIENIA PODSTAWOWE OKNA
        # na razie nie ogarnelam jak dostac zaktualizowane wymiary centralWidget
        # przed funkcja show() dla okna glownego, wiec wiem z wypisywan po show
        # ze pasek menu i pasek stanu zabieraja 47 px okna, a ja chce kwadracik
        # (moze cos z update(), setFixedsize??)
        self.setFixedSize(self.rozmiarOkna,self.rozmiarOkna+47)
        self.center()
        self.setWindowTitle('KRTEK')
        self.setWindowIcon(QtGui.QIcon('ikonka1.png'))       
        
        
        # pasek menu
        menubar = self.menuBar()
               
        # zakladka File
        fileMenu = menubar.addMenu('&Soubor')
      
        # podzakladka Options
        optionsAction = QtGui.QAction('Možnosti', self)
        optionsAction.setShortcut('Ctrl+M')
        optionsAction.setStatusTip('Změna možností')
        optionsAction.triggered.connect(self.okno_opcje)
        
        fileMenu.addAction(optionsAction)
        
        # podzakladka Quit
        exitAction = QtGui.QAction('Ukončení', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Zavřít aplikaci')
        exitAction.triggered.connect(self.close)
        
        fileMenu.addAction(exitAction)
        
        # zakladka Help
        helpMenu = menubar.addMenu('&Pomoc')   
        
        # podzakladka About
        aboutAction = QtGui.QAction('O aplikaci (eng)', self)
        aboutAction.setShortcut('Ctrl+H')
        aboutAction.setStatusTip('O aplikaci Krtek')
        aboutAction.triggered.connect(self.okno_about)
        
        helpMenu.addAction(aboutAction)
        
        
        # pasek statusu
        self.statusbar = self.statusBar()
        self.statusbar.showMessage('Ano!')
        
        
        
        # USTAWIENIE CENTRALNEGO WIDGETU
        # ustawiam plansze gry w centrum aplikacji i przekazuje jej info o 
        # wymiarze okna glownego (to docelowe, tu 600)
        self.plansza = Plansza(self, self.rozmiarOkna)
        self.setCentralWidget(self.plansza)
        
        # laczymy info z Planszy z napisami w statusbar
        self.plansza.doStatusBara[str].connect(self.statusbar.showMessage)
        
        self.show()
        
        
        
    # ustawianie okna na srodku ekranu
    def center(self):
        
        #qr = self.frameGeometry()
        #cp = QtGui.QDesktopWidget().availableGeometry().center()
        #qr.moveCenter(cp)
        #self.move(qr.topLeft())
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, 
            (screen.height()-size.height())/2)

    # okno Options
    def okno_opcje(self):
        
        opcje = oknoOpcji(self)
        opcje.show()
        
    # okno About
    def okno_about(self):
        
        about =QtGui.QDialog(self)
        about.setWindowTitle("O aplikaci (eng)")
        about.resize(350, 350)
        l = QtGui.QVBoxLayout()
        
        # bo czemu nie html
        tekst =QtGui.QLabel("""
        <center><IMG SRC="ikonka1.png" ALT="ikonka" WIDTH=150 HEIGHT=150></center>
        <center><h2>Krtek 1.0</h2></center>
        <center><h4>The Czech version of popular Snake game</h4></center>
        <center><h4>Copyright © 2016 Ewa Baranowska </h4></center>
        <center><h4>Inspired by Krtek (Copyright © Zdeňek Miler)</h4></center>
        <center><h4>For bug reports, please go to my Github <a href="https://github.com/flaminka/Python_gra">website</a> </h4></center>
        """)
        tekst.setOpenExternalLinks(True) # by otworzylo link po kliknieciu
        l.addWidget(tekst)
                
        h = QtGui.QHBoxLayout()
        przyciskOK = QtGui.QPushButton('OK', self)
        przyciskOK.clicked.connect(about.close)
        przyciskOK.setFixedSize(100,30) 
        przyciskOK.move(150,150)
        h.addWidget(przyciskOK)
        l.addLayout(h)
        about.setLayout(l)
        about.show()
        
    

class oknoOpcji(QtGui.QDialog):
    
    def __init__(self, parent):
        
        super(oknoOpcji, self).__init__(parent)
        
        self.parent = parent
        self.initOknoOpcji()

    def initOknoOpcji(self):
    

        self.setWindowTitle("Možnosti")
        self.resize(400, 400)
        
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)
        self.setLayout(grid)
        self.board = grid
        
        
        
        self.predkosc = 300
        self.jedzenieCzas = 4000
        self.tlo = "trawka.png"
 
        # DAC JAKIES OGRANICZENIA NA PODAWANE WIELKOSCI!!!
 
        # mozna rozciagac widgety na pare pol 
 
        # zmiana predkosci gry
        labelkaPredk = QtGui.QLabel("Choose game speed (the smaller the faster):")
        self.board.addWidget(labelkaPredk, 0, 0)

        PredkCombobox = QtGui.QComboBox(self)   
        PredkCombobox.addItem("500")
        PredkCombobox.addItem("400")
        PredkCombobox.addItem("300")
        PredkCombobox.addItem("200")
        PredkCombobox.addItem("100")
        PredkCombobox.activated[str].connect(self.updateSpeed)
        self.board.addWidget(PredkCombobox, 0, 1)  
        
 
        # zmiana interwalow dla jedzenia
        labelkaJedz = QtGui.QLabel("Choose food time interval:")
        self.board.addWidget(labelkaJedz, 1, 0)
        
        JedzCombobox = QtGui.QComboBox(self)   
        JedzCombobox.addItem("5000")
        JedzCombobox.addItem("4000")
        JedzCombobox.addItem("3000")
        JedzCombobox.addItem("2000")
        JedzCombobox.addItem("1000")
        JedzCombobox.activated[str].connect(self.updateFood)
        self.board.addWidget(JedzCombobox, 1, 1)  
        
    
        # zmiana trawki
        labelkaTlo = QtGui.QLabel("Choose background:")
        self.board.addWidget(labelkaTlo, 2,0)
        
        
        TloCombobox = QtGui.QComboBox(self)   
        TloCombobox.addItem("light texture")
        TloCombobox.addItem("dark texture")
        TloCombobox.addItem("light green")
        TloCombobox.addItem("dark green")
        self.board.addWidget(TloCombobox, 2, 1)        
        TloCombobox.activated[str].connect(self.updateTlo)
        

        # przycisk ok
        przyciskOK = QtGui.QPushButton('Change settings', self)
        przyciskOK.clicked.connect(self.updateKrtek)
        przyciskOK.resize(przyciskOK.sizeHint())
        self.board.addWidget(przyciskOK, 5,1)

   
    
    # moze bez przyciskow
    def updateSpeed(self, text):
        self.predkosc = int(text)
        
    def updateFood(self, text):
        self.jedzenieCzas = int(text)
        
    def updateTlo(self, text):
        
        if text == "light texture":
            text = "trawka.png"
        elif text == "dark texture":
            text = "trawka1.png"
        elif text == "light green":
            text = "trawka2.png"
        elif text == "dark green":
            text = "trawka3.png"
        self.tlo = text

    def updateKrtek(self):
        
        # tu cos nie dziala, dac to moe sygnalem --!!!!!
        #self.parent.plansza.close()
        self.parent.plansza = Plansza(self.parent,self.parent.rozmiarOkna, self.predkosc, self.jedzenieCzas, self.tlo)
        self.parent.setCentralWidget(self.parent.plansza)
        self.parent.plansza.doStatusBara[str].connect(self.parent.statusbar.showMessage)
        self.parent.plansza.show()# tu dodac argumenty w init
        #self.parent.update()
        #self.parent.plansza.update()
        self.close()
        
        # nie pokazuje sie np. na statusbarze wynik czy cokolwiek
        # jakis update planszy
        # dodac do kontstruktora te szybGry itd





class Plansza(QtGui.QFrame):
    
  
    doStatusBara = QtCore.pyqtSignal(str)
    
    
    def __init__(self, parent, rozmiarOkna_Gl, predkosc = 300, jedzenie = 4000, tlo = "trawka1.png"):
        
        super(Plansza, self).__init__(parent)
        self.szybkoscGry = predkosc
        self.czasJedzonka = jedzenie
        self.tlo = tlo 
        self.initPlansza(rozmiarOkna_Gl)

        
    def initPlansza(self,rozmiarOkna_Gl):
        
        #pamietac by jakos dostac sie do wymiarow jednej labelki i ustawic krecika
        #pod to
        self.rozmiarOkna_Gl = rozmiarOkna_Gl        
        self.szerPlanszy = 11 
        
        # LAYOUT GRY
        grid = QtGui.QGridLayout()
        grid.setSpacing(0)
        self.setLayout(grid)
        self.board = grid

        # tło
        trawka = QtGui.QPixmap(self.tlo)  

        positions = [(i,j) for i in range(self.szerPlanszy) for j in range(self.szerPlanszy)]
        
        for position in positions:
            
            labelka = QtGui.QLabel(self)
            labelka.setPixmap(trawka)
            self.board.addWidget(labelka, *position)
                       
        wymiarChodzika = int(self.rozmiarOkna_Gl/ self.szerPlanszy)
        
        # jedzonka
        kopiec = QtGui.QPixmap("kopiec.png") 
        kopiec = kopiec.scaled(wymiarChodzika,wymiarChodzika,QtCore.Qt.KeepAspectRatio)
        kopiecL = QtGui.QLabel(self)
        kopiecL.setPixmap(kopiec)
        self.jedzonko = kopiecL
        self.row_jedzonko = self.szerPlanszy-2
        self.col_jedzonko = self.szerPlanszy-2
        grid.addWidget(self.jedzonko,self.row_jedzonko,self.col_jedzonko)
        
        self.jedzonkoTimer = QtCore.QBasicTimer()
        self.jedzonkoTimer.start(self.czasJedzonka, self)  

        # chodzik
        krecik = QtGui.QPixmap("chodzik1.png")
        krecik = krecik.scaled(wymiarChodzika,wymiarChodzika,QtCore.Qt.KeepAspectRatio)
        self.krecik = krecik
        krecikL = QtGui.QLabel(self)
        krecikL.setPixmap(self.krecik)
        self.chodzik = krecikL
        self.chodzik.aktual_row = int(self.szerPlanszy/2)
        self.chodzik.aktual_col = int(self.szerPlanszy/2)
        grid.addWidget(self.chodzik,int(self.szerPlanszy/2),int(self.szerPlanszy/2))
        
        
        self.kierunek = "prawo"
        
        # dodawanie kolejnych krecikoczlonow
        self.czlony = []
        self.ile_czlonow = 0
        self.czyCosZjedzone = False
        
        # do czlonow obrazek
        czlon_obraz = QtGui.QPixmap("czlon.png")
        czlon_obraz = czlon_obraz.scaled(wymiarChodzika,wymiarChodzika,QtCore.Qt.KeepAspectRatio)
        self.czlon_obraz = czlon_obraz
            

        # do ruchu
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.isStarted = True
                   
                   
                   
        self.timer = QtCore.QBasicTimer() 
        self.timer.start(self.szybkoscGry, self)
        self.isPaused = False
                           
    def timerEvent(self, event):
        
        if event.timerId() == self.timer.timerId():
                            
            czlonyInverse = self.czlony[::-1]
            
            # zapisywanie pozycji czlonow
            self.zajeteRow = []                
            self.zajeteCol = []            
                
                
            for czlon in czlonyInverse:
                czlon.updatePosition()
                self.zajeteRow.append(czlon.aktual_row)
                self.zajeteCol.append(czlon.aktual_col)
                czlon.ruszCzlon()
                
               

            
            self.ruch_krecika(self.kierunek) # jaki kierunek taka pozycja
            
            # zapisujemy aktualnie zajete miejsca, by nie stawiac tam jedzenia
            # i by wiedziec czy gameover
            self.miejscaZajete = []
            self.miejscaZajete = [(i,j) for i,j in zip(self.zajeteRow, self.zajeteCol)]

            pozycjaChodzika = (self.chodzik.aktual_row, self.chodzik.aktual_col)         
            
            # jesli wejdzie chodzik w czlon game_over (i nie bylo przedtem gameover)
            if pozycjaChodzika in self.miejscaZajete and self.isStarted:
                self.game_over()
            else:
                self.miejscaZajete.append(pozycjaChodzika)            
                # ruszamy kreta
                self.board.addWidget(self.chodzik,*pozycjaChodzika)
            


            if self.chodzik.aktual_col==self.col_jedzonko and self.chodzik.aktual_row ==self.row_jedzonko:
                self.ile_czlonow = self.ile_czlonow + 1
                self.jedzonko.hide()
                self.doStatusBara.emit("Kolik krtků: " + str(self.ile_czlonow))
                self.czyCosZjedzone = True
                
                if self.ile_czlonow == 1:
                    self.ktoteraz = self.chodzik
                else:
                    self.ktoteraz = self.czlony[-1] 
                
                self.czlony.append( Czlon(self, self.ktoteraz, self.czlon_obraz) )
                
                # przyspieszamy gre wraz ze zjedzeniem kopca
                if self.szybkoscGry > 10:
                    self.szybkoscGry = self.szybkoscGry - 10
                    self.timer.start(self.szybkoscGry, self)
                        
        #dodawanie jedzonka co okreslomy czas
        if event.timerId() == self.jedzonkoTimer.timerId():  
            
            self.row_jedzonko = random.randint(0, self.szerPlanszy-1)
            self.col_jedzonko = random.randint(0, self.szerPlanszy-1)
            self.jedzonko.show()
            while (self.row_jedzonko, self.col_jedzonko) in self.miejscaZajete:
                self.row_jedzonko = random.randint(0, self.szerPlanszy-1)
                self.col_jedzonko = random.randint(0, self.szerPlanszy-1)
            self.board.addWidget(self.jedzonko, self.row_jedzonko, self.col_jedzonko)
            
        else:
            super(Plansza, self).timerEvent(event)
                             


    # ustawiamy nacisnieciem strzalek kierunek tylko
    # reakcja na wciskanie okreslonych klawiszy
    def keyPressEvent(self, event):
        
        if not self.isStarted:
            super(Plansza, self).keyPressEvent(event)
            return

        key = event.key()
        
        if key == QtCore.Qt.Key_Space:
            self.zatrzymajGre()
        elif key == QtCore.Qt.Key_Left and self.kierunek != "prawo":
            #self.ruch_krecika("lewo")
            self.kierunek = "lewo" 
        elif key == QtCore.Qt.Key_Right and self.kierunek != "lewo":
            #self.ruch_krecika("prawo")
            self.kierunek = "prawo"
        elif key == QtCore.Qt.Key_Up and self.kierunek != "dol":
            #self.ruch_krecika("gora")
            self.kierunek = "gora"
        elif key == QtCore.Qt.Key_Down and self.kierunek != "gora":
            #self.ruch_krecika("dol")
            self.kierunek = "dol"
        else:
            super(Plansza, self).keyPressEvent(event)
     
    def zatrzymajGre(self):
        
        if not self.isStarted:
            return

        self.isPaused = not self.isPaused
        
        if self.isPaused:
            self.timer.stop()
            self.jedzonkoTimer.stop()
            self.doStatusBara.emit("Přestávka")
            
        else:
            self.timer.start(self.szybkoscGry, self)
            self.jedzonkoTimer.start(self.czasJedzonka, self)
            self.doStatusBara.emit("Kolik krtků: " + str(self.ile_czlonow))

            
                 
    # ustalamy nastepna pozycje krecika w zaleznosci od kierunku
    def ruch_krecika(self, wktoraStrona):
        
        if wktoraStrona == "lewo":
            self.chodzik.aktual_col = self.chodzik.aktual_col -1
            #self.kierunek = "lewo"
            # jak wyjdzie poza plansze to koniec gry
            if self.chodzik.aktual_col == -1:
                self.game_over()
                self.chodzik.aktual_col = 0
                
            #else: #wywal elsa, jak chcesz teleporty na przeciwna strone
            #    self.board.addWidget(self.chodzik,self.aktual_row,self.aktual_col)
        elif wktoraStrona == "prawo":
            self.chodzik.aktual_col = self.chodzik.aktual_col +1
            #self.kierunek = "prawo"
            if self.chodzik.aktual_col == self.szerPlanszy:
                self.game_over()
                self.chodzik.aktual_col = self.chodzik.aktual_col - 1
                
            #else:
            #    self.board.addWidget(self.chodzik,self.aktual_row,self.aktual_col)
        elif wktoraStrona == "gora":
            self.chodzik.aktual_row = self.chodzik.aktual_row - 1
            #self.kierunek = "gora"
            if self.chodzik.aktual_row == -1:
                self.game_over()
                self.chodzik.aktual_row = 0
                
            #else:
            #    self.board.addWidget(self.chodzik,self.aktual_row,self.aktual_col)
        elif wktoraStrona == "dol":
            self.chodzik.aktual_row = self.chodzik.aktual_row + 1
            #self.kierunek = "dol"
            if self.chodzik.aktual_row == self.szerPlanszy:
                self.game_over()
                self.chodzik.aktual_row = self.chodzik.aktual_row - 1
                
            #else:
            #    self.board.addWidget(self.chodzik,self.aktual_row,self.aktual_col)
        else:
            return
        #self.board.addWidget(self.chodzik,self.aktual_row,self.aktual_col)


    # konczenie gry
    def game_over(self):
        
        # jak konczy sie gra, to chowamy wszystkie czlony na planszy
        if len(self.czlony) > 0:
            for czlon in self.czlony:
                czlon.hide()
        self.isStarted = False # ze klawisze juz nie dzialaja (KeyEvent patrz)
        self.timer.stop()        
        self.jedzonkoTimer.stop()
        #QtGui.QSound.play("test.wav")
        self.doStatusBara.emit("konec krtkowania :(")
        QtGui.QMessageBox.information(None, "KONEC!", "Vaše skóre: " + str(self.ile_czlonow) )
        
        

        
        
        
# potrzebny rodzic, kierunek, pozycja, bedzie zmieniac pozycje w zaleznosci od rodzica
# potrzebny wyglad,
# bedzie elementem listy self.czlony
# nazwe zdefiniowac chyba w dodanie czlonow


# DAĆ NA KONIEC TA KLASE, BO INDENTY ZLE SA TERAZ
class Czlon(QtGui.QLabel):

    # konstruktor (parent - by wiedzialo w ktorym oknie sie pojawic)
    def __init__(self, parent, poprzednik, ikonka):
        
        super(Czlon, self).__init__(parent)
        
        self.parent = parent
        self.poprzednik = poprzednik
        self.ikonka = ikonka          
        
        self.initCzlon()
      
        
    def initCzlon(self):
        
        self.aktual_row = 0
        self.aktual_col = 0
        self.setPixmap(self.ikonka)
    
    # funkcja do sledzenia polozenia rodzica
    def updatePosition(self):
        self.aktual_row = self.poprzednik.aktual_row
        self.aktual_col = self.poprzednik.aktual_col

    def ruszCzlon(self):
        self.parent.board.addWidget(self, self.aktual_row, self.aktual_col)


# URUCHAMIANIE APLIKACJI       
 
def main():

    app =  QtGui.QApplication(sys.argv)

    # ekran powitalny
    witaj_obraz = QtGui.QPixmap('tytul.png')
    witaj_ekran = QtGui.QSplashScreen(witaj_obraz, QtCore.Qt.WindowStaysOnTopHint)
    witaj_ekran.setMask(witaj_obraz.mask())
    witaj_ekran.show()
    app.processEvents()

    # uruchomienie glownej aplikacji (juz tutaj to, by sie zaladowala wczesniej)
    Krtek_apka = Krtek()
    
    # ile czasu wyswietlac ekran powitalny
    time.sleep(2)
    
    # zamkniecie ekranu powitalnego
    witaj_ekran.close()
    #witaj_ekran.finish(Krtek_apka) - zeby uzaleznic jedno okno od drugiego

    #pokazanie aplikacji glownej
    Krtek_apka.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()    
    
    
    
    
    
