import math
import config
from tabulate import tabulate

def truncate(f):
    return math.floor(f * 10 ** 1) / 10 ** 1

def zeugnis_ausgeben(notentabelle):
    zeilen = []
    for fach, noten in notentabelle.items():
        zeilen.append([fach, noten["gesamt"]])

    gesamtnoten = [noten["gesamt"] for noten in notentabelle.values()]
    durchschnittsnote = sum(gesamtnoten) / len(gesamtnoten)

    zeilen.append(["Durchschnittsnote", round(durchschnittsnote, 1)])

    return f"Zeugnis über die Feststellungsprüfung\n{tabulate(zeilen, headers=["Fach", "Note"], tablefmt="grid")}"

def muendliche_berechnen(faecher, notentabelle):
    config.mundklausur = True
    print(f"Sie müssen eine mündliche Prüfung {"im Fach" if len(faecher)==1 else "in Fächern"} {", ".join(faecher)} ablegen.")
    for fach in faecher:
        while True:
            try:
                muendlichenote = float(input(f"Muendliche Note im Fach {fach}: "))
                if 1.0 <= muendlichenote <= 5.0:
                    notentabelle[fach]["muendlich"] = truncate(muendlichenote)
                    break
                else: 
                    raise ValueError
            except ValueError:
                print("Die Note soll eine Zahl zwischen 1 und 5 sein.")
    return notentabelle

def gesamt_berechnen(notentabelle):
    muendliche = []
    nichtbestanden = []
    muendlichnichtbestanden = []
    if not config.mundklausur:
        
        for fach in notentabelle:

            if notentabelle[fach]["schriftlich"] > 0.0:
                notentabelle[fach]["gesamt"] =  truncate((notentabelle[fach]["semesternote"] + notentabelle[fach]["schriftlich"]) / 2)
                
                
                if notentabelle[fach]["gesamt"] > 4.0:
                    muendliche.append(fach)
                    nichtbestanden.append(fach)
                    print(f"Sie haben die FSP im Fach {fach} nicht bestanden und müssen Mündliche Prüfung bestehen!")
                
                
                if abs(notentabelle[fach]["semesternote"] - notentabelle[fach]["schriftlich"]) >= 1.0:
                    muendliche.append(fach)
                    print(f"Es gibt eine Abweichung zwischen Semesternote und Prüfungsnote im {fach} von mehr als einer Note!")
            
            else:
                notentabelle[fach]["gesamt"] =  notentabelle[fach]["semesternote"]
        
        
        if len(muendliche) > 0:
            
            if len(nichtbestanden) >= 2:
                config.fsp_bestanden = False
                config.fsp_grund = "In zwei sind die Semesternote und schriftliche Prüfungsnote nicht ausreichend."
                return
            else:
                notentabelle = muendliche_berechnen(muendliche, notentabelle)
                return gesamt_berechnen(notentabelle)
    
    elif config.mundklausur:

        for fach in notentabelle:
            if notentabelle[fach]["muendlich"] > 0.0:  # Проверяем, если устные оценки есть
                notentabelle[fach]["gesamt"] = truncate((notentabelle[fach]["semesternote"] + notentabelle[fach]["schriftlich"] + notentabelle[fach]["muendlich"]) / 3)
                if notentabelle[fach]["gesamt"] > 4.0:
                    muendlichnichtbestanden.append(fach)
        if len(muendlichnichtbestanden) > 1:
            config.fsp_bestanden = False
            config.fsp_grund = "Nach den mündlichen Prüfungen in mehr als einem Fach ist der Durchschnitt der drei Noten nicht ausreichend."
            return
        
        return notentabelle

def main():
    noten = {
        "Deutsch": {"semesternote": 0.0, "schriftlich": 0.0, "muendlich": 0.0, "gesamt": 0.0},
        "Mathematik": {"semesternote": 0.0, "schriftlich": 0.0, "muendlich": 0.0, "gesamt": 0.0},
        "Physik": {"semesternote": 0.0, "schriftlich": 0.0, "muendlich": 0.0, "gesamt": 0.0},
        "Informatik": {"semesternote": 0.0, "schriftlich": 0.0, "muendlich": 0.0, "gesamt": 0.0}}


    for fach in noten:
        while True:
            try:
                semesternote = float(input(f"Note im Fach {fach}: "))
                if 1.0 <= semesternote <= 5.0:
                    noten[fach]["semesternote"] = truncate(semesternote)
                    break
                else: 
                    raise ValueError
            except ValueError:
                print("Die Note soll eine Zahl zwischen 1 und 5 sein.")
    n = 0
    while n != 1:
        fsp_geschrieben = input("In welchen Fächer haben sie FSP geschrieben? ").capitalize().replace(" ", "").split(",")
        fsp_geschrieben = [i.capitalize() for i in fsp_geschrieben]
        if ("Deutsch" not in fsp_geschrieben or "Mathematik" not in fsp_geschrieben) or ("Informatik" in fsp_geschrieben and "Physik" in fsp_geschrieben):
                    print("Sie müssen Deutsch und Mathematik als Pflichtfach schriftlich bestehen und können nicht gleichzeitig Informatik und Physik schreiben.")
        else:
            for fach in fsp_geschrieben:
                if isinstance(fach, str) and fach in [fach for fach in noten] and len(fsp_geschrieben) == 3:
                    while True:
                        try:
                            schriftlichenote = float(input(f"Schriftliche FSP im Fach {fach}: "))
                            if 1.0 <= schriftlichenote <= 5.0:
                                noten[fach]["schriftlich"] = truncate(schriftlichenote)
                                break
                            else: 
                                raise ValueError
                        except ValueError:
                            print("Die Note soll eine Zahl zwischen 1 und 5 sein.")
                    n = 1
    result = gesamt_berechnen(noten)
    if config.fsp_bestanden:
        print(zeugnis_ausgeben(result))
    else:
        print(f"Sie haben die FSP nicht bestanden. \nGrund: {config.fsp_grund}")
        

if __name__ == "__main__":
    main()

# Nachklausuren
# Eine verschieden Funktion für Input