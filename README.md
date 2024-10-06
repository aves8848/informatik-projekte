Studienkolleg Informatikprojekt (2. Semester)

Dieses Programm wurde im Rahmen des zweiten Semesters im Studienkolleg am KIT entwickelt. Es dient der Berechnung der Endnoten basierend auf den Semesternoten und den Klausurnoten der Feststellungsprüfung (FSP) für die jeweiligen Fächer. Das Programm berücksichtigt verschiedene Prüfungsszenarien, einschließlich der speziellen Regelungen für externe Prüflinge sowie der Befreiung von der Deutschprüfung.

Hauptfunktionen des Programms:

[+] Eingabe der Noten: Das Programm ermöglicht die Eingabe der Semesternoten und der schriftlichen Prüfungsnoten für alle relevanten Fächer.

[+] Automatische Berechnung: Es wird der Durchschnitt aus den Semesternoten und Prüfungsnoten gebildet. Dabei wird die spezielle Rundungsregel beachtet, bei der die Note nach der ersten Nachkommastelle abgeschnitten wird (z.B. wird aus 4,27 eine 4,2).

[+] Mündliche Prüfungen: Falls eine schriftliche Prüfungsnote unzureichend ist oder eine große Abweichung zwischen Semester- und Prüfungsnote besteht, wird automatisch eine mündliche Prüfung in diesem Fach angesetzt. Diese wird ebenfalls in die Berechnung der Endnote einbezogen.

[+] Nachprüfung: Falls nach einer mündlichen Prüfung in einem Fach die Endnote immer noch unzureichend ist, wird eine Nachprüfung organisiert. Das Programm berücksichtigt dabei den gesamten Prüfungsverlauf, inklusive der Wiederholungsprüfungen.

[+] Sonderfälle für Externe: Externe Prüflinge (ohne Semesternoten) haben besondere Prüfungsregelungen, bei denen die schriftlichen Prüfungsnoten doppelt zählen. Das Programm ist in der Lage, diesen Sonderfall korrekt zu verarbeiten.

Beispielhafte Prüfungsabläufe:

Eine mündliche Prüfung muss abgelegt werden, wenn der Durchschnitt der Semester- und Klausurnoten nicht ausreichend ist (Note ≥ 4,0).
Externe Prüflinge haben keine Semesternoten, daher zählen die schriftlichen Prüfungen doppelt. Falls die schriftliche Note unzureichend ist (unter 3,5), wird zusätzlich eine mündliche Prüfung in diesem Fach notwendig.
Das Programm berücksichtigt auch Fälle, in denen eine Befreiung von der Deutschprüfung vorliegt.

Technische Details:

[+] Programmiersprache: Python

[+] Eingaben: Semesternoten und Klausurnoten für die Fächer Deutsch, Mathematik, Physik und Informatik (bzw. Chemie)

[+] Ausgaben: Endnoten pro Fach und Gesamtbewertung der Feststellungsprüfung (Bestanden / Nicht bestanden)


Entwickelt von: Vsevolod Iorhov

Auftraggeber: Dozent Thomas Stirner, Studienkolleg am KIT

Projekt abgeschlossen am: 01.10.2024
