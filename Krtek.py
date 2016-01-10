#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

TUTAJ POWINIEN ZNALEZC SIE PIEKNY I INFORMATYWNY OPIS SKRYPTU

WYKORZYSTAC ARGUMENTY z konsoli (NP. JAKO TAJNE KODY DO TAJNEJ GRY)

# dac message boxa przy wychodzeniu z gry z krecikiem
# gdy game over - ahjo dzwiek
# obracanie krecika jak zmiana strony
# uzupelnic opcje - kolor tla, moze chodzika, moze szybkosc gry, rozmiar okna
# dodac pauze
# uzupelnic readme
# uzupełnić About
# zrobic troche chwili zanim sie wlaczy krecik


# NA TERAZ
# DODAC, ZE JAK CHCE WEJSC W SWOJ OGON TO GAME OVER
# zeby sie obracal chodzik jak zmienia kierunek


# posprzatac kod

# w menu - nowa gra?? - zamknij obecny example Krtek, otworz nowy, albo planszy raczej nowy?
# wymiary okna automatyczne!!
# zeby nie wchodzil w siebie jak gameover

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
        aboutAction = QtGui.QAction('O aplikaci', self)
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
        
        opcje =QtGui.QDialog(self)
        opcje.setWindowTitle("Možnosti")
        opcje.resize(400, 400)
        opcje.show()
        
    # okno About
    def okno_about(self):
        
        about =QtGui.QDialog(self)
        about.setWindowTitle("O aplikaci")
        about.resize(400, 400)
        l = QtGui.QVBoxLayout()
        tekst =QtGui.QLabel("""<center><h1>About Krtek</h1></center>
        This game was created by me""")
        l.addWidget(tekst)
        about.setLayout(l)
        about.show()



class Plansza(QtGui.QFrame):
    
  
    doStatusBara = QtCore.pyqtSignal(str)
    
    
    def __init__(self, parent, rozmiarOkna_Gl):
        
        super(Plansza, self).__init__(parent)
        self.initPlansza(rozmiarOkna_Gl)
        
    def initPlansza(self,rozmiarOkna_Gl):
        
        #pamietac by jakos dostac sie do wymiarow jednej labelki i ustawic krecika
        #pod to
        self.rozmiarOkna_Gl = rozmiarOkna_Gl        
        self.szerPlanszy = 11 
        szybkoscGry = 300
        
        # LAYOUT GRY
        grid = QtGui.QGridLayout()
        grid.setSpacing(0)
        self.setLayout(grid)
        self.board = grid

        # tło
        trawka = QtGui.QPixmap("trawka1.png")  

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
        czasJedzonka = 4000
        self.jedzonkoTimer.start(czasJedzonka, self)  

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
        self.timer.start(szybkoscGry, self)
                           
    def timerEvent(self, event):
        
        # dodawanie jedzonka co okreslomy czas
        if event.timerId() == self.jedzonkoTimer.timerId():  
            
            self.jedzonko.show()
            self.row_jedzonko = random.randint(0, self.szerPlanszy-1)
            self.col_jedzonko = random.randint(0, self.szerPlanszy-1)
            self.board.addWidget(self.jedzonko, self.row_jedzonko, self.col_jedzonko)
            
        if event.timerId() == self.timer.timerId():
                
           
            czlonyInverse = self.czlony[::-1]
            for czlon in czlonyInverse:
                czlon.updatePosition()
                czlon.ruszCzlon()
            
           
            self.ruch_krecika(self.kierunek) # jaki kierunek taka pozycja

            # ruszamy kreta
            self.board.addWidget(self.chodzik,self.chodzik.aktual_row,self.chodzik.aktual_col)
            

              
   # czy kolejnosc na liscie dobrze idzie? moze odwrotnie, moze dodatkowan funkcja...         
            # ze krecik jeszcze potem ma pewne funkcje
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
                print(len(self.czlony))
                if len(self.czlony)>1:
                    print(self.czlony[0] == self.czlony[1])

                
            
            
            
        else:
            super(Plansza, self).timerEvent(event)
                

                
