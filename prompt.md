# Prompts used to generate the Programm

I generated this project using githup copilot. Therefore I used following prompts:

## Initial

Erstelle ein python Programm, dem mittels Kommdozeilenparameter einer CSV Datei sowie ein Startzeitpunkt und ein Entzeitpunkt übergeben wird. Startzeitpunkt und Endzeitpunkt sind optionale parameter, die CSV Datei muss immer angegeben werden.
Die CSV Datei enthält Blutdruckdaten im Format CSV. Als Beispiel kannst Du die Datei bloodPressure.csv ansehen. Die erste Zeile der CSV Datei enthält überschriften und muss ignoriert werden. Die Folgenden Zeilen enthalten jeweils eine Zeitstempel, den systolischen Blutdruck, den diastolischen Blutdruck und den Puls. Lade die Daten aus der Datei in eine Liste und nenne sie bloodpressure_complete.
Sortiere die Daten in bloodpressure_complete nach den Zeitstempeln.
Falls ein Startzeitpunkt übergeben wurde, so entferne alle Daten aus bloodpressure_complete, deren Zeitstempel davor liegt.
Falls ein Endzeitpunkt erstellt wurde, so entferne alle Daten aus bloodpressure_complete, deren Zeitstempel später ist.
Erstelle eine weitere Liste mit dem Namen bloodpressure_morning, welche jeweils den ersten Blutdruckwert eines Tages enthält. Entferne alle Daten aus bloodpressure_morning, die vor 4:00 oder nach 12:00 Uhr eines Tages liegen.
Erstelle eine weitere Liste mit dem Namen bloodpressure_evening, welche jeweils den letzten Blutdruckwert eines Tages enthält. Entferne alle Daten aus bloodpressure_evening, die vor 18:00 liegen.
Erstelle jeweils ein Liniendiagramm für die Daten aus bloodpressure_complete, bloodpressure_morning und bloodpressure_evening, welches den systolischen Blutdruck, den Diastolischen Blutdruck und den Puls für die jeweiligen Zeitstempel anzeigt. Speicher diese diese Diagramme als SVG Dateien mit den namen bloddpressure_complee.svg, bloodpressure_morning.svg und bloodpressure_evening.svg. Erstelle ein PDF Dokument im DIN A4 Format und füge die Diagramme auf jeweils einer Seite ein, so dass sie seitenfüllend im Queerformat dargestellt werden.
Erstelle ein Diagramm, in dem der durchschnittliche Blutdruck und die Standardabweichung für bloodpressure_complete, bloodpressure_morning und bloodpressure_evening dargestellt wird. Speichere das Diagramm als SVG Datei mit dem Namen cluudpressure_average.svg. Füge das Diagramm auch als neue Seite in die PDF Datei ein.
Füge neue Seiten in das PDF Dokument ein, auf denen Du die Daten aus bloodpressure_complete als Tabelle darstellst. Die Tabelle soll als erste Sparte die die Überschriften enthalten, also "Zeitstempel", "SYS", "DIA" und "Puls". Makiere die Daten, die auch in bloodpressure_morning sind, indem Du sie in einem hellen Gelb hinterlegst. Makiere die Daten, die auch in bloodpressure_evening sind, indem Du sie in einem hellen Orange hinterlegst. Füge nach der Tabelle eine Legende ein, welche diese Farben erklärt.
Versiehe das PDF Dokument mit einer Startseite, welche in 24 Punkt Schriftgröße und horozontal und vertikal zentrirt den Text "Blutdruckdaten Sascha Effert" enthält. Falls der Startzeitpunkt per Kommdozeile angegeben wurde, so füge ihn der Startseite hinzu, andernfalls füge den Zeitstempel des ersten Zeitstempels aus bloodpressure_complete hinzu. Falls der Endzeitpunkt per Kommdozeile angegeben wurde, so füge ihn der Startseite hinzu, andernfalls füge den Zeitstempel des letzten Zeitstempels aus bloodpressure_complete hinzu.
Spreichere das PDf inder dem Namen bloodpressure.pdf.
Erstelle ein bash Skript, welches ein python virtual environment erstellt, diesem alle python Pakete hinzufügt, welche zur Ausführung notwendig sind und das Programm startet, indem es seine Kommndozeilenparameter weiter leitet.

## Diagramms were missing

In der PDF Datei fehlen die Diagramme. Stattdessen steht dort jeweils der Name der SVG Dateien. Bitte korrigiere das.

## Diagramm comparing morning and evening Data

