# Magic Compiler
![Alt Text](https://media.giphy.com/media/12NUbkX6p4xOO4/giphy.gif)


Hier stellen wir den Compiler der neuen Programmiersprache *Magic* vor!

In Zusammenarbeit mit:

* [Butterbee1609](https://github.com/butterbee1609)
* [bene77](https://github.com/bene77)

# Vorraussetzungen
Python 3.x muss intalliert sein. 

# Aufruf
python compiler.py filename.magic

# Programm
Das Programm muss mit der Datei Dateiname.magic geschrieben werden.

# Magic
Um eine Funktion zu definieren, muss das Wort "magic" vor dem Funktionsnamen geschrieben sein. Siehe Beispiel:

# Funktionalität von Magic
## Verfügbare Operationen
```
+ Addition
- Subtraktion
/ Division
* Multiplikation
% Modulo

#===========================

&& Logisches UND
|| Logisches ODER
< Kleiner
> Größer
== Logisches GLEICH
!= Logisches UNGLEICH
```
## Variablen Deklaration
```
a = 3;
b = 3 * 4; 
c = true;
d = true && false;
e = 5 * (b - 2);
```
## Funktions Deklaration & Aufruf

### mit Funktionsparametern
```
magic simple_add(a, b)
{
  c = a + b;
  return c;
}

a = 10;
b = 20;

simple_add(a, b);
```
### ohne Funktionsparameter
```
magic give_me_five()
{
  return 5;
}

x = give_me_five();
```

## Conditional Statements
```
if (2 < 3)
{
  x = 10;
}else{
  x = 20;
}
```
```
a = true;
b = false;

if( a || b)
{
  c = true;
}else{
  c = false;
}
```
# Beispiel
### Fakultät berechnen (Rekursion)
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
