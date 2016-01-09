#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

TUTAJ POWINIEN ZNALEZC SIE PIEKNY I INFORMATYWNY OPIS SKRYPTU

WYKORZYSTAC ARGUMENTY z konsoli (NP. JAKO TAJNE KODY DO TAJNEJ GRY)

# dac message boxa przy wychodzeniu z gry z krecikiem
# gdy game over - ahjo dzwiek
# obracanie krecika jak zmiana strony
# uzupelnic opcje


"""
import sys, time, random
from PyQt4 import QtGui, QtCore



# dziedziczymy po QtGui.QWidget
class Krtek(QtGui.QMainWindow):
    
    #konstruktor
    def __init__(self):
        super(Krtek, self).__init__()
        
        self.initUI()

    def initUI(self):
    
        self.rozmiarOkna = 600
    
        # na razie nie ogarnelam jak dostac zaktualizowane wymiary centralWidget
        # przed funkcja show() dla okna glownego, wiec wiem z wypisywan po show
        # ze pasek menu i pasek stanu zabieraja 47 px okna, a ja chce kwadracik
        # (moze cos z update(), setFixedsize??)
        self.setFixedSize(self.rozmiarOkna,self.rozmiarOkna+47)
        self.center()
        self.setWindowTitle('KRTEK')
        self.setWindowIcon(QtGui.QIcon('ikonka1.png'))       
        



        # ustawiam plansze gry w centrum aplikacji i przekazuje jej info o 
        # wymiarze okna glownego (to docelowe, tu 600)
        self.plansza = Plansza(self, self.rozmiarOkna)
        self.setCentralWidget(self.plansza)

        # pasek menu
        menubar = self.menuBar()
               
        # zakladka File
        fileMenu = menubar.addMenu('&File')
      
        # podzakladka Options
        optionsAction = QtGui.QAction('Options', self)
        optionsAction.setShortcut('Ctrl+O')
        optionsAction.setStatusTip('Change options')
        optionsAction.triggered.connect(self.okno_opcje)
        
        fileMenu.addAction(optionsAction)
        
        # podzakladka Quit
        exitAction = QtGui.QAction('Quit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)
        
        fileMenu.addAction(exitAction)
        
        # zakladka Help
        helpMenu = menubar.addMenu('&Help')   
        
        # podzakladka About
        aboutAction = QtGui.QAction('About', self)
        aboutAction.setShortcut('Ctrl+A')
        aboutAction.setStatusTip('About Krtek')
        aboutAction.triggered.connect(self.okno_about)
        
        helpMenu.addAction(aboutAction)
        
        
        # pasek statusu
        self.statusBar().showMessage('Ano!')
        
        
        #print(self.plansza.geometry())
        self.show()
        #print(self.plansza.geometry())
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
        opcje.setWindowTitle("Options")
        opcje.resize(400, 400)
        opcje.show()
        
    # okno About
    def okno_about(self):
        
        about =QtGui.QDialog(self)
        about.setWindowTitle("About")
        about.resize(400, 400)
        l = QtGui.QVBoxLayout()
        tekst =QtGui.QLabel("""<center><h1>About Krtek</h1></center>
        This game was created by me""")
        l.addWidget(tekst)
        about.setLayout(l)
        about.show()


        
        
class Plansza(QtGui.QFrame):
    
  
        
    
    
    def __init__(self, parent, rozmiarOkna_Gl):
        
        super(Plansza, self).__init__(parent)
        self.initPlansza(rozmiarOkna_Gl)
        
    def initPlansza(self,rozmiarOkna_Gl):
        
        self.rozmiarOkna_Gl = rozmiarOkna_Gl        
        
        
        grid = QtGui.QGridLayout()
        grid.setSpacing(0)
        
        self.setLayout(grid)
        
        #pamietac by jakos dostac sie do wymiarow jednej labelki i ustawic krecika
        #pod to
        self.szerPlanszy = 15 
        #szybGry = 200
        
        positions = [(i,j) for i in range(self.szerPlanszy) for j in range(self.szerPlanszy)]
        
        #obrazki
        wymiarChodzika = int(self.rozmiarOkna_Gl/ self.szerPlanszy)
        

        # tło
        trawka = QtGui.QPixmap("trawka1.png")  
        
     
        #chodzik1 = chodzik.scaled(60,60,QtCore.Qt.KeepAspectRatio)
        
        for position in positions:
            
            labelka = QtGui.QLabel(self)
            #labelka.setStyleSheet("QLabel { background-color : red }")
            #if position[0]==0 or position[1]==0 or position[0]==14 or position[1]==14:            
            #    labelka.setPixmap(droga)
           # else:
            labelka.setPixmap(trawka)
            grid.addWidget(labelka, *position)
        
        
        #labelka = QtGui.QLabel(self)        
        #labelka.setPixmap(QtGui.QPixmap(krecik)) 
        # mozna usuwac i dodawac addWidget w to samo miejsce widgety
        krecik = QtGui.QPixmap("chodzik1.png")
        wymiarChodzika = int(self.rozmiarOkna_Gl/ self.szerPlanszy)
        krecik = krecik.scaled(wymiarChodzika,wymiarChodzika,QtCore.Qt.KeepAspectRatio)
        krecikL = QtGui.QLabel(self)
        krecikL.setPixmap(krecik)
        self.chodzik = krecikL
        self.aktual_row = int(self.szerPlanszy/2)
        self.aktual_col = int(self.szerPlanszy/2)
        grid.addWidget(self.chodzik,int(self.szerPlanszy/2),int(self.szerPlanszy/2))
        self.board = grid
    
    
    
        # jedzonka
        kopiec = QtGui.QPixmap("kopiec.png") 
        kopiec = kopiec.scaled(wymiarChodzika,wymiarChodzika,QtCore.Qt.KeepAspectRatio)
        kopiecL = QtGui.QLabel(self)
        kopiecL.setPixmap(kopiec)
        self.jedzonko = kopiecL
        self.jedzonkoTimer = QtCore.QBasicTimer()
        czasJedzonka = 3000
        self.jedzonkoTimer.start(czasJedzonka, self)        
        grid.addWidget(self.jedzonko,self.szerPlanszy-2,self.szerPlanszy-2)
        
     

        # do ruchu
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.isStarted = True
                           
                           
    def timerEvent(self, event):
        # timer
        if event.timerId() == self.jedzonkoTimer.timerId():    
            row_jedzonko = random.randint(0, self.szerPlanszy-1)
            col_jedzonko = random.randint(0, self.szerPlanszy-1)
            self.board.addWidget(self.jedzonko, row_jedzonko, col_jedzonko)
                

 # reakcja na wciskanie okreslonych klawiszy
    def keyPressEvent(self, event):
        
        if not self.isStarted:
            super(Plansza, self).keyPressEvent(event)
            return

        key = event.key()
        
        if key == QtCore.Qt.Key_Space:
            return
        elif key == QtCore.Qt.Key_Left:
            self.ruch_krecika("lewo")
        elif key == QtCore.Qt.Key_Right:
            self.ruch_krecika("prawo")
        elif key == QtCore.Qt.Key_Up:
            self.ruch_krecika("gora")
        elif key == QtCore.Qt.Key_Down:
            self.ruch_krecika("dol")


        else:
            super(Plansza, self).keyPressEvent(event)
                 

    def ruch_krecika(self, kierunek):
        
        if kierunek == "lewo":
           # if self.aktual_col == 0:
            #    self.aktual_col = 14
            #else:
             #   self.aktual_col = self.aktual_col - 1
            self.aktual_col = self.aktual_col -1
            if self.aktual_col == -1:
                self.aktual_col = 14
                self.game_over()
            else: #wywal elsa, jak chcesz teleporty na przeciwna strone
                self.board.addWidget(self.chodzik,self.aktual_row,self.aktual_col)
        if kierunek == "prawo":
            self.aktual_col = self.aktual_col +1
            if self.aktual_col == 15:
                self.aktual_col = 0
                self.game_over()
            else:
                self.board.addWidget(self.chodzik,self.aktual_row,self.aktual_col)
        if kierunek == "gora":
            self.aktual_row = self.aktual_row - 1
            if self.aktual_row == -1:
                self.aktual_row = 14
                self.game_over()
            else:
                self.board.addWidget(self.chodzik,self.aktual_row,self.aktual_col)
        if kierunek == "dol":
            self.aktual_row = self.aktual_row + 1
            if self.aktual_row == 15:
                self.aktual_row = 0
                self.game_over()
            else:
                self.board.addWidget(self.chodzik,self.aktual_row,self.aktual_col)
        else:
            return


    def game_over(self):
        self.isStarted = False
        #QtGui.QSound.play("test.wav")
        QtGui.QMessageBox.information(None, "Game over.", "You have lost." )



# napisać funkcje ktora by przesuwala te labelki?  ktora by je wkladala gdie indziej a poprzednia usuwala, problem z dostaniem sie do gridu i labelek                   
                  
                  
def main():
    
    

    app =  QtGui.QApplication(sys.argv)

    # ekran powitalny
    witaj_obraz =  QtGui.QPixmap('tytul.png')
    witaj_ekran =  QtGui.QSplashScreen(witaj_obraz,  QtCore.Qt.WindowStaysOnTopHint)
    witaj_ekran.setMask(witaj_obraz.mask())
    witaj_ekran.show()
    app.processEvents()

    # ile czasu wyswietlac Krecika
    time.sleep(2)
    # uruchomienie glownej aplikacji
    Krtek_apka = Krtek()
    #witaj_ekran.finish(Krtek_apka)

    
    witaj_ekran.close()
    Krtek_apka.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()    
    
    
    
    
    
