def berechnen(notentabelle):
    for fach in notentabelle:
        notentabelle[fach]["gesamt"] =  (notentabelle[fach]["semesternote"] + notentabelle[fach]["schriftlich"]) / 2
    
    return notentabelle
def main():
    noten = {
        "Deutsch": {"semesternote": 0.0, "schriftlich": 0.0, "muendlich": 0.0, "gesamt": 0.0},
        "Mathematik": {"semesternote": 0.0, "schriftlich": 0.0, "muendlich": 0.0, "gesamt": 0.0},
        "Physik": {"semesternote": 0.0, "schriftlich": 0.0, "muendlich": 0.0, "gesamt": 0.0},
        "Informatik": {"semesternote": 0.0, "schriftlich": 0.0, "muendlich": 0.0, "gesamt": 0.0}}
    while True:
        try:
            for fach in noten:
                noten[fach]["semesternote"] = float(input(f"Note im Fach {fach}: "))
            n = 0
            while n != 1:
                fsp_geschrieben = input("In welchen Fächer haben sie FSP geschrieben? ").replace(" ", "").split(",")
                for fach in fsp_geschrieben:
                    if isinstance(fach, str) and fach in [fach for fach in noten] and len(fsp_geschrieben) == 3:
                        noten[fach]["schriftlich"] = float(input(f"Schriftliche FSP im Fach {fach}: "))
                        n = 1
            print(berechnen(noten))
        except ValueError:
            print("Die Note soll eine Zahl sein.")
        

if __name__ == "__main__":
    main()