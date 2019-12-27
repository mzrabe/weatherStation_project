#!/usr/bin/python
#-*- coding: utf-8 -*-

# Beaufort-Scalar
# Beaufort number [Btf], (max) wind velocity [m/s], description, visible effect (land), visible effect (see)


BEAUFORT_SCALAR = [
    [0,0.3,'Stille','Rauch steigt senkrecht empor','spiegelglatte See'],
    [1,1.6,'leichter Zug','Windrichtung angezeigt durch den Zug des Rauches','leichte Kraeuselwellen'],
    [2,3.4,'leichte Brise','Wind im Gesicht spuerbar, Blaetter und Windfahnen bewegen sich','kleine, kurze Wellen, Oberflaeche glasig'],
    [3,5.5,'schwache Brise','Wind bewegt duenne Zweige und streckt Wimpel','Schaumkronen bilden sich auf Seen'],
    [4,8.0,'maeßige Brise','Zweige bewegen sich loses Papier wird vom Boden gehoben','kleine, laenger werdende Wellen, recht regelmaeßige Schaumkoepfe'],
    [5,10.8,'frische Brise','groeßere Zweige und Bäume bewegen sich, Wind deutlich hoerbar','maeßige Wellen von großer Laenge, ueberall Schaumkoepfe'],
    [6,13.9,'starker Wind','starke Aeste schwanken, Regenschirme sind nur schwer zu halten, Telegrafenleitungen pfeifen im Wind','groeßere Wellen mit brechenden Koepfen, überall weiße Schaumflecken'],
    [7,17.2,'steifer Wind','fühlbare Hemmungen beim Gehen gegen den Wind, ganze Baeume bewegen sich','weißer Schaum von den brechenden Wellenkoepfen legt sich in Schaumstreifen in die Windrichtung '],
    [8,20.8,'struemischer Wind','Zweige brechen von Baeumen, erschwert erheblich das Gehen im Freien','ziemlich hohe Wellenberge, deren Koepfe verweht werden, überall Schaumstreifen'],
    [9,24.5,'Sturm','Aeste brechen von Baeumen, kleinere Schaeden an Haeusern (Dachziegel oder Rauchhauben abgehoben)','hohe Wellen mit verwehter Gischt, Brecher beginnen sich zu bilden'],
    [10,28.5,'schwerer Sturm','Wind bricht Baeume, groeßere Schaeden an Haeusern','sehr hohe Wellen, weiße Flecken auf dem Wasser, lange, ueberbrechende Kaemme, schwere Brecher'],
    [11,32.7,'orkanartiker Sturm','Wind entwurzelt Baeume, verbreitet Sturmschaeden','bruellende See, Wasser wird waagerecht weggeweht, starke Sichtverminderung'],
    [12,37.0,'Orkan','schwere Verwuestungen','See vollkommen weiß, Luft mit Schaum und Gischt gefuellt, keine Sicht mehr']
]

BTF_NUMBER = 0
WIND_VELOCITY = 1
DESCRIPTION = 2
VIS_EFFECT_LAND = 3
VIS_EFFECT_SEE = 4

def fetchIndex(v):
    if v < 0.0:
        return -1
    if v >= 0.0 and v < BEAUFORT_SCALAR[0][WIND_VELOCITY]:
        return 0
    if v >= BEAUFORT_SCALAR[-1][WIND_VELOCITY]:
        return len(BEAUFORT_SCALAR)-1

    for i in range(1,len(BEAUFORT_SCALAR)):
        if v >= BEAUFORT_SCALAR[i-1][WIND_VELOCITY] and v < BEAUFORT_SCALAR[i][WIND_VELOCITY]:
            return i

def calcBtf(v):
    return round((v/0.836)**(0.66666666666666666667)-0.5)

if __name__ == '__main__':
	velocity = 20
	print BEAUFORT_SCALAR[fetchIndex(velocity)]
	print calcBtf(velocity)