Bitte erstelle ein weiteres Diagramm, welche die die Blutdruckdaten aus bloodpressure_morning und bloodpressure_evening enthält. Spreiche es als bloodpressure_moning_evening.svg und erstelle in dem PDF Dokument eine neue Seite mit dem Diagramm, seitenfüllend im Querformat. Die Seite soll vor der Tabelle mit den Daten eingefügt werden.

## Remove single Diagramms for morning and evening

Ich möchte die beiden Diagramme, welche die Daten aus bloodpressure_morning und bloodpressure_evening enthalten, nicht in dem PDF Dokument haben. Nur die gerade ninzugrfügte Seite mit den Kurven aus beiden Listen soll bleiben.

## change Order

Bitte verschiebe die Seite mit den durchschnittlichen Blutdruckwerten hinter die Seite mit den Werten für morgens und abends.

## All pages in DIN A4 landscape

Bitte stelle sicher, dass alle Seiten im PDF Dokument im DIN A4 Querformat sind.

## Change wrong filename (because of typo in first prompt)

Die SVG Datei mit den durchschnittlichen Daten soll bloodpressure_average.svg heißen, nicht cluudpressure_average.svg.

## Create Testdata as I do not to upload my own ones

Bitte erstelle eine Datei bloodpressure_example.csv mit generierten Testdaten, welche sich gut zum Testen eignen.

## Create .gitignore

Erstelle eine Datei .gitignore und trage alles ein, was sinnvollerweise nicht mit in das git repository soll.

## Do git commit

Füge mittels git add die Dateien dem git repository hinzu und erstelle einen git commit mit einer gute commit message.

## push to github (here I had to some things manually)

Erstelle auf github ein Projekt bloodpressure_analyzor, verbinde es mit diesem git repository und synchronisiere die Daten von hir zu github.

## Add values to average diagramm

Bitte schreibe bei den durchschnittlichen Blutdruckswerten jeweils den Durchschnittswert in die Balken.

## Add value of std variation to average diagramm

Bitte schreibe bei den durchschnittlichen Blutdruckswerten auch die Standardabweichung in die Balken.

## Check in

Füge die Änderungen wieder zum git hinzu, erstelle dazu eine gute commit message und synchronisiere die Änderungen zu github.

## Change diagramm filename (another typo in first prompt)

Die SVG Datei mit den Diagramm der daten aus bloodpressure_complete soll bloodpressure_complete.svg heißen, nicht bloddpressure_complee.svg.

## Check in

Füge die Änderungen wieder zum git hinzu, erstelle dazu eine gute commit message und synchronisiere die Änderungen zu github.

## Legend overwritten

Wenn die Tabelle mit den Daten zu lang wird, dann wir die Legende aktuell in den Text gedruckt. Bitte stelle sicher, dass die Legende immer unter der Tabelle dargestellt wird. Falls auf der letzten Seite kein Platz mehr ist, dann soll sie auf die nächste Seite gedruckt werden.

## Legend only on last page

Die Legende soll nur auf der letzten Seite erscheinen.

## Higher rows on last page

Auf der letzten Seite sind die Zeilen der Tabelle nun höher als auf den Seiten davor. Die Tabelle scheint den Raum auf der letzten Seite ausfüllen zu wollen. Bitte sorge dafür, dass auch die Zeilen auf der letzten Seite die gleichen Zeilenhöhe habe wie auf den Seiten davor.

## Still higher rows on last page

Nein, die Zeilen auf der letzten Seite sind immernoch höher, als auf den Seiten davor.

## Remove bordering for empty cells

Kannst Du bei den leeren Zellen die Umrandung entfernen?

## Check in

Bitte checke die Daten wieder mit einer guten commit message in git ein und synchronisiere die Änderungen zu github.

## Clean up code

Warum hast Du eigene Methoden zum erzeugen der Diagramm für die SVG und PDF Dateien erstellt?

## Did not like to create figure two times, even using same code

Könntest Du die SVG-Datei nicht auch einfach in _create_chart_for_pdf erzeugen, so dass der Code aus _create_base_chart nur einmal aufgerufen würde?

## Remove unused figures (in svg) and clean up code

Ich brauche die Dateien bloodpressure_evening.svg und bloodpressure_morning.svg nicht mehr. Du kannst den Code, der zu deren Erzeugung da war, auch entfernen.

## Check in

Bitte checke die Daten wieder mit einer guten commit message in git ein und synchronisiere die Änderungen zu github.
