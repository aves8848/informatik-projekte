import math
import config
from tabulate import tabulate


# Rundet eine Zahl auf eine Nachkommastelle ab
def truncate(f):
    return math.floor(f * 10 ** 1) / 10 ** 1


# Fragt eine Note ab und validiert, ob sie zwischen 1.0 und 5.0 liegt
def get_valid_grade(fach, notentyp):
    while True:
        try:
            note = float(input(f"{notentyp} im Fach {fach}: "))
            if 1.0 <= note <= 5.0:
                return truncate(note)
            else:
                raise ValueError
        
        except ValueError:
            print("Die Note soll eine Zahl zwischen 1 und 5 sein.")


# Gibt das Zeugnis mit den Fächern und Durchschnittsnote aus
def zeugnis_ausgeben(notentabelle):
    zeilen = [[fach, noten["gesamt"]] for fach, noten in notentabelle.items()]
    durchschnittsnote = sum(noten["gesamt"] for noten in notentabelle.values()) / len(notentabelle)

    zeilen.append(["Durchschnittsnote", round(durchschnittsnote, 1)])

    return f"Zeugnis über die Feststellungsprüfung\n{tabulate(zeilen, headers=["Fach", "Note"], tablefmt="fancy_grid")}"


# Berechnet die Nachklausur für das gegebene Fach
def nachklausur_berechnen(fach, notentabelle):
    config.mundklausur = False
    config.nachklausur = fach
    print(f"Sie haben eine Nachklausur im Fach {fach}.")
    notentabelle[fach]["schriftlich"] = get_valid_grade(fach, "Nachklausur Note")
    notentabelle[fach]["gesamt"] = notentabelle[fach]["muendlich"] = 0.0
    return notentabelle


# Berechnet die mündliche Prüfung für die betroffenen Fächer
def muendliche_berechnen(faecher, notentabelle):
    config.mundklausur = True
    print(f"Sie müssen eine mündliche Prüfung {"im Fach" if len(faecher)==1 else "in Fächern"} {", ".join(faecher)} ablegen.")

    for fach in faecher:
        notentabelle[fach]["muendlich"] = get_valid_grade(fach, "Mündliche Note")

    return notentabelle


