# README dla Krtek.py
0. W tym repo znajduje się plik README.md, który właśnie czytasz, jeden skrypt pythonowy Krtek.py (z kodem gry) i obrazki, niezbędne do krecikowania.
1. (Instrukcja dla przyszłej mnie) W Linuxie uruchamiamy program w konsoli poleceniem ./Krtek.py (gdy znajdujemy 
sie w folderze z tym skryptem, lub podajac cala sciezke zamiast ./), uprzednio
nadajac sobie prawa do zabawy z tym skryptem: chmod u+x Krtek.py

2. Gra Krtek to czeska wersja snake'a, który był popularny za czasów moich pierwszych telefonów komórkowych.

3. Zasady:
    - wyjście poza planszę kończy grę,
    - wejście na swój krecikoczłon również kończy grę
    - wejście na krecikokopca dodaje krecikoczłon (i 1 punkt do wyniku) oraz zwiększa szybkość gry
    - krecikowąż (vel krecikochodzik) porusza sie automatycznie, my za pomocą
      strzałek możemy mu nadać kierunek, przy czym kierunek ten nie może być
      odwrotny do obecnego (krecikowąż nie wejdzie za siebie, w siebie - jak 
      zwał tak zwał),
    - naszym zadaniem jest zebranie jak największej ilości punktów (krecikokopców)
      omijając przy tym brzegi zielonego poletka i własne krecikoczłony (nie dopuszczam
      krecikokanibalizmu).
    - trudność gry polega na tym, że im więcej jest krecikoczłonów na planszy tym trudniej na nie nie wpaść
      (mniej wolnych pól + co raz większa szybkość gry)
    - spacja służy do pauzowania gry
      
4. PS. nie znam języka bratanków krecika, więc ewentualne błędy zwalam na Mr. Google.
