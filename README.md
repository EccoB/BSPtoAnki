# BSPtoAnki
Pythonskript dass Fragen von bootsfuehrerschein-portal.de in ein Anki Deck wandelt zum mobilen lernen. 

In dem gebuchten Kurs bei bootsfuehrerschein-portal.de können online im Browser Fragen für das Bodenseeschifferpatent gelernt werden. Möchte man das allerdings mobil und auf täglicher Basis machen ist es praktischer das Ganze mit der Karteikartenapp Anki zu lernen. Dieses Pythonskript erstellt ein solches Anki-Deck aus der vorher manuell rauskopierten JSON-COde von der Website und ergänzt dieses mit den passenden Bilder.

# Usage
- Es wird ein gültiger Account benötigt bei bootsfuehrerschein-portal.de
- Das Skript benötigt die Fragen, diese müssen _manuell_ runtergeladen und als JSON-File gespeichert werden.
- Die entsprechenden Daten findet man nach dem Aufruf der Übung im Portal mit dem Browser in der Variable _selectedQuestions_ im File _wbtpackage.js_ (Hier als Bsp: https://www.bootsfuehrerschein-portal.de/mandant/0/content/bsp-scorm12-de/de/sys/js/wbtpackage.js)
- Export als JSON-File und lokal speichern
- Start das Python Sykript mit python bspToAnki.py [JSON] [ANKIOUTPUT]
