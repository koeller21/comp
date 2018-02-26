# Magic Compiler
Hier stellen wir den Compiler der neuen Programmiersprache *Magic* vor!

# Vorraussetzungen
Python 3.x muss intalliert sein. 

# Aufruf
python compiler.py

# Programm
Das Programm muss mit der Datei  Dateiname.magic geschrieben werden.

# Magic
Um eine Funktion zu definieren, muss das Wort "magic" vor dem Funktionsnamen geschrieben sein. Siehe Beispiel:
  
# Beispiel
### Fakultät berechnen
```
magic fac(n){
  if( n == 1){
    return 1;
  }else{
    a = n - 1;
    k = fac(a);
    x = k * n;
    return x;
  }
}

i = 5;
res = fac(i);
```


# Grammatik
Die funktionale Programmiersprache die wir bauen werden heißt Magic. Alle notwendigen Grammatik Daten vom aktuellen Stand befinden sich in dem File grammatik.txt