# Berechnet die Gesamtbewertung und entscheidet über Nachklausur oder Mündliche
def gesamt_berechnen(notentabelle):
    muendliche = []
    nichtbestanden = []
    muendlichnichtbestanden = []

    # Berechnung der Gesamtbewertung und Ermittlung der Prüfungen
    if not config.mundklausur:
        
        for fach in notentabelle:

            if notentabelle[fach]["gesamt"] == 0.0:
                if notentabelle[fach]["schriftlich"] > 0.0:
                    notentabelle[fach]["gesamt"] =  truncate((notentabelle[fach]["semesternote"] + notentabelle[fach]["schriftlich"]) / 2)
                    
                    if notentabelle[fach]["gesamt"] > 4.0:
                        muendliche.append(fach)
                        nichtbestanden.append(fach)
                        print(f"Sie haben die FSP im Fach {fach} nicht bestanden und müssen Mündliche Prüfung bestehen!")
                    
                    
                    elif abs(notentabelle[fach]["semesternote"] - notentabelle[fach]["schriftlich"]) >= 1.0:
                        muendliche.append(fach)
                        print(f"Es gibt eine Abweichung zwischen Semesternote und Prüfungsnote im {fach} von mehr als einer Note!")
                
                else:
                    notentabelle[fach]["gesamt"] =  notentabelle[fach]["semesternote"]
                    if notentabelle[fach]["gesamt"] > 4.0:
                        nichtbestanden.append(fach)
        
        if len(muendliche) > 0:

            if len(nichtbestanden) > 1:
                config.fsp_bestanden = False
                config.fsp_grund = "In zwei Fächern sind die Semesternote und schriftliche Prüfungsnote nicht ausreichend."
                return notentabelle

            
            notentabelle = muendliche_berechnen(muendliche, notentabelle)
            
            if len(nichtbestanden) == 1:
                if not config.nachklausur:
                    notentabelle = nachklausur_berechnen(nichtbestanden[0], notentabelle)                
                    return gesamt_berechnen(notentabelle)
        
    # Verarbeitung der mündlichen Prüfungen und Nachklausur
    elif config.mundklausur:

        for fach in notentabelle:
            
            if notentabelle[fach]["muendlich"] > 0.0:
                notentabelle[fach]["gesamt"] = truncate((notentabelle[fach]["semesternote"] + notentabelle[fach]["schriftlich"] + notentabelle[fach]["muendlich"]) / 3)
                
                if notentabelle[fach]["gesamt"] > 4.0:
                    muendlichnichtbestanden.append(fach)
                    if config.nachklausur == fach:
                        config.fsp_bestanden = False
                        config.fsp_grund = "Leider haben Sie die Nachklausur im Fach {fach} nicht bestanden"
                        return notentabelle
        
        if len(muendlichnichtbestanden) > 1:
            config.fsp_bestanden = False
            config.fsp_grund = "Nach den mündlichen Prüfungen in mehr als einem Fach ist der Durchschnitt der drei Noten nicht ausreichend."
            return notentabelle
        
        elif len(muendlichnichtbestanden) == 1:
            if not config.nachklausur:
                notentabelle = nachklausur_berechnen(muendlichnichtbestanden[0], notentabelle)
                return gesamt_berechnen(notentabelle)

    # Überprüfung, ob Fächer mit nicht bestandener Gesamtnote vorhanden sind
    for fach in notentabelle:
        if notentabelle[fach]["gesamt"] > 4.0:
            config.fsp_bestanden = False
            config.fsp_grund = "Die Gesamtbewertung in einem oder mehreren Fächern ist nicht ausreichend."
            return notentabelle
    
    return notentabelle


def main():
    # Initialisiert die Noten für die Fächer
    noten = {
        "Deutsch": {"semesternote": 0.0, "schriftlich": 0.0, "muendlich": 0.0, "gesamt": 0.0},
        "Mathematik": {"semesternote": 0.0, "schriftlich": 0.0, "muendlich": 0.0, "gesamt": 0.0},
        "Physik": {"semesternote": 0.0, "schriftlich": 0.0, "muendlich": 0.0, "gesamt": 0.0},
        "Informatik": {"semesternote": 0.0, "schriftlich": 0.0, "muendlich": 0.0, "gesamt": 0.0}}

    # Fragt die Semesternoten für alle Fächer ab
    for fach in noten:
        noten[fach]["semesternote"] = get_valid_grade(fach, "Semesternote")


    # Validierung der Fächer für die schriftliche Prüfung
    n = 0

    while n != 1:
        fsp_geschrieben = input("In welchen Fächer haben sie FSP geschrieben? ").capitalize().replace(" ", "").split(",")
        fsp_geschrieben = [i.capitalize() for i in fsp_geschrieben]

        if ("Deutsch" not in fsp_geschrieben or "Mathematik" not in fsp_geschrieben) or ("Informatik" in fsp_geschrieben and "Physik" in fsp_geschrieben):
                    print("Sie müssen Deutsch und Mathematik als Pflichtfach schriftlich bestehen und können nicht gleichzeitig Informatik und Physik schreiben.")
    
        else:
            for fach in fsp_geschrieben:
                if isinstance(fach, str) and fach in noten.keys() and len(fsp_geschrieben) == 3:
                    noten[fach]["schriftlich"] = get_valid_grade(fach, "Schriftliche FSP")
                    n = 1

    # Berechnet die Gesamtnoten und gibt das Ergebnis aus
    result = gesamt_berechnen(noten)

    if config.fsp_bestanden:
        print(zeugnis_ausgeben(result))

    else:
        print(f"Sie haben die FSP nicht bestanden. \nGrund: {config.fsp_grund}")


if __name__ == "__main__":
    main()