# potrzebne info o kierunku by wiedziec gdzie go dodac
#
# potrzebna lista z info jakie pozycje sa zajete
               
    # tylko dodanie 
    #def dodanieCzlonow(self):
        
        
     #   krecik = QtGui.QPixmap("chodzik1.png")
      #  wymiarChodzika = int(self.rozmiarOkna_Gl/ self.szerPlanszy)
       # krecik = krecik.scaled(wymiarChodzika,wymiarChodzika,QtCore.Qt.KeepAspectRatio)
        #if self.czyCosZjedzone:
         #   czlon_nazwa = "czlon" + str(self.ile_czlonow)  #nazywam kolejne czlony numerami
          #  czlon_nazwa = QtGui.QLabel(self)
           # czlon_nazwa.setPixmap(krecik)
            #self.czlon_nazwa = czlon_nazwa
            #self.czlony.append(self.czlon_nazwa) # dodaje obiekty do listy!
            
            #self.board.addWidget(self.nazwa,self.aktual_row, self.aktual_col)    
            #dodanie wydarzenia dla obiektu?
            
           # zmiana_poz_czlonu_action = QtGui.QAction(QtCore.QCoreApplication.translate('ExchangeDockWidget',
           #                                                                                "&refresh balance"),
           #                                                                                self, triggered=self.zmiana_poz_czlonu())            
            
           # self.czlon_nazwa.addAction(zmiana_poz_czlonu_action)
            #self.czyCosZjedzone = False



# ustawiamy nacisnieciem strzalek kierunek tylko
     # reakcja na wciskanie okreslonych klawiszy
    def keyPressEvent(self, event):
        
        if not self.isStarted:
            super(Plansza, self).keyPressEvent(event)
            return

        key = event.key()
        
        if key == QtCore.Qt.Key_Space:
            return
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
                 
                 
    # ustalamy nastepna pozycje krecika w zaleznosci od kierunku
    def ruch_krecika(self, wktoraStrona):
        
        if wktoraStrona == "lewo":
            self.chodzik.aktual_col = self.chodzik.aktual_col -1
            #self.kierunek = "lewo"
            # jak wyjdzie poza plansze to koniec gry
            if self.chodzik.aktual_col == -1:
                self.chodzik.aktual_col = 0
                self.game_over()
            #else: #wywal elsa, jak chcesz teleporty na przeciwna strone
            #    self.board.addWidget(self.chodzik,self.aktual_row,self.aktual_col)
        elif wktoraStrona == "prawo":
            self.chodzik.aktual_col = self.chodzik.aktual_col +1
            #self.kierunek = "prawo"
            if self.chodzik.aktual_col == self.szerPlanszy:
                self.chodzik.aktual_col = self.chodzik.aktual_col - 1
                self.game_over()
            #else:
            #    self.board.addWidget(self.chodzik,self.aktual_row,self.aktual_col)
        elif wktoraStrona == "gora":
            self.chodzik.aktual_row = self.chodzik.aktual_row - 1
            #self.kierunek = "gora"
            if self.chodzik.aktual_row == -1:
                self.chodzik.aktual_row = 0
                self.game_over()
            #else:
            #    self.board.addWidget(self.chodzik,self.aktual_row,self.aktual_col)
        elif wktoraStrona == "dol":
            self.chodzik.aktual_row = self.chodzik.aktual_row + 1
            #self.kierunek = "dol"
            if self.chodzik.aktual_row == self.szerPlanszy:
                self.chodzik.aktual_row = self.chodzik.aktual_row - 1
                self.game_over()
            #else:
            #    self.board.addWidget(self.chodzik,self.aktual_row,self.aktual_col)
        else:
            return
        #self.board.addWidget(self.chodzik,self.aktual_row,self.aktual_col)


    # konczenie gry
    def game_over(self):
        
        self.isStarted = False # ze klawisze juz nie dzialaja (KeyEvent patrz)
        self.jedzonkoTimer.stop()
        self.timer.stop()
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
    
    
    
    
    
