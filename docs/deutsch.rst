SAUCE Dokumentation
===================

Kurzeinführung
------------------

SAUCE kurz zusammengefasst:
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Du bist als *Student* einem *Team* angehörig, das einer Übungsgruppe (*Lesson*) zugeordnet ist, welche von einem Übungsleiter (*Teacher*) gehalten wird. 
Dieser Übungsleiter korrigiert deine Abgaben (*Submissions*).

Wenn du eine Abgabe einsendest wird diese auch schon automatisch
geprüft, mit Testdaten, die der Oberassistent der Veranstaltung
vorbereitet hat.

Dadurch erhälst du direkt beim Abgeben eine Rückmeldung, ob dein 
Programm tut, was es soll, oder nicht.
Der Übungsleiter hat es bei der Korrektur auch einfacher, denn
er sieht ebenfalls direkt ob das Programm die Aufgabenstellung
erfüllt, oder nicht.

SAUCE soll und kann nicht die Übungsleiter aus Fleisch und Blut ersetzen, denn manchmal kommt es nicht (nur) auf stupide Korrektheit an, sondern auch auf die Qualität des Quellcodes, o.ä.

    **Deshalb:** Nicht verzweifeln wenn der automatische Test einer Abgabe fehlschlägt! Deine Abgabe ist gespeichert und wird dem Übungsleiter in jedem Fall angezeigt, so dass er sie bewerten kann.

Eine ganze Veranstaltung (*Event*) wird ebenfalls von einem
Teacher betreut (Oberassistent). Dieser erstellt die Übungsblätter (*Sheets*), Aufgaben (*Assignments*) und die zugehörigen Tests.

Die *Submission*-Seite
""""""""""""""""""""""
Auf der *Submission*-Seite hast du die Möglichkeit, deinen Quellcode entweder  als Datei hochzuladen oder ihn in das Textfeld einzufügen.
Je nach verwendeter Programmiersprache ist es wichtig, den Dateinamen anzugeben (z.B. muss bei Java der Dateiname dem Klassennamen entsprechen).

    **Wichtig**: Der gesamte Quellcode pro Abgabe muss in **einer** Datei vorliegen. Vor allem bei Java ist darauf zu achten, **keine** ``package``-Deklaration zu verwenden.

Die drei Buttons auf der *Submission*-Seite haben folgende Funktionen:

**Test**
    Der Test-Button sendet deine Abgabe an den Server, kompiliert sie (falls nötig) und testet das Programm mit den definierten, sichtbaren Testfällen (die du auf der *Assignment*-Seite siehst).
    Die Ausgabe deines Programmes wird dir im Vergleich zur erwarteten Ausgabe des Testfalles als `Diff <http://en.wikipedia.org/wiki/Diff#Unified_format>`_ angezeigt.
    
        Auch wenn der Test **nicht** erfolgreich war, ist deine *Submission* auf dem Server gespeichert! Deshalb: Nicht in Panik geraten, sondern Ausgabe anschauen und das Programm debuggen.

        - Falls du der Meinung bist, dass dein Programm korrekt, aber der *Test* falsch ist, sende eine eMail an den Oberassistenten der Veranstaltung.
        - Falls du der Meinung bist, dass SAUCE etwas falsch macht, schreibe eine eMail an `Moritz Schlarb <mailto:moschlar@students.uni-mainz.de>`_

**Finish**
    Der Finish-Button markiert deine Abgabe als fertig, du kannst sie dann nicht mehr bearbeiten.
    SAUCE testet deine Abgabe nun auch mit weiteren, unsichtbaren Testfällen (falls vorhanden) und gibt dir Rückmeldung, ob dein Programm diese auch erfolgreich berechnet hat oder nicht.
   
        Auch hier gelten die selben Anmerkungen wie beim Test-Button: Keine Panik wenn SAUCE sagt, dass deine Lösung falsch wäre.
        Debugge dein Programm und erstelle einfach eine neue Submission bis es funktioniert.

**Delete**
    Ein Klick auf den Delete-Button löscht deine Abgabe.
    Es gibt keine Möglichkeit, dies rückgängig zu machen.

