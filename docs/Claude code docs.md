> [!NOTE]
> # Claude Code overview

> Erfahren Sie mehr über Claude Code, Anthropics agentenbasiertes Programmiertool, das in Ihrem Terminal lebt und Ihnen hilft, Ideen schneller als je zuvor in Code umzusetzen.

## In 30 Sekunden loslegen

Voraussetzungen: [Node.js 18 oder neuer](https://nodejs.org/en/download/)

```bash
# Install Claude Code
npm install -g @anthropic-ai/claude-code

# Navigate to your project
cd your-awesome-project

# Start coding with Claude
claude
```

Das war's! Du bist bereit, mit Claude zu programmieren. [Weiter mit Quickstart (5 Min.) →](/de/docs/claude-code/quickstart)

(Haben Sie spezielle Einrichtungsbedürfnisse oder Probleme mit Treffern? Siehe [advanced setup](/de/docs/claude-code/setup) oder [troubleshooting](/de/docs/claude-code/troubleshooting).)

## Was Claude Code für Sie tut

* **Funktionen aus Beschreibungen erstellen**: Sagen Sie Claude in einfachem Englisch, was Sie bauen wollen. Es wird einen Plan erstellen, den Code schreiben und sicherstellen, dass er funktioniert.

* **Probleme beseitigen und beheben**: Beschreiben Sie einen Fehler oder fügen Sie eine Fehlermeldung ein. Claude Code wird Ihre Codebasis analysieren, das Problem identifizieren und eine Lösung implementieren.

* **Navigieren in jeder Codebasis**: Stellen Sie Fragen zur Codebasis Ihres Teams, und Sie erhalten eine durchdachte Antwort. Claude Code behält den Überblick über Ihre gesamte Projektstruktur, kann aktuelle Informationen aus dem Web finden und mit [MCP](/de/docs/claude-code/mcp) auf externe Datenquellen wie Google Drive, Figma und Slack zugreifen.

* **Automatisieren Sie lästige Aufgaben**: Beheben Sie knifflige Lint-Probleme, lösen Sie Merge-Konflikte und schreiben Sie Versionshinweise. Erledigen Sie all dies mit einem einzigen Befehl von Ihren Entwicklungsrechnern aus oder automatisch in CI.

## Warum Entwickler Claude Code lieben

**Arbeitet in Ihrem Terminal**: 

Kein weiteres Chat-Fenster. Keine weitere IDE. Claude Code trifft Sie dort, wo Sie bereits arbeiten, mit den Tools, die Sie bereits lieben.

**Tut etwas**: 

Claude Code kann Dateien direkt bearbeiten, Befehle ausführen und Übertragungen erstellen. Brauchen Sie mehr? mit [MCP](/de/docs/claude-code/mcp) kann Claude Ihre Entwurfsdokumente in Google Drive lesen, Ihre Tickets in Jira aktualisieren oder *Ihre* benutzerdefinierten Entwicklerwerkzeuge verwenden.

**Unix-Philosophie**: 

Claude Code ist komponierbar und skriptfähig. `tail -f app.log | claude -p "Slack me if you see any anomalies appear in this log stream"` *arbeitet*. Ihr CI kann `claude -p "Wenn es neue Textstrings gibt, übersetze sie ins Französische und erhebe einen PR für das @lang-fr-team zur Überprüfung"` ausführen.

**Enterprise-ready**: 

Verwenden Sie die API von Anthropic oder hosten Sie auf AWS oder GCP. Unternehmenstaugliche [Sicherheit](/de/docs/claude-code/security), [Datenschutz](/de/docs/claude-code/data-usage) und [Compliance](https://trust.anthropic.com/) sind eingebaut.

## Nächste Schritte

<CardGroup>
  <Card title="Schnellstart" icon="rocket" href="/de/docs/claude-code/quickstart">
    Sehen Sie Claude Code in Aktion mit praktischen Beispielen
  </Karte>

  <Card title="Allgemeine Arbeitsabläufe" icon="graduation-cap" href="/de/docs/claude-code/common-workflows">
    Schritt-für-Schritt-Anleitungen für gängige Arbeitsabläufe
  </Card>

  <Card title="Fehlerbehebung" icon="Schraubenschlüssel" href="/de/docs/claude-code/troubleshooting">
    Lösungen für häufige Probleme mit Claude Code
  </Card>

  <Card title="IDE-Einrichtung" icon="Laptop" href="/de/docs/claude-code/ide-integrations">
    Claude Code zu Ihrer IDE hinzufügen
  </Card>
</CardGroup>

## Zusätzliche Ressourcen


Host on AWS or GCP" icon="cloud" href="/de/docs/claude-code/third-party-integrations">
Konfigurieren Sie Claude Code mit Amazon Bedrock oder Google Vertex AI


Einstellungen" icon="gear" href="/de/docs/claude-code/settings
Passen Sie Claude Code für Ihren Arbeitsablauf an


Befehle" icon="terminal" href="/de/docs/claude-code/cli-reference
Erfahren Sie mehr über CLI-Befehle und -Steuerungen

Referenzimplementierung" icon="code" href="https://github.com/anthropics/claude-code/tree/main/.devcontainer">
Klonen Sie unsere Referenzimplementierung des Entwicklungscontainers


Sicherheit" icon="shield" href="/de/docs/claude-code/security
Entdecken Sie die Sicherheitsvorkehrungen von Claude Code und die besten Praktiken für eine sichere Nutzung

Datenschutz und Datennutzung" icon="lock" href="/de/docs/claude-code/data-usage
Verstehen Sie, wie Claude Code mit Ihren Daten umgeht



---

> [!NOTE]
> # Quickstart

> Willkommen bei Claude Code!

Mit dieser Schnellstart-Anleitung können Sie in nur wenigen Minuten eine KI-gestützte Programmierhilfe nutzen. Am Ende werden Sie verstehen, wie Sie Claude Code für gängige Entwicklungsaufgaben nutzen können.

## Bevor Sie beginnen

Stellen Sie sicher, dass Sie Folgendes haben:

* Ein Terminal oder eine Eingabeaufforderung geöffnet
* [Node.js 18 oder neuer installiert](https://nodejs.org/en/download/)
* Ein Code-Projekt, mit dem Sie arbeiten können

## Schritt 1: Claude Code installieren

Um Claude Code zu installieren, führen Sie den folgenden Befehl aus:

```sh
npm install -g @anthropic-ai/claude-code
```

## Schritt 2: Starten Sie Ihre erste Sitzung

Öffnen Sie Ihr Terminal in einem beliebigen Projektverzeichnis und starten Sie Claude Code:

```bash
cd /pfad/zu/ihrem/projekt
claude
```

Sie werden die Eingabeaufforderung Claude Code in einer neuen interaktiven Sitzung sehen:

```
✻ Willkommen bei Claude Code!

...

> Versuch "create a util logging.py that..."
```

## Schritt 3: Stellen Sie Ihre erste Frage

Beginnen wir damit, Ihre Codebasis zu verstehen. Versuchen Sie einen der folgenden Befehle:

```
> what does this project do?
```

Claude will analyze your files and provide a summary. You can also ask more specific questions:

```
> what technologies does this project use?
```

```
> where is the main entry point?
```

```
> explain the folder structure
```


Claude Code liest Ihre Dateien nach Bedarf - Sie müssen den Kontext nicht manuell hinzufügen.


## Schritt 4: Nehmen Sie Ihre erste Codeänderung vor

Lassen Sie Claude Code nun tatsächlich etwas kodieren. Versuchen Sie eine einfache Aufgabe:

```
> Füge eine Hallo-Welt-Funktion in die Hauptdatei ein
```

Claude Code wird:

1. Die entsprechende Datei finden
2. Zeigt Ihnen die vorgeschlagenen Änderungen
3. Sie um Ihre Zustimmung bitten
4. Die Bearbeitung vornehmen


  Claude Code bittet immer um Erlaubnis, bevor Dateien geändert werden. Sie können einzelne Änderungen genehmigen oder den Modus "Alle akzeptieren" für eine Sitzung aktivieren.


## Schritt 5: Git mit Claude Code verwenden

Claude Code macht Git-Operationen unterhaltsam:

```
> Welche Dateien habe ich geändert?
```

```
> meine Änderungen mit einer beschreibenden Nachricht übergeben
```

Sie können auch nach komplexeren Git-Operationen fragen:

```
> einen neuen Zweig namens feature/quickstart erstellen
```

```
> zeige mir die letzten 5 Übertragungen
```

```
> Hilf mir, Merge-Konflikte zu lösen
```

## Schritt 6: Einen Fehler beheben oder eine Funktion hinzufügen

Claude beherrscht die Fehlerbehebung und die Implementierung von Funktionen.

Beschreiben Sie in natürlicher Sprache, was Sie wollen:

```
> Eingabevalidierung zum Benutzerregistrierungsformular hinzufügen
```

Oder bestehende Probleme beheben:

```
> es gibt einen Fehler, bei dem Benutzer leere Formulare einreichen können - beheben Sie ihn
```

Claude Code wird:

* Den relevanten Code ausfindig machen
* Verstehen des Kontextes
* Eine Lösung implementieren
* Tests durchführen, falls vorhanden

## Schritt 7: Testen Sie andere gängige Arbeitsabläufe

Es gibt eine Reihe von Möglichkeiten, mit Claude zu arbeiten:

**Refactor-Code**

```
> Refaktorierung des Authentifizierungsmoduls, um async/await anstelle von Callbacks zu verwenden
```

**Tests schreiben**

```
> schreibe Unit-Tests für die Funktionen des Taschenrechners
```

**Dokumentation aktualisieren**

```
> Aktualisierung der README mit Installationsanweisungen
```

**Codeüberprüfung**

```
> meine Änderungen überprüfen und Verbesserungen vorschlagen
```


  **Erinnern Sie sich**: Claude Code ist Ihr AI-Paar-Programmierer. Sprechen Sie mit ihm wie mit einem hilfsbereiten Kollegen - beschreiben Sie, was Sie erreichen wollen, und er wird Ihnen helfen, es zu erreichen.


## Wichtige Befehle

Hier sind die wichtigsten Befehle für den täglichen Gebrauch:

| Command             | What it does                              | Example                             |
| ------------------- | ----------------------------------------- | ----------------------------------- |
| `claude`            | Interaktiven Modus starten                | `claude`                            |
| `claude "task"`     | Eine einmalige Aufgabe ausführen          | `claude "fix the build error"`      |
| `claude -p "query"` | Einmalige Abfrage ausführen, dann beenden | `claude -p "explain this function"` |
| `claude -c`         | Letzte Unterhaltung fortsetzen            | `claude -c`                         |
| `claude -r`         | Fortsetzen eines vorherigen Gesprächs     | `claude -r`                         |
| `claude commit`     | Eine Git-Übertragung erstellen            | `claude commit`                     |
| `/clear`            | Gesprächsverlauf löschen                  | `> /clear`                          |
| `/help`             | Verfügbare Befehle anzeigen               | `> /help`                           |
| `exit` or Ctrl+C    | Exit Claude Code                          | `> exit`                            |

Eine vollständige Liste der Befehle finden Sie in der [CLI-Referenz](/de/docs/claude-code/cli-reference).

## Profi-Tipps für Anfänger


  Seien Sie spezifisch mit Ihren Anfragen">
    Anstelle von: "Beheben Sie den Fehler"

    Versuchen Sie: "Beheben Sie den Anmeldefehler, bei dem die Benutzer nach der Eingabe falscher Anmeldedaten einen leeren Bildschirm sehen"
  </Akkordeon>

  Schritt-für-Schritt-Anweisungen verwenden">
    Unterteilen Sie komplexe Aufgaben in einzelne Schritte:

    ```
    > 1. Erstellen einer neuen Datenbanktabelle für Benutzerprofile
    ```

    ```
    > 2. Erstellen eines API-Endpunkts zum Abrufen und Aktualisieren von Benutzerprofilen
    ```

    ```
    > 3. eine Webseite erstellen, auf der die Benutzer ihre Informationen sehen und bearbeiten können
    ```


  Lass Claude zuerst erkunden">
    Bevor Sie Änderungen vornehmen, lassen Sie Claude Ihren Code verstehen:

    ```
    > Analysieren Sie das Datenbankschema
    ```

    ```
    > ein Dashboard erstellen, das die Produkte zeigt, die von unseren britischen Kunden am häufigsten zurückgegeben werden
    ```


  Sparen Sie Zeit mit Shortcuts">
    * Tabulator für die Befehlsvervollständigung verwenden
    * Drücken Sie ↑ für die Befehlshistorie
    * Tippen Sie `/`, um alle Schrägstrich-Befehle zu sehen


## Wie geht es weiter?

Nachdem Sie nun die Grundlagen kennengelernt haben, können Sie sich mit den fortgeschrittenen Funktionen beschäftigen:

Allgemeine Arbeitsabläufe
Schritt-für-Schritt-Anleitungen für allgemeine Aufgaben

CLI-Referenz
Alle Befehle und Optionen beherrschen

Konfiguration
Anpassen von Claude Code für Ihren Arbeitsablauf


## Hilfe erhalten

* **In Claude Code**: Tippen Sie `/help` oder fragen Sie "wie kann ich..."
* **Dokumentation**: Sie sind hier! Andere Anleitungen durchsuchen
* **Gemeinschaft**: Treten Sie unserem [Discord] (https://www.anthropic.com/discord) für Tipps und Unterstützung bei


---

> [!HINWEIS]
> # Gemeinsame Arbeitsabläufe

> Erfahren Sie mehr über gängige Arbeitsabläufe mit Claude Code.

Jede Aufgabe in diesem Dokument enthält klare Anweisungen, Beispielbefehle und bewährte Verfahren, damit Sie Claude Code optimal nutzen können.

## Neue Codebasen verstehen

## Einen schnellen Überblick über die Codebase erhalten

Nehmen wir an, Sie sind gerade einem neuen Projekt beigetreten und müssen dessen Struktur schnell verstehen.


Navigieren Sie in das Wurzelverzeichnis des Projekts">
```bash
cd /Pfad/zu/Projekt
```


Start Claude Code">
```bash
claude
```


Frag nach einer Übersicht auf höchster Ebene">
```
> Gib mir einen Überblick über diese Codebasis
```


Tiefer in bestimmte Komponenten eintauchen">
```
> Erläuterung der wichtigsten hier verwendeten Architekturmuster
```

```
> Was sind die wichtigsten Datenmodelle?
```

```
> wie wird die Authentifizierung gehandhabt?
```



  Tipps:

  * Beginnen Sie mit allgemeinen Fragen und grenzen Sie sie dann auf bestimmte Bereiche ein
  * Fragen Sie nach den im Projekt verwendeten Kodierungskonventionen und -mustern
  * Fordern Sie ein Glossar mit projektspezifischen Begriffen an


### Relevanten Code finden

Angenommen, Sie müssen Code zu einem bestimmten Merkmal oder einer bestimmten Funktion finden.


Bitten Sie Claude, relevante Dateien zu finden
```
> Finde die Dateien, die die Benutzerauthentifizierung behandeln
```


Kontext über das Zusammenspiel der Komponenten erhalten
```
> Wie arbeiten diese Authentifizierungsdateien zusammen?
```


Verstehen Sie den Ausführungsablauf
```
> Verfolgen Sie den Anmeldeprozess vom Frontend zur Datenbank
```



  Tipps:

  * Geben Sie genau an, wonach Sie suchen
  * Verwenden Sie die Fachsprache des Projekts


***

## Fehler effizient beheben

Angenommen, Sie sind auf eine Fehlermeldung gestoßen und müssen deren Ursache finden und beheben.


Teilen Sie den Fehler mit Claude">
```
> Ich erhalte eine Fehlermeldung, wenn ich npm test ausführe
```


Fragen Sie nach Empfehlungen zur Behebung">
```
> einige Möglichkeiten vorschlagen, um das @ts-ignore in user.ts zu beheben
```


Die Korrektur anwenden">
```
> user.ts aktualisieren, um die von Ihnen vorgeschlagene Nullprüfung hinzuzufügen
```




  Tipps:

  * Nennen Sie Claude den Befehl, um das Problem zu reproduzieren und einen Stack-Trace zu erhalten
  * Nennen Sie alle Schritte zur Reproduktion des Fehlers
  * Teilen Sie Claude mit, ob der Fehler intermittierend oder konsistent auftritt


***

## Code umgestalten

Angenommen, Sie müssen alten Code aktualisieren, um moderne Muster und Praktiken zu verwenden.


Identifizieren Sie alten Code für das Refactoring
```
> veraltete API-Verwendung in unserer Codebasis finden
```


Refactoring-Empfehlungen erhalten
```
> Vorschläge zum Refactoring von utils.js, um moderne JavaScript-Funktionen zu nutzen
```


Die Änderungen sicher anwenden
```
> Refactoring von utils.js, um ES2024-Funktionen zu nutzen, während das gleiche Verhalten beibehalten wird
```


Überprüfen Sie das Refactoring
```
> Ausführen von Tests für den umstrukturierten Code
```




  Tipps:

  * Bitten Sie Claude, die Vorteile des modernen Ansatzes zu erläutern
  * Verlangen Sie, dass Änderungen bei Bedarf die Abwärtskompatibilität wahren
  * Führen Sie das Refactoring in kleinen, testbaren Schritten durch


***

## Arbeit mit Tests

Angenommen, Sie müssen Tests für ungedeckten Code hinzufügen.

Identifizieren Sie ungetesteten Code
```
> Funktionen in NotificationsService.swift finden, die nicht durch Tests abgedeckt sind
```


Testgerüst generieren
```
> Tests für den Benachrichtigungsdienst hinzufügen
```


Sinnvolle Testfälle hinzufügen
```
> Hinzufügen von Testfällen für Randbedingungen im Benachrichtigungsdienst
```


Tests ausführen und verifizieren
```
> die neuen Tests ausführen und eventuelle Fehler beheben
```




  Tipps:

  * Bitten Sie um Tests, die Randfälle und Fehlerbedingungen abdecken
  * Fordern Sie, wenn nötig, sowohl Unit- als auch Integrationstests an
  * Lassen Sie sich von Claude die Teststrategie erklären


***

## Pull Requests erstellen

Angenommen, Sie müssen einen gut dokumentierten Pull-Request für Ihre Änderungen erstellen.


Fassen Sie Ihre Änderungen zusammen
```
> fasst die Änderungen zusammen, die ich am Authentifizierungsmodul vorgenommen habe
```


Erzeuge einen PR mit Claude
```
> einen PR erstellen
```


Überprüfen und verfeinern
```
> die PR-Beschreibung mit mehr Kontext über die Sicherheitsverbesserungen erweitern
```


Testdetails hinzufügen
```
> Informationen darüber hinzufügen, wie diese Änderungen getestet wurden
```




  Tipps:

  * Bitten Sie Claude direkt, eine PR für Sie zu erstellen
  * Prüfen Sie den von Claude erstellten PR, bevor Sie ihn einreichen
  * Bitten Sie Claude, auf mögliche Risiken oder Überlegungen hinzuweisen


## Dokumentation handhaben

Angenommen, Sie müssen Dokumentation für Ihren Code hinzufügen oder aktualisieren.


Identifizieren Sie undokumentierten Code
```
> Suche nach Funktionen ohne JSDoc-Kommentare im Modul auth
```


Dokumentation generieren
```
> JSDoc-Kommentare zu den undokumentierten Funktionen in auth.js hinzufügen
```


Überprüfen und verbessern
```
> Verbesserung der generierten Dokumentation mit mehr Kontext und Beispielen
```


Überprüfen der Dokumentation
```
> prüfen, ob die Dokumentation unseren Projektstandards entspricht
```




  Tipps:

  * Geben Sie den gewünschten Dokumentationsstil an (JSDoc, docstrings, usw.)
  * Fragen Sie nach Beispielen in der Dokumentation
  * Fordern Sie Dokumentation für öffentliche APIs, Schnittstellen und komplexe Logik


***

## Arbeiten mit Bildern

Angenommen, Sie müssen in Ihrem Code mit Bildern arbeiten und benötigen Claudes Hilfe bei der Analyse von Bildinhalten.


Fügen Sie der Unterhaltung ein Bild hinzu">
Sie können eine der folgenden Methoden verwenden:

1. Ziehen Sie ein Bild in das Fenster "Claude Code" und legen Sie es dort ab
2. Kopieren Sie ein Bild und fügen Sie es mit ctrl+v in die CLI ein (verwenden Sie nicht cmd+v)
3. Geben Sie einen Bildpfad für Claude an. Zum Beispiel: "Analysiere dieses Bild: /pfad/zu/ihr/bild.png"


Claude auffordern, das Bild zu analysieren
```
> Was zeigt dieses Bild?
```

```
> Beschreiben Sie die UI-Elemente in diesem Screenshot
```

```
> Gibt es problematische Elemente in diesem Diagramm?
```


Verwenden Sie Bilder für den Kontext
```
> Hier ist ein Screenshot des Fehlers. Was ist die Ursache?
```

```
> Dies ist unser aktuelles Datenbankschema. Wie sollten wir es für die neue Funktion ändern?
```


Code-Vorschläge aus visuellen Inhalten abrufen
```
> CSS generieren, das zu diesem Design-Mockup passt
```

```
> Welche HTML-Struktur würde diese Komponente nachbilden?
```




  Tipps:

  * Verwenden Sie Bilder, wenn Textbeschreibungen unklar oder umständlich wären
  * Fügen Sie Screenshots von Fehlern, UI-Designs oder Diagrammen für einen besseren Kontext ein
  * Sie können mit mehreren Bildern in einer Konversation arbeiten
  * Die Bildanalyse funktioniert mit Diagrammen, Screenshots, Mockups und mehr


***

## Referenzdateien und Verzeichnisse

Verwenden Sie @, um Dateien oder Verzeichnisse schnell einzubinden, ohne darauf zu warten, dass Claude sie liest.

Eine einzelne Datei referenzieren
```
> Erkläre die Logik in @src/utils/auth.js
```

Dies beinhaltet den vollständigen Inhalt der Datei in der Konversation.


Verweis auf ein Verzeichnis
```
> Wie ist die Struktur von @src/components?
```

Dies liefert eine Verzeichnisliste mit Dateiinformationen.


Referenz MCP-Ressourcen
```
> Zeige mir die Daten von @github:repos/owner/repo/issues
```

Diese Funktion holt Daten von verbundenen MCP-Servern im Format @server:resource. Siehe [MCP-Ressourcen](/de/docs/claude-code/mcp#use-mcp-resources) für Details.


  Tipps:

  * Dateipfade können relativ oder absolut sein
  * @ Dateiverweise fügen CLAUDE.md im Verzeichnis der Datei und den übergeordneten Verzeichnissen zum Kontext hinzu
  * Verzeichnisverweise zeigen Dateilisten an, nicht den Inhalt
  * Sie können mehrere Dateien in einer einzigen Nachricht referenzieren (z. B. "@file1.js und @file2.js")


***

## Erweitertes Denken nutzen

Nehmen wir an, Sie arbeiten an komplexen architektonischen Entscheidungen, herausfordernden Fehlern oder planen mehrstufige Implementierungen, die tiefgreifende Überlegungen erfordern.


  Geben Sie den Kontext vor und bitten Sie Claude zu denken
    ```
    > Ich muss ein neues Authentifizierungssystem mit OAuth2 für unsere API implementieren. Denken Sie gründlich über den besten Ansatz für die Implementierung in unserer Codebasis nach.
    ```

    Claude wird relevante Informationen aus Ihrer Codebase sammeln und
    erweitertes Denken verwenden, das in der Schnittstelle sichtbar sein wird.
  

  Verfeinern Sie die Überlegungen mit Folgeaufforderungen
    ```
    > Denken Sie über mögliche Sicherheitslücken bei diesem Ansatz nach
    ```

    ```
    > Überlegen Sie genauer, welche Randfälle wir behandeln sollten
    ```
  



  Tipps, um den größten Nutzen aus dem erweiterten Denken zu ziehen:

  Erweitertes Denken ist am wertvollsten für komplexe Aufgaben wie z. B.:

  * Planung komplexer Architekturänderungen
  * Fehlersuche bei komplizierten Problemen
  * Erstellung von Implementierungsplänen für neue Funktionen
  * Verstehen komplexer Codebasen
  * Abwägen von Kompromissen zwischen verschiedenen Ansätzen

  Die Art und Weise, wie Sie zum Nachdenken auffordern, führt zu einer unterschiedlichen Tiefe des Denkens:

  * "denken" löst einfaches, erweitertes Denken aus
  * intensivere Formulierungen wie "mehr denken", "viel denken", "härter denken" oder "länger denken" lösen tieferes Denken aus

  Weitere Tipps für erweiterte Denkanstöße finden Sie unter [Tipps für erweitertes Denken](/de/docs/build-with-claude/prompt-engineering/extended-thinking-tips).


  Claude zeigt seinen Denkprozess als kursiven grauen Text über der
  antwort.


***

## Vorherige Gespräche fortsetzen

Angenommen, Sie haben mit Claude Code an einer Aufgabe gearbeitet und müssen in einer späteren Sitzung dort weitermachen, wo Sie aufgehört haben.

Claude Code bietet zwei Möglichkeiten, frühere Unterhaltungen fortzusetzen:

* `--Fortsetzen`, um automatisch die letzte Unterhaltung fortzusetzen
* `--resume`, um eine Gesprächsauswahl anzuzeigen


Die letzte Konversation fortsetzen">
``bash
claude --continue
```

Damit wird die letzte Unterhaltung sofort und ohne Aufforderung fortgesetzt.


Weiter im nicht-interaktiven Modus">
```bash
claude --continue --print "Weiter mit meiner Aufgabe"
```

Verwenden Sie `--print` mit `--continue`, um die letzte Konversation im nicht-interaktiven Modus fortzusetzen, ideal für Skripte oder Automatisierung.


Gesprächspicker anzeigen">
``bash
claude --resume


Dies zeigt eine interaktive Gesprächsauswahl an:

* Uhrzeit des Gesprächsbeginns
* Erste Eingabeaufforderung oder Gesprächszusammenfassung
* Anzahl der Nachrichten

Verwenden Sie die Pfeiltasten zum Navigieren und drücken Sie die Eingabetaste, um eine Konversation auszuwählen.




  Tipps:

  * Der Gesprächsverlauf wird lokal auf Ihrem Rechner gespeichert
  * Verwenden Sie "Fortsetzen", um schnell auf Ihre letzte Unterhaltung zuzugreifen
  * Verwenden Sie `--resume`, wenn Sie ein bestimmtes vergangenes Gespräch auswählen möchten
  * Bei der Wiederaufnahme sehen Sie den gesamten Gesprächsverlauf, bevor Sie fortfahren
  * Die wiederaufgenommene Konversation beginnt mit demselben Modell und derselben Konfiguration wie die ursprüngliche

  So funktioniert es:

  1. **Konversationsspeicherung**: Alle Unterhaltungen werden automatisch lokal mit ihrem gesamten Nachrichtenverlauf gespeichert
  2. **Nachrichten-Deserialisierung**: Bei der Wiederaufnahme wird der gesamte Nachrichtenverlauf wiederhergestellt, um den Kontext zu erhalten
  3. **Werkzeug-Status**: Die Verwendung der Werkzeuge und die Ergebnisse der vorherigen Konversation bleiben erhalten
  4. **Kontext-Wiederherstellung**: Die Konversation wird unter Beibehaltung des vorherigen Kontexts fortgesetzt

  Beispiele:

  ```bash
  # Continue most recent conversation
  claude --continue

  # Continue most recent conversation with a specific prompt
  claude --continue --print "Show me our progress"

  # Show conversation picker
  claude --resume

  # Continue most recent conversation in non-interactive mode
  claude --continue --print "Run the tests again"
  ```


***

## Parallele Claude Code-Sitzungen mit Git-Arbeitsblöcken durchführen

Angenommen, Sie müssen an mehreren Aufgaben gleichzeitig arbeiten und dabei den Code zwischen den Claude Code-Instanzen vollständig isolieren.


Git-Worktrees verstehen">
Mit Git-Workrees können Sie mehrere Zweige aus demselben
repository in separate Verzeichnisse auszuchecken. Jeder Worktree hat sein eigenes Arbeitsverzeichnis
arbeitsverzeichnis mit isolierten Dateien, aber mit demselben Git-Verlauf. Erfahren Sie
mehr in der [offiziellen Git-Worktree
dokumentation](https://git-scm.com/docs/git-worktree).


Einen neuen Arbeitsbaum erstellen
```bash
# Create a new worktree with a new branch 
git worktree add ../project-feature-a -b feature-a

# Or create a worktree with an existing branch
git worktree add ../project-bugfix bugfix-123
```

Dadurch wird ein neues Verzeichnis mit einer separaten Arbeitskopie Ihres Repositorys erstellt.


Führen Sie Claude Code in jedem Arbeitsbaum aus
```bash
# Navigate to your worktree 
cd ../project-feature-a

# Run Claude Code in this isolated environment
claude
```


Claude in einem anderen Arbeitsbaum ausführen
```bash
cd ../project-bugfix
claude
```


Verwalten Sie Ihre Arbeitsbäume
```bash
# List all worktrees
git worktree list

# Remove a worktree when done
git worktree remove ../project-feature-a
```




  Tipps:

  * Jeder Arbeitsbaum hat seinen eigenen unabhängigen Dateistatus, was ihn perfekt für parallele Claude Code-Sitzungen macht
  
  * Änderungen, die in einem Arbeitsbaum vorgenommen werden, wirken sich nicht auf andere Arbeitsbäume aus, wodurch verhindert wird, dass sich Claude-Instanzen gegenseitig beeinträchtigen

  * Alle Arbeitsbäume nutzen denselben Git-Verlauf und dieselben Remote-Verbindungen

  * Bei langwierigen Aufgaben können Sie Claude in einem Arbeitsbaum arbeiten lassen, während Sie in einem anderen weiter entwickeln

  * Verwenden Sie aussagekräftige Verzeichnisnamen, um leicht zu erkennen, für welche Aufgabe die einzelnen Arbeitsbäume bestimmt sind

  * Denken Sie daran, Ihre Entwicklungsumgebung in jedem neuen Worktree entsprechend der Einrichtung Ihres Projekts zu initialisieren. Abhängig von Ihrem Stack kann dies Folgendes beinhalten:
    * JavaScript-Projekte: Installation von Abhängigkeiten (`npm install`, `yarn`)
    * Python-Projekte: Einrichten von virtuellen Umgebungen oder Installieren mit Paketmanagern
    * Andere Sprachen: Befolgen Sie den Standard-Installationsprozess für Ihr Projekt


***

## Claude als Unix-ähnliches Dienstprogramm verwenden

## Fügen Sie Claude zu Ihrem Verifizierungsprozess hinzu

Angenommen, Sie möchten Claude Code als Linter oder Code-Reviewer verwenden.

**Fügen Sie Claude zu Ihrem Build-Skript hinzu:**

```json
// paket.json
{
    ...
    "scripts": {
        ...
        "lint:claude": "claude -p 'du bist ein linter. bitte schau dir die änderungen gegenüber main an und melde alle probleme, die mit typos zusammenhängen. melde den dateinamen und die zeilennummer in einer zeile und eine beschreibung des problems in der zweiten zeile. gib keinen anderen text zurück.'"
    }
}
```


  Tipps:

  * Verwenden Sie Claude für die automatische Codeüberprüfung in Ihrer CI/CD-Pipeline
  * Passen Sie die Eingabeaufforderung an, um nach bestimmten, für Ihr Projekt relevanten Problemen zu suchen
  * Erwägen Sie die Erstellung mehrerer Skripte für verschiedene Arten der Überprüfung


### Pipe in, pipe out

Angenommen, Sie möchten Daten über die Pipeline in Claude einspeisen und Daten in einem strukturierten Format zurückerhalten.

**Daten durch Claude leiten:*

```bash
cat build-error.txt | claude -p 'concisely explain the root cause of this build error' > output.txt
```


  Tipps:

  * Verwenden Sie Pipes, um Claude in bestehende Shell-Skripte zu integrieren
  * Kombinieren Sie Claude mit anderen Unix-Tools für leistungsfähige Arbeitsabläufe
  * Erwägen Sie die Verwendung von --output-format für strukturierte Ausgaben


### Ausgabeformat kontrollieren

Angenommen, Sie benötigen die Ausgabe von Claude in einem bestimmten Format, insbesondere bei der Integration von Claude Code in Skripte oder andere Tools.


Textformat verwenden (Standard)">
```bash
cat data.txt | claude -p 'diese Daten zusammenfassen' --output-format text > summary.txt
```

Dies gibt nur die reine Textantwort von Claude aus (Standardverhalten).


Verwende JSON-Format">
```bash
cat code.py | claude -p 'analysiere diesen Code nach Fehlern' --output-format json > analysis.json
```

Dies gibt ein JSON-Array von Meldungen mit Metadaten wie Kosten und Dauer aus.


Verwenden Sie das Streaming JSON Format">
```bash
cat log.txt | claude -p 'parse this log file for errors' --output-format stream-json
```

Dies gibt eine Reihe von JSON-Objekten in Echtzeit aus, während Claude die Anfrage verarbeitet. Jede Nachricht ist ein gültiges JSON-Objekt, aber die gesamte Ausgabe ist kein gültiges JSON, wenn sie verkettet wird.




  Tipps:

  * Verwenden Sie `--output-format text` für einfache Integrationen, bei denen Sie nur die Antwort von Claude benötigen
  * Verwenden Sie `--output-format json`, wenn Sie das komplette Gesprächsprotokoll benötigen
  * Verwenden Sie `--output-format stream-json` für die Echtzeit-Ausgabe jeder Gesprächsrunde


***

## Benutzerdefinierte Slash-Befehle erstellen

Claude Code unterstützt benutzerdefinierte Slash-Befehle, die Sie erstellen können, um bestimmte Abfragen oder Aufgaben schnell auszuführen.

Weitere Details finden Sie auf der Referenzseite [Slash commands](/de/docs/claude-code/slash-commands).

### Projektspezifische Befehle erstellen

Angenommen, Sie möchten wiederverwendbare Slash-Befehle für Ihr Projekt erstellen, die alle Teammitglieder nutzen können.


Erstellen Sie ein Verzeichnis commands in Ihrem Projekt">
```bash
mkdir -p .claude/commands
```


Erzeuge eine Markdown-Datei für jeden Befehl">
```bash
echo "Analysieren Sie die Leistung dieses Codes und schlagen Sie drei spezifische Optimierungen vor:" > .claude/commands/optimize.md
```


Verwenden Sie Ihren eigenen Befehl in Claude Code">
```
> /optimieren
```




  Tipps:

  * Befehlsnamen werden vom Dateinamen abgeleitet (z. B. wird `optimize.md` zu `/optimize`)
  * Sie können Befehle in Unterverzeichnissen organisieren (z.B. `.claude/commands/frontend/component.md` erzeugt `/component` mit "(project:frontend)" in der Beschreibung)
  * Die Projektbefehle sind für jeden verfügbar, der das Repository klont
  * Der Inhalt der Markdown-Datei wird zur Eingabeaufforderung, die an Claude gesendet wird, wenn der Befehl aufgerufen wird


### Befehlsargumente mit \$ARGUMENTS hinzufügen

Angenommen, Sie möchten flexible Schrägstrich-Befehle erstellen, die zusätzliche Eingaben von Benutzern akzeptieren können.


Erstellen Sie eine Befehlsdatei mit dem Platzhalter $ARGUMENTS">
```bash
echo "Finden und beheben Sie das Problem #$ARGUMENTS. Folgen Sie diesen Schritten: 1.
Verstehen Sie das im Ticket beschriebene Problem 2. Finde den relevanten Code in
unserer Codebasis 3. Implementieren Sie eine Lösung, die die Ursache behebt 4. Hinzufügen von
geeignete Tests 5. Bereiten Sie eine kurze PR-Beschreibung vor" >
.claude/commands/fix-issue.md
```


Verwenden Sie den Befehl mit einer Ausgabenummer">
In Ihrer Claude-Sitzung verwenden Sie den Befehl mit Argumenten.

```
> /fix-issue 123
```

Dadurch wird \$ARGUMENTS in der Eingabeaufforderung durch "123" ersetzt.




  Tipps:

  * Der Platzhalter \$ARGUMENTS wird durch jeden Text ersetzt, der auf den Befehl folgt
  * Sie können \$ARGUMENTS überall in Ihrer Befehlsvorlage platzieren
  * Andere nützliche Anwendungen: Generieren von Testfällen für bestimmte Funktionen, Erstellen von Dokumentation für Komponenten, Überprüfen von Code in bestimmten Dateien oder Übersetzen von Inhalten in bestimmte Sprachen


### Persönliche Slash-Befehle erstellen

Angenommen, Sie möchten persönliche Slash-Befehle erstellen, die in allen Ihren Projekten funktionieren.


Erstellen Sie ein Verzeichnis commands in Ihrem Home-Ordner">
```bash
mkdir -p ~/.claude/commands
```


Erstelle eine Markdown-Datei für jeden Befehl">
```bash
echo "Überprüfen Sie diesen Code auf Sicherheitsschwachstellen, insbesondere auf:" >
~/.claude/commands/security-review.md
```


Verwenden Sie Ihr persönliches Kommando">
```
> /security-review
```




  Tipps:

  * Persönliche Befehle zeigen "(user)" in ihrer Beschreibung an, wenn sie mit `/help` aufgelistet werden
  * Persönliche Befehle sind nur für Sie selbst verfügbar und werden nicht an Ihr Team weitergegeben
  * Persönliche Befehle funktionieren in allen Ihren Projekten
  * Sie können diese für konsistente Arbeitsabläufe in verschiedenen Codebasen verwenden


***

## Nächste Schritte

<Card title="Claude Code Referenzimplementierung" icon="code" href="https://github.com/anthropics/claude-code/tree/main/.devcontainer">
  Klonen Sie unsere Referenzimplementierung des Entwicklungscontainers.
</Karte>

---

> [!HINWEIS]
> # Claude Code SDK

> Erfahren Sie mehr über die programmatische Integration von Claude Code in Ihre Anwendungen mit dem Claude Code SDK.

Das Claude Code SDK ermöglicht die Ausführung von Claude Code als Unterprozess und bietet eine Möglichkeit, KI-gestützte Programmierassistenten und Tools zu erstellen, die die Fähigkeiten von Claude nutzen.

Das SDK ist für Kommandozeilen-, TypeScript- und Python-Nutzung verfügbar.

## Authentifizierung

Das Claude Code SDK unterstützt mehrere Authentifizierungsmethoden:

### Anthropischer API-Schlüssel

Um das Claude Code SDK direkt mit der Anthropic-API zu verwenden, empfehlen wir, einen eigenen API-Schlüssel zu erstellen:

1. Erstellen Sie einen Anthropic-API-Schlüssel in der [Anthropic-Konsole] (https://console.anthropic.com/)
2. Setzen Sie dann die Umgebungsvariable `ANTHROPIC_API_KEY`. Wir empfehlen, diesen Schlüssel sicher zu speichern (z.B. mit einem Github [secret](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions))

### API-Anmeldeinformationen von Drittanbietern

Das SDK unterstützt auch API-Anbieter von Drittanbietern:

* **Amazon Bedrock**: Setzen Sie die Umgebungsvariable "CLAUDE_CODE_USE_BEDROCK=1" und konfigurieren Sie AWS-Anmeldeinformationen
* **Google Vertex AI**: Setzen Sie die Umgebungsvariable "CLAUDE_CODE_USE_VERTEX=1" und konfigurieren Sie die Google Cloud-Anmeldeinformationen

Detaillierte Konfigurationsanweisungen für Drittanbieter finden Sie in den Dokumentationen [Amazon Bedrock](/de/docs/claude-code/amazon-bedrock) und [Google Vertex AI](/de/docs/claude-code/google-vertex-ai).

## Grundlegende SDK-Nutzung

Das Claude Code SDK ermöglicht es Ihnen, Claude Code im nicht-interaktiven Modus in Ihren Anwendungen zu verwenden.

### Kommandozeile

Hier sind ein paar grundlegende Beispiele für das Kommandozeilen-SDK:

```bash
# Run a single prompt and exit (print mode)
$ claude -p "Write a function to calculate Fibonacci numbers"

# Using a pipe to provide stdin
$ echo "Explain this code" | claude -p

# Output in JSON format with metadata
$ claude -p "Generate a hello world function" --output-format json

# Stream JSON output as it arrives
$ claude -p "Build a React component" --output-format stream-json
```

### TypeScript

Das TypeScript-SDK ist im Hauptpaket [`@anthropic-ai/claude-code`] (https://www.npmjs.com/package/@anthropic-ai/claude-code) auf NPM enthalten:

```ts
import { query, type SDKMessage } from "@anthropic-ai/claude-code";

const messages: SDKMessage[] = [];

for await (const message of query({
  prompt: "Write a haiku about foo.py",
  abortController: new AbortController(),
  options: {
    maxTurns: 3,
  },
})) {
  messages.push(message);
}

console.log(messages);
```

Das TypeScript SDK akzeptiert alle Argumente, die vom Kommandozeilen-SDK unterstützt werden, sowie:

| Argument                     | Description                         | Default                                                       |
| :--------------------------- | :---------------------------------- | :------------------------------------------------------------ |
| `abortController`            | Abort controller                    | `new AbortController()`                                       |
| `cwd`                        | Current working directory           | `process.cwd()`                                               |
| `executable`                 | Which JavaScript runtime to use     | `node` when running with Node.js, `bun` when running with Bun |
| `executableArgs`             | Arguments to pass to the executable | `[]`                                                          |
| `pathToClaudeCodeExecutable` | Path to the Claude Code executable  | Executable that ships with `@anthropic-ai/claude-code`        |

### Python

The Python SDK is available as [`claude-code-sdk`](https://github.com/anthropics/claude-code-sdk-python) on PyPI:

```bash
pip install claude-code-sdk
```

**Prerequisites:**

* Python 3.10+
* Node.js
* Claude Code CLI: `npm install -g @anthropic-ai/claude-code`

Basic usage:

```python
import anyio
from claude_code_sdk import query, ClaudeCodeOptions, Message

async def main():
    messages: list[Message] = []
    
    async for message in query(
        prompt="Write a haiku about foo.py",
        options=ClaudeCodeOptions(max_turns=3)
    ):
        messages.append(message)
    
    print(messages)

anyio.run(main)
```

The Python SDK accepts all arguments supported by the command line SDK through the `ClaudeCodeOptions` class:

```python
from claude_code_sdk import query, ClaudeCodeOptions
from pathlib import Path

options = ClaudeCodeOptions(
    max_turns=3,
    system_prompt="You are a helpful assistant",
    cwd=Path("/path/to/project"),  # Can be string or Path
    allowed_tools=["Read", "Write", "Bash"],
    permission_mode="acceptEdits"
)

async for message in query(prompt="Hello", options=options):
    print(message)
```

## Erweiterte Nutzung

Die folgende Dokumentation verwendet das Kommandozeilen-SDK als Beispiel, kann aber auch mit den TypeScript- und Python-SDKs verwendet werden.

### Multi-Turn-Konversationen

Bei Multi-Turn-Konversationen können Sie die Konversation fortsetzen oder mit der letzten Sitzung fortfahren:

```bash
# Continue the most recent conversation
$ claude --continue

# Continue and provide a new prompt
$ claude --continue "Now refactor this for better performance"

# Resume a specific conversation by session ID
$ claude --resume 550e8400-e29b-41d4-a716-446655440000

# Resume in print mode (non-interactive)
$ claude -p --resume 550e8400-e29b-41d4-a716-446655440000 "Update the tests"

# Continue in print mode (non-interactive)
$ claude -p --continue "Add error handling"
```

### Benutzerdefinierte Systemaufforderungen

Sie können benutzerdefinierte System-Eingabeaufforderungen bereitstellen, um das Verhalten von Claude zu steuern:

```bash
# Override system prompt (only works with --print)
$ claude -p "Build a REST API" --system-prompt "You are a senior backend engineer. Focus on security, performance, and maintainability."

# System prompt with specific requirements
$ claude -p "Create a database schema" --system-prompt "You are a database architect. Use PostgreSQL best practices and include proper indexing."
```

Sie können auch Anweisungen an die Standard-Systemeingabeaufforderung anhängen:

```bash
# Append system prompt (only works with --print)
$ claude -p "Build a REST API" --append-system-prompt "After writing code, be sure to code review yourself."
```

### MCP-Konfiguration

Das Model Context Protocol (MCP) ermöglicht es Ihnen, Claude Code mit zusätzlichen Tools und Ressourcen von externen Servern zu erweitern. Mit dem Flag `--mcp-config` können Sie MCP-Server laden, die spezielle Funktionen wie Datenbankzugriff, API-Integrationen oder benutzerdefinierte Werkzeuge bereitstellen.

Erstellen Sie eine JSON-Konfigurationsdatei mit Ihren MCP-Servern:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/path/to/allowed/files"
      ]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "your-github-token"
      }
    }
  }
}
```

Dann verwenden Sie es mit Claude Code:

```bash
# Load MCP servers from configuration
$ claude -p "List all files in the project" --mcp-config mcp-servers.json

# Important: MCP tools must be explicitly allowed using --allowedTools
# MCP tools follow the format: mcp__$serverName__$toolName
$ claude -p "Search for TODO comments" \
  --mcp-config mcp-servers.json \
  --allowedTools "mcp__filesystem__read_file,mcp__filesystem__list_directory"

# Use an MCP tool for handling permission prompts in non-interactive mode
$ claude -p "Deploy the application" \
  --mcp-config mcp-servers.json \
  --allowedTools "mcp__permissions__approve" \
  --permission-prompt-tool mcp__permissions__approve
```


>   Wenn Sie MCP-Tools verwenden, müssen Sie diese explizit mit dem Flag `--allowedTools` zulassen. MCP-Werkzeugnamen folgen dem Muster `mcp__<serverName>__<toolName>`, wobei:
>
* "Servername" ist der Schlüssel aus Ihrer MCP-Konfigurationsdatei
> * `toolName` ist das spezifische Werkzeug, das von diesem Server bereitgestellt wird
>
> Diese Sicherheitsmaßnahme stellt sicher, dass MCP-Tools nur verwendet werden, wenn dies ausdrücklich erlaubt ist.
>
> Wenn Sie nur den Servernamen angeben (z.B. `mcp__<Servername>`), werden alle Tools dieses Servers zugelassen.
>
> Glob-Muster (z.B. `mcp__go*`) werden nicht unterstützt.


### Benutzerdefiniertes Werkzeug für die Eingabeaufforderung

Verwenden Sie optional `--permission-prompt-tool`, um ein MCP-Tool zu übergeben, mit dem wir prüfen, ob der Benutzer dem Modell die Berechtigung zum Aufrufen eines bestimmten Tools erteilt oder nicht. Wenn das Modell ein Werkzeug aufruft, geschieht Folgendes:

1. Zunächst werden die Berechtigungseinstellungen überprüft: alle [settings.json-Dateien] (/de/docs/claude-code/settings) sowie die im SDK übergebenen `--allowedTools` und `--disallowedTools`

```ts
// tool call is allowed
{
  "behavior": "allow",
  "updatedInput": {...}, // updated input, or just return back the original input
}

// tool call is denied
{
  "behavior": "deny",
  "message": "..." // human-readable string explaining why the permission was denied
}
```

Die Implementierung eines TypeScript MCP-Berechtigungsabfragetools könnte beispielsweise so aussehen:

```ts
const server = new McpServer({
  name: "Test permission prompt MCP Server",
  version: "0.0.1",
});

server.tool(
  "approval_prompt",
  'Simulate a permission check - approve if the input contains "allow", otherwise deny',
  {
    tool_name: z.string().describe("The name of the tool requesting permission"),
    input: z.object({}).passthrough().describe("The input for the tool"),
    tool_use_id: z.string().optional().describe("The unique tool use request ID"),
  },
  async ({ tool_name, input }) => {
    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(
            JSON.stringify(input).includes("allow")
              ? {
                  behavior: "allow",
                  updatedInput: input,
                }
              : {
                  behavior: "deny",
                  message: "Permission denied by test approval_prompt tool",
                }
          ),
        },
      ],
    };
  }
);
```

Um dieses Tool zu verwenden, fügen Sie Ihren MCP-Server hinzu (z. B. mit `--mcp-config`) und rufen dann das SDK wie folgt auf:

```sh
claude -p "..." \
  --permission-prompt-tool mcp__test-server__approval_prompt \
  --mcp-config my-config.json
```

Anmerkungen zur Verwendung:

* Verwenden Sie `updatedInput`, um dem Modell mitzuteilen, dass die Erlaubnisaufforderung seine Eingabe verändert hat die ursprüngliche Eingabe, wie im obigen Beispiel. Wenn das Tool dem Benutzer beispielsweise eine Datei-Editierdifferenz zeigt und ihn Folgendes bearbeiten lässtwenn Sie den Unterschied manuell ändern, sollte das Werkzeug zur Eingabeaufforderung für Berechtigungen die aktualisierte Bearbeitung zurückgeben.
* Die Nutzlast muss JSON-stringifiziert sein

## Available CLI options 

Das SDK nutzt alle in Claude Code verfügbaren CLI-Optionen. Hier sind die wichtigsten für die Verwendung des SDK:

| Flag                       | Description                                                                                                                             | Example                                                                                                                   |
| :------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------ |
| `--print`, `-p`            | Lauf im nicht-interaktiven Modus                                                                                                        | `claude -p "query"`                                                                                                       |
| `--output-format`          | Angabe des Ausgabeformats (`text`, `json`, `stream-json`)                                                                               | `claude -p --output-format json`                                                                                          |
| `--resume`, `-r`           | Wiederaufnahme eines Gesprächs nach Sitzungs-ID                                                                                         | `claude --resume abc123`                                                                                                  |
| `--continue`, `-c`         | Fortsetzung der letzten Unterhaltung                                                                                                    | `claude --continue`                                                                                                       |
| `--verbose`                | Ausführliche Protokollierung einschalten                                                                                                | `claude --verbose`                                                                                                        |
| `--max-turns`              | Begrenzung der Agentenumdrehungen im nicht-interaktiven Modus                                                                           | `claude --max-turns 3`                                                                                                    |
| `--system-prompt`          | Systemaufforderung außer Kraft setzen (nur mit `--print`)                                                                               | `claude --system-prompt "Custom instruction"`                                                                             |
| `--append-system-prompt`   | Anhängen an die System-Eingabeaufforderung (nur mit `--print`)                                                                          | `claude --append-system-prompt "Custom instruction"`                                                                      |
| `--allowedTools`           | Durch Leerzeichen getrennte Liste zulässiger Werkzeuge oder <br /><br /> String einer durch Komma getrennten Liste zulässiger Werkzeuge | `claude --allowedTools mcp__slack mcp__filesystem`<br /><br />`claude --allowedTools "Bash(npm install),mcp__filesystem"` |
| `--disallowedTools`        | Durch Leerzeichen getrennte Liste der verweigerten Werkzeuge oder <br /><br /> durch Komma getrennte Liste der verweigerten Werkzeuge   | `claude --disallowedTools mcp__splunk mcp__github`<br /><br />`claude --disallowedTools "Bash(git commit),mcp__github"`   |
| `--mcp-config`             | MCP-Server aus einer JSON-Datei laden                                                                                                   | `claude --mcp-config servers.json`                                                                                        |
| `--permission-prompt-tool` | MCP-Werkzeug zur Behandlung von Erlaubnisaufforderungen (nur mit `--print`)                                                             | `claude --permission-prompt-tool mcp__auth__prompt`                                                                       |

For a complete list of CLI options and features, see the [CLI reference](/en/docs/claude-code/cli-reference) documentation.

## Output formats

The SDK supports multiple output formats:

### Text output (default)

Returns just the response text:

```bash
$ claude -p "Explain file src/components/Header.tsx"
# Output: This is a React component showing...
```

### JSON output

Returns structured data including metadata:

```bash
$ claude -p "How does the data layer work?" --output-format json
```

Response format:

```json
{
  "type": "result",
  "subtype": "success",
  "total_cost_usd": 0.003,
  "is_error": false,
  "duration_ms": 1234,
  "duration_api_ms": 800,
  "num_turns": 6,
  "result": "The response text here...",
  "session_id": "abc123"
}
```

### Streaming JSON output

Streams each message as it is received:

```bash
$ claude -p "Build an application" --output-format stream-json
```

Each conversation begins with an initial `init` system message, followed by a list of user and assistant messages, followed by a final `result` system message with stats. Each message is emitted as a separate JSON object.

## Message schema

Messages returned from the JSON API are strictly typed according to the following schema:

```ts
type SDKMessage =
  // An assistant message
  | {
      type: "assistant";
      message: Message; // from Anthropic SDK
      session_id: string;
    }

  // A user message
  | {
      type: "user";
      message: MessageParam; // from Anthropic SDK
      session_id: string;
    }

  // Emitted as the last message
  | {
      type: "result";
      subtype: "success";
      duration_ms: float;
      duration_api_ms: float;
      is_error: boolean;
      num_turns: int;
      result: string;
      session_id: string;
      total_cost_usd: float;
    }

  // Emitted as the last message, when we've reached the maximum number of turns
  | {
      type: "result";
      subtype: "error_max_turns" | "error_during_execution";
      duration_ms: float;
      duration_api_ms: float;
      is_error: boolean;
      num_turns: int;
      session_id: string;
      total_cost_usd: float;
    }

  // Emitted as the first message at the start of a conversation
  | {
      type: "system";
      subtype: "init";
      apiKeySource: string;
      cwd: string;
      session_id: string;
      tools: string[];
      mcp_servers: {
        name: string;
        status: string;
      }[];
      model: string;
      permissionMode: "default" | "acceptEdits" | "bypassPermissions" | "plan";
    };
```

We will soon publish these types in a JSONSchema-compatible format. We use semantic versioning for the main Claude Code package to communicate breaking changes to this format.

`Message` and `MessageParam` types are available in Anthropic SDKs. For example, see the Anthropic [TypeScript](https://github.com/anthropics/anthropic-sdk-typescript) and [Python](https://github.com/anthropics/anthropic-sdk-python/) SDKs.

## Input formats

The SDK supports multiple input formats:

### Text input (default)

Input text can be provided as an argument:

```bash
$ claude -p "Explain this code"
```

Or input text can be piped via stdin:

```bash
$ echo "Explain this code" | claude -p
```

### Streaming JSON input

A stream of messages provided via `stdin` where each message represents a user turn. This allows multiple turns of a conversation without re-launching the `claude` binary and allows providing guidance to the model while it is processing a request.

Each message is a JSON 'User message' object, following the same format as the output message schema. Messages are formatted using the [jsonl](https://jsonlines.org/) format where each line of input is a complete JSON object. Streaming JSON input requires `-p` and `--output-format stream-json`.

Currently this is limited to text-only user messages.

```bash
$ echo '{"type":"user","message":{"role":"user","content":[{"type":"text","text":"Explain this code"}]}}' | claude -p --output-format=stream-json --input-format=stream-json --verbose
```

## Examples

### Simple script integration

```bash
#!/bin/bash

# Simple function to run Claude and check exit code
run_claude() {
    local prompt="$1"
    local output_format="${2:-text}"

    if claude -p "$prompt" --output-format "$output_format"; then
        echo "Success!"
    else
        echo "Error: Claude failed with exit code $?" >&2
        return 1
    fi
}

# Usage examples
run_claude "Write a Python function to read CSV files"
run_claude "Optimize this database query" "json"
```

### Processing files with Claude

```bash
# Process a file through Claude
$ cat mycode.py | claude -p "Review this code for bugs"

# Process multiple files
$ for file in *.js; do
    echo "Processing $file..."
    claude -p "Add JSDoc comments to this file:" < "$file" > "${file}.documented"
done

# Use Claude in a pipeline
$ grep -l "TODO" *.py | while read file; do
    claude -p "Fix all TODO items in this file" < "$file"
done
```

### Session management

```bash
# Start a session and capture the session ID
$ claude -p "Initialize a new project" --output-format json | jq -r '.session_id' > session.txt

# Continue with the same session
$ claude -p --resume "$(cat session.txt)" "Add unit tests"
```

## Best practices

1. **Use JSON output format** for programmatic parsing of responses:

   ```bash
   # Parse JSON response with jq
   result=$(claude -p "Generate code" --output-format json)
   code=$(echo "$result" | jq -r '.result')
   cost=$(echo "$result" | jq -r '.cost_usd')
   ```

2. **Handle errors gracefully** - check exit codes and stderr:

   ```bash
   if ! claude -p "$prompt" 2>error.log; then
       echo "Error occurred:" >&2
       cat error.log >&2
       exit 1
   fi
   ```

3. **Use session management** for maintaining context in multi-turn conversations

4. **Consider timeouts** for long-running operations:

   ```bash
   timeout 300 claude -p "$complex_prompt" || echo "Timed out after 5 minutes"
   ```

5. **Respect rate limits** when making multiple requests by adding delays between calls

## Real-world applications

The Claude Code SDK enables powerful integrations with your development workflow. One notable example is the [Claude Code GitHub Actions](/en/docs/claude-code/github-actions), which uses the SDK to provide automated code review, PR creation, and issue triage capabilities directly in your GitHub workflow.

## Related resources

* [CLI usage and controls](/en/docs/claude-code/cli-reference) - Complete CLI documentation
* [GitHub Actions integration](/en/docs/claude-code/github-actions) - Automate your GitHub workflow with Claude
* [Common workflows](/en/docs/claude-code/common-workflows) - Step-by-step guides for common use cases

----

> [!NOTE]
> # Get started with Claude Code hooks

> Learn how to customize and extend Claude Code's behavior by registering shell commands

Claude Code hooks are user-defined shell commands that execute at various points
in Claude Code's lifecycle. Hooks provide deterministic control over Claude
Code's behavior, ensuring certain actions always happen rather than relying on
the LLM to choose to run them.


  For reference documentation on hooks, see [Hooks reference](/en/docs/claude-code/hooks).


Example use cases for hooks include:

* **Notifications**: Customize how you get notified when Claude Code is awaiting
  your input or permission to run something.
* **Automatic formatting**: Run `prettier` on .ts files, `gofmt` on .go files,
  etc. after every file edit.
* **Logging**: Track and count all executed commands for compliance or
  debugging.
* **Feedback**: Provide automated feedback when Claude Code produces code that
  does not follow your codebase conventions.
* **Custom permissions**: Block modifications to production files or sensitive
  directories.

By encoding these rules as hooks rather than prompting instructions, you turn
suggestions into app-level code that executes every time it is expected to run.

<Warning>
  You must consider the security implication of hooks as you add them, because hooks run automatically during the agent loop with your current environment's credentials.
  For example, malicious hooks code can exfiltrate your data. Always review your hooks implementation before registering them.

  For full security best practices, see [Security Considerations](/en/docs/claude-code/hooks#security-considerations) in the hooks reference documentation.
</Warning>

## Hook Events Overview

Claude Code provides several hook events that run at different points in the workflow:

* **PreToolUse**: Runs before tool calls (can block them)
* **PostToolUse**: Runs after tool calls complete
* **Notification**: Runs when Claude Code sends notifications
* **Stop**: Runs when Claude Code finishes responding
* **SubagentStop**: Runs when subagent tasks complete

Each event receives different data and can control Claude's behavior in different ways.

## Quickstart

In this quickstart, you'll add a hook that logs the shell commands that Claude
Code runs.

### Prerequisites

Install `jq` for JSON processing in the command line.

### Step 1: Open hooks configuration

Run the `/hooks` [slash command](/en/docs/claude-code/slash-commands) and select
the `PreToolUse` hook event.

`PreToolUse` hooks run before tool calls and can block them while providing
Claude feedback on what to do differently.

### Step 2: Add a matcher

Select `+ Add new matcher…` to run your hook only on Bash tool calls.

Type `Bash` for the matcher.


  Use an empty string `""` to match all tools. The `*` character is not a valid matcher on its own.


### Step 3: Add the hook

Select `+ Add new hook…` and enter this command:

```bash
jq -r '"\(.tool_input.command) - \(.tool_input.description // "No description")"' >> ~/.claude/bash-command-log.txt
```

### Step 4: Save your configuration

For storage location, select `User settings` since you're logging to your home
directory. This hook will then apply to all projects, not just your current
project.

Then press Esc until you return to the REPL. Your hook is now registered!

### Step 5: Verify your hook

Run `/hooks` again or check `~/.claude/settings.json` to see your configuration:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '\"\\(.tool_input.command) - \\(.tool_input.description // \"No description\")\"' >> ~/.claude/bash-command-log.txt"
          }
        ]
      }
    ]
  }
}
```

### Step 6: Test your hook

Ask Claude to run a simple command like `ls` and check your log file:

```bash
cat ~/.claude/bash-command-log.txt
```

You should see entries like:

```
ls - Lists files and directories
```

## More Examples


  For a complete example implementation, see the [bash command validator example](https://github.com/anthropics/claude-code/blob/main/examples/hooks/bash_command_validator_example.py) in our public codebase.


### Code Formatting Hook

Automatically format TypeScript files after editing:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | { read file_path; if echo \"$file_path\" | grep -q '\\.ts$'; then npx prettier --write \"$file_path\"; fi; }"
          }
        ]
      }
    ]
  }
}
```

### Custom Notification Hook

Get desktop notifications when Claude needs input:

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "notify-send 'Claude Code' 'Awaiting your input'"
          }
        ]
      }
    ]
  }
}
```

### File Protection Hook

Block edits to sensitive files:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "python3 -c \"import json, sys; data=json.load(sys.stdin); path=data.get('tool_input',{}).get('file_path',''); sys.exit(2 if any(p in path for p in ['.env', 'package-lock.json', '.git/']) else 0)\""
          }
        ]
      }
    ]
  }
}
```

## Learn more

* For reference documentation on hooks, see [Hooks reference](/en/docs/claude-code/hooks).
* For comprehensive security best practices and safety guidelines, see [Security Considerations](/en/docs/claude-code/hooks#security-considerations) in the hooks reference documentation.
* For troubleshooting steps and debugging techniques, see [Debugging](/en/docs/claude-code/hooks#debugging) in the hooks reference documentation.

---

> [!NOTE]
> # Claude Code GitHub Actions

> Learn about integrating Claude Code into your development workflow with Claude Code GitHub Actions

Claude Code GitHub Actions brings AI-powered automation to your GitHub workflow. With a simple `@claude` mention in any PR or issue, Claude can analyze your code, create pull requests, implement features, and fix bugs - all while following your project's standards.

<Info>
  Claude Code GitHub Actions is currently in beta. Features and functionality may evolve as we refine the experience.
</Info>


  Claude Code GitHub Actions is built on top of the [Claude Code SDK](/en/docs/claude-code/sdk), which enables programmatic integration of Claude Code into your applications. You can use the SDK to build custom automation workflows beyond GitHub Actions.


## Why use Claude Code GitHub Actions?

* **Instant PR creation**: Describe what you need, and Claude creates a complete PR with all necessary changes
* **Automated code implementation**: Turn issues into working code with a single command
* **Follows your standards**: Claude respects your `CLAUDE.md` guidelines and existing code patterns
* **Simple setup**: Get started in minutes with our installer and API key
* **Secure by default**: Your code stays on Github's runners

## What can Claude do?

Claude Code provides powerful GitHub Actions that transform how you work with code:

### Claude Code Action

This GitHub Action allows you to run Claude Code within your GitHub Actions workflows. You can use this to build any custom workflow on top of Claude Code.

[View repository →](https://github.com/anthropics/claude-code-action)

### Claude Code Action (Base)

The foundation for building custom GitHub workflows with Claude. This extensible framework gives you full access to Claude's capabilities for creating tailored automation.

[View repository →](https://github.com/anthropics/claude-code-base-action)

## Setup

## Quick setup

The easiest way to set up this action is through Claude Code in the terminal. Just open claude and run `/install-github-app`.

This command will guide you through setting up the GitHub app and required secrets.


  * You must be a repository admin to install the GitHub app and add secrets
  * This quickstart method is only available for direct Anthropic API users. If you're using AWS Bedrock or Google Vertex AI, please see the [Using with AWS Bedrock & Google Vertex AI](#using-with-aws-bedrock-%26-google-vertex-ai) section.


## Manual setup

If the `/install-github-app` command fails or you prefer manual setup, please follow these manual setup instructions:

1. **Install the Claude GitHub app** to your repository: [https://github.com/apps/claude](https://github.com/apps/claude)
2. **Add ANTHROPIC\_API\_KEY** to your repository secrets ([Learn how to use secrets in GitHub Actions](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions))
3. **Copy the workflow file** from [examples/claude.yml](https://github.com/anthropics/claude-code-action/blob/main/examples/claude.yml) into your repository's `.github/workflows/`


  After completing either the quickstart or manual setup, test the action by tagging `@claude` in an issue or PR comment!


## Example use cases

Claude Code GitHub Actions can help you with a variety of tasks. For complete working examples, see the [examples directory](https://github.com/anthropics/claude-code-action/tree/main/examples).

### Turn issues into PRs

In an issue comment:

```
@claude implement this feature based on the issue description
```

Claude will analyze the issue, write the code, and create a PR for review.

### Get implementation help

In a PR comment:

```
@claude how should I implement user authentication for this endpoint?
```

Claude will analyze your code and provide specific implementation guidance.

### Fix bugs quickly

In an issue:

```yaml
@claude fix the TypeError in the user dashboard component
```

Claude will locate the bug, implement a fix, and create a PR.

## Best practices

### CLAUDE.md configuration

Create a `CLAUDE.md` file in your repository root to define code style guidelines, review criteria, project-specific rules, and preferred patterns. This file guides Claude's understanding of your project standards.

### Security considerations

<Warning>
  Never commit API keys directly to your repository!
</Warning>

Always use GitHub Secrets for API keys:

* Add your API key as a repository secret named `ANTHROPIC_API_KEY`
* Reference it in workflows: `anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}`
* Limit action permissions to only what's necessary
* Review Claude's suggestions before merging

Always use GitHub Secrets (e.g., `${{ secrets.ANTHROPIC_API_KEY }}`) rather than hardcoding API keys directly in your workflow files.

### Optimizing performance

Use issue templates to provide context, keep your `CLAUDE.md` concise and focused, and configure appropriate timeouts for your workflows.

### CI costs

When using Claude Code GitHub Actions, be aware of the associated costs:

**GitHub Actions costs:**

* Claude Code runs on GitHub-hosted runners, which consume your GitHub Actions minutes
* See [GitHub's billing documentation](https://docs.github.com/en/billing/managing-billing-for-your-products/managing-billing-for-github-actions/about-billing-for-github-actions) for detailed pricing and minute limits

**API costs:**

* Each Claude interaction consumes API tokens based on the length of prompts and responses
* Token usage varies by task complexity and codebase size
* See [Claude's pricing page](https://www.anthropic.com/api) for current token rates

**Cost optimization tips:**

* Use specific `@claude` commands to reduce unnecessary API calls
* Configure appropriate `max_turns` limits to prevent excessive iterations
* Set reasonable `timeout_minutes` to avoid runaway workflows
* Consider using GitHub's concurrency controls to limit parallel runs

## Configuration examples

For ready-to-use workflow configurations for different use cases, including:

* Basic workflow setup for issue and PR comments
* Automated code reviews on pull requests
* Custom implementations for specific needs

Visit the [examples directory](https://github.com/anthropics/claude-code-action/tree/main/examples) in the Claude Code Action repository.


  The examples repository includes complete, tested workflows that you can copy directly into your `.github/workflows/` directory.


## Using with AWS Bedrock & Google Vertex AI

For enterprise environments, you can use Claude Code GitHub Actions with your own cloud infrastructure. This approach gives you control over data residency and billing while maintaining the same functionality.

### Prerequisites

Before setting up Claude Code GitHub Actions with cloud providers, you need:

#### For Google Cloud Vertex AI:

1. A Google Cloud Project with Vertex AI enabled
2. Workload Identity Federation configured for GitHub Actions
3. A service account with the required permissions
4. A GitHub App (recommended) or use the default GITHUB\_TOKEN

#### For AWS Bedrock:

1. An AWS account with Amazon Bedrock enabled
2. GitHub OIDC Identity Provider configured in AWS
3. An IAM role with Bedrock permissions
4. A GitHub App (recommended) or use the default GITHUB\_TOKEN



Create a custom GitHub App (Recommended for 3P Providers)">
For best control and security when using 3P providers like Vertex AI or Bedrock, we recommend creating your own GitHub App:

1. Go to [https://github.com/settings/apps/new](https://github.com/settings/apps/new)
2. Fill in the basic information:
   * **GitHub App name**: Choose a unique name (e.g., "YourOrg Claude Assistant")
   * **Homepage URL**: Your organization's website or the repository URL
1. Configure the app settings:
   * **Webhooks**: Uncheck "Active" (not needed for this integration)
1. Set the required permissions:
   * **Repository permissions**:
	 * Contents: Read & Write
	 * Issues: Read & Write
	 * Pull requests: Read & Write
1. Click "Create GitHub App"
2. After creation, click "Generate a private key" and save the downloaded `.pem` file
3. Note your App ID from the app settings page
4. Install the app to your repository:
   * From your app's settings page, click "Install App" in the left sidebar
   * Select your account or organization
   * Choose "Only select repositories" and select the specific repository
   * Click "Install"
1. Add the private key as a secret to your repository:
   * Go to your repository's Settings → Secrets and variables → Actions
   * Create a new secret named `APP_PRIVATE_KEY` with the contents of the `.pem` file
1. Add the App ID as a secret:

* Create a new secret named `APP_ID` with your GitHub App's ID


  This app will be used with the [actions/create-github-app-token](https://github.com/actions/create-github-app-token) action to generate authentication tokens in your workflows.


**Alternative for Anthropic API or if you don't want to setup your own Github app**: Use the official Anthropic app:

1. Install from: [https://github.com/apps/claude](https://github.com/apps/claude)
2. No additional configuration needed for authentication


Configure cloud provider authentication">
Choose your cloud provider and set up secure authentication:



AWS Bedrock
**Configure AWS to allow GitHub Actions to authenticate securely without storing credentials.**

> **Security Note**: Use repository-specific configurations and grant only the minimum required permissions.

**Required Setup**:

1. **Enable Amazon Bedrock**:
   * Request access to Claude models in Amazon Bedrock
   * For cross-region models, request access in all required regions

1. **Set up GitHub OIDC Identity Provider**:
   * Provider URL: `https://token.actions.githubusercontent.com`
   * Audience: `sts.amazonaws.com`

1. **Create IAM Role for GitHub Actions**:
   * Trusted entity type: Web identity
   * Identity provider: `token.actions.githubusercontent.com`
   * Permissions: `AmazonBedrockFullAccess` policy
   * Configure trust policy for your specific repository

**Required Values**:

After setup, you'll need:

* **AWS\_ROLE\_TO\_ASSUME**: The ARN of the IAM role you created


  OIDC is more secure than using static AWS access keys because credentials are temporary and automatically rotated.


See [AWS documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html) for detailed OIDC setup instructions.


  Google Vertex AI">
	**Configure Google Cloud to allow GitHub Actions to authenticate securely without storing credentials.**

> **Security Note**: Use repository-specific configurations and grant only the minimum required permissions.

**Required Setup**:

1. **Enable APIs** in your Google Cloud project:
   * IAM Credentials API
   * Security Token Service (STS) API
   * Vertex AI API

1. **Create Workload Identity Federation resources**:
   * Create a Workload Identity Pool
   * Add a GitHub OIDC provider with:
	 * Issuer: `https://token.actions.githubusercontent.com`
	 * Attribute mappings for repository and owner
	 * **Security recommendation**: Use repository-specific attribute conditions

1. **Create a Service Account**:
   * Grant only `Vertex AI User` role
   * **Security recommendation**: Create a dedicated service account per repository

1. **Configure IAM bindings**:
   * Allow the Workload Identity Pool to impersonate the service account
   * **Security recommendation**: Use repository-specific principal sets

**Required Values**:

After setup, you'll need:

* **GCP\_WORKLOAD\_IDENTITY\_PROVIDER**: The full provider resource name
* **GCP\_SERVICE\_ACCOUNT**: The service account email address


  Workload Identity Federation eliminates the need for downloadable service account keys, improving security.


For detailed setup instructions, consult the [Google Cloud Workload Identity Federation documentation](https://cloud.google.com/iam/docs/workload-identity-federation).


Add Required Secrets">
Add the following secrets to your repository (Settings → Secrets and variables → Actions):

#### For Anthropic API (Direct):

1. **For API Authentication**:
* `ANTHROPIC_API_KEY`: Your Anthropic API key from [console.anthropic.com](https://console.anthropic.com)

1. **For GitHub App (if using your own app)**:
* `APP_ID`: Your GitHub App's ID
* `APP_PRIVATE_KEY`: The private key (.pem) content

#### For Google Cloud Vertex AI

1. **For GCP Authentication**:
* `GCP_WORKLOAD_IDENTITY_PROVIDER`
* `GCP_SERVICE_ACCOUNT`

1. **For GitHub App (if using your own app)**:
* `APP_ID`: Your GitHub App's ID
* `APP_PRIVATE_KEY`: The private key (.pem) content

#### For AWS Bedrock

1. **For AWS Authentication**:
* `AWS_ROLE_TO_ASSUME`

1. **For GitHub App (if using your own app)**:
* `APP_ID`: Your GitHub App's ID
* `APP_PRIVATE_KEY`: The private key (.pem) content


Create workflow files">
Create GitHub Actions workflow files that integrate with your cloud provider. The examples below show complete configurations for both AWS Bedrock and Google Vertex AI:


AWS Bedrock workflow">
**Prerequisites:**

* AWS Bedrock access enabled with Claude model permissions
* GitHub configured as an OIDC identity provider in AWS
* IAM role with Bedrock permissions that trusts GitHub Actions

**Required GitHub secrets:**

| Secret Name          | Description                                       |
| -------------------- | ------------------------------------------------- |
| `AWS_ROLE_TO_ASSUME` | ARN of the IAM role for Bedrock access            |
| `APP_ID`             | Your GitHub App ID (from app settings)            |
| `APP_PRIVATE_KEY`    | The private key you generated for your GitHub App |

```yaml
name: Claude PR Action 

permissions:
contents: write
pull-requests: write
issues: write
id-token: write 

on:
issue_comment:
types: [created]
pull_request_review_comment:
types: [created]
issues:
types: [opened, assigned]

jobs:
claude-pr:
if: |
(github.event_name == 'issue_comment' && contains(github.event.comment.body, '@claude')) ||
(github.event_name == 'pull_request_review_comment' && contains(github.event.comment.body, '@claude')) ||
(github.event_name == 'issues' && contains(github.event.issue.body, '@claude'))
runs-on: ubuntu-latest
env:
AWS_REGION: us-west-2
steps:
- name: Checkout repository
uses: actions/checkout@v4

- name: Generate GitHub App token
id: app-token
uses: actions/create-github-app-token@v2
with:
app-id: ${{ secrets.APP_ID }}
private-key: ${{ secrets.APP_PRIVATE_KEY }}

- name: Configure AWS Credentials (OIDC)
uses: aws-actions/configure-aws-credentials@v4
with:
role-to-assume: ${{ secrets.AWS_ROLE_TO_ASSUME }}
aws-region: us-west-2

- uses: ./.github/actions/claude-pr-action
with:
trigger_phrase: "@claude"
timeout_minutes: "60"
github_token: ${{ steps.app-token.outputs.token }}
use_bedrock: "true"
model: "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
```


The model ID format for Bedrock includes the region prefix (e.g., `us.anthropic.claude...`) and version suffix.



Google Vertex AI workflow">
**Prerequisites:**

* Vertex AI API enabled in your GCP project
* Workload Identity Federation configured for GitHub
* Service account with Vertex AI permissions

**Required GitHub secrets:**

| Secret Name                      | Description                                       |
| -------------------------------- | ------------------------------------------------- |
| `GCP_WORKLOAD_IDENTITY_PROVIDER` | Workload identity provider resource name          |
| `GCP_SERVICE_ACCOUNT`            | Service account email with Vertex AI access       |
| `APP_ID`                         | Your GitHub App ID (from app settings)            |
| `APP_PRIVATE_KEY`                | The private key you generated for your GitHub App |

```yaml
name: Claude PR Action

permissions:
contents: write
pull-requests: write
issues: write
id-token: write  

on:
issue_comment:
types: [created]
pull_request_review_comment:
types: [created]
issues:
types: [opened, assigned]

jobs:
claude-pr:
if: |
(github.event_name == 'issue_comment' && contains(github.event.comment.body, '@claude')) ||
(github.event_name == 'pull_request_review_comment' && contains(github.event.comment.body, '@claude')) ||
(github.event_name == 'issues' && contains(github.event.issue.body, '@claude'))
runs-on: ubuntu-latest
steps:
- name: Checkout repository
uses: actions/checkout@v4

- name: Generate GitHub App token
id: app-token
uses: actions/create-github-app-token@v2
with:
app-id: ${{ secrets.APP_ID }}
private-key: ${{ secrets.APP_PRIVATE_KEY }}

- name: Authenticate to Google Cloud
id: auth
uses: google-github-actions/auth@v2
with:
workload_identity_provider: ${{ secrets.GCP_WORKLOAD_IDENTITY_PROVIDER }}
service_account: ${{ secrets.GCP_SERVICE_ACCOUNT }}

- uses: ./.github/actions/claude-pr-action
with:
trigger_phrase: "@claude"
timeout_minutes: "60"
github_token: ${{ steps.app-token.outputs.token }}
use_vertex: "true"
model: "claude-3-7-sonnet@20250219"
env:
ANTHROPIC_VERTEX_PROJECT_ID: ${{ steps.auth.outputs.project_id }}
CLOUD_ML_REGION: us-east5
VERTEX_REGION_CLAUDE_3_7_SONNET: us-east5
```


The project ID is automatically retrieved from the Google Cloud authentication step, so you don't need to hardcode it.


## Troubleshooting

### Claude not responding to @claude commands

Verify the GitHub App is installed correctly, check that workflows are enabled, ensure API key is set in repository secrets, and confirm the comment contains `@claude` (not `/claude`).

### CI not running on Claude's commits

Ensure you're using the GitHub App or custom app (not Actions user), check workflow triggers include the necessary events, and verify app permissions include CI triggers.

### Authentication errors

Confirm API key is valid and has sufficient permissions. For Bedrock/Vertex, check credentials configuration and ensure secrets are named correctly in workflows.

## Advanced configuration

### Action parameters

The Claude Code Action supports these key parameters:

| Parameter           | Description                    | Required |
| ------------------- | ------------------------------ | -------- |
| `prompt`            | The prompt to send to Claude   | Yes\*    |
| `prompt_file`       | Path to file containing prompt | Yes\*    |
| `anthropic_api_key` | Anthropic API key              | Yes\*\*  |
| `max_turns`         | Maximum conversation turns     | No       |
| `timeout_minutes`   | Execution timeout              | No       |

\*Either `prompt` or `prompt_file` required\
\*\*Required for direct Anthropic API, not for Bedrock/Vertex

### Alternative integration methods

While the `/install-github-app` command is the recommended approach, you can also:

* **Custom GitHub App**: For organizations needing branded usernames or custom authentication flows. Create your own GitHub App with required permissions (contents, issues, pull requests) and use the actions/create-github-app-token action to generate tokens in your workflows.
* **Manual GitHub Actions**: Direct workflow configuration for maximum flexibility
* **MCP Configuration**: Dynamic loading of Model Context Protocol servers

See the [Claude Code Action repository](https://github.com/anthropics/claude-code-action) for detailed documentation.

### Customizing Claude's behavior

You can configure Claude's behavior in two ways:

1. **CLAUDE.md**: Define coding standards, review criteria, and project-specific rules in a `CLAUDE.md` file at the root of your repository. Claude will follow these guidelines when creating PRs and responding to requests. Check out our [Memory documentation](/en/docs/claude-code/memory) for more details.
2. **Custom prompts**: Use the `prompt` parameter in the workflow file to provide workflow-specific instructions. This allows you to customize Claude's behavior for different workflows or tasks.

Claude will follow these guidelines when creating PRs and responding to requests.

---

---

> [!NOTE]
> # Model Context Protocol (MCP)

> Learn how to set up MCP with Claude Code.

Model Context Protocol (MCP) is an open protocol that enables LLMs to access external tools and data sources. For more details about MCP, see the [MCP documentation](https://modelcontextprotocol.io/introduction).


> [!NOTE]
>   Use third party MCP servers at your own risk. Make sure you trust the MCP
>   servers, and be especially careful when using MCP servers that talk to the
>   internet, as these can expose you to prompt injection risk.


## Configure MCP servers


Add an MCP stdio Server
```bash
# Basic syntax
claude mcp add <name> <command> [args...]

# Example: Adding a local server
claude mcp add my-server -e API_KEY=123 -- /path/to/server arg1 arg2
```


Add an MCP SSE Server
```bash
# Basic syntax
claude mcp add --transport sse <name> <url>

# Example: Adding an SSE server
claude mcp add --transport sse sse-server https://example.com/sse-endpoint

# Example: Adding an SSE server with custom headers
claude mcp add --transport sse api-server https://api.example.com/mcp --header "X-API-Key: your-key"
```


Add an MCP HTTP Server
```bash
# Basic syntax
claude mcp add --transport http <name> <url>

# Example: Adding a streamable HTTP server
claude mcp add --transport http http-server https://example.com/mcp

# Example: Adding an HTTP server with authentication header
claude mcp add --transport http secure-server https://api.example.com/mcp --header "Authorization: Bearer your-token"
```


Manage your MCP servers
```bash
# List all configured servers
claude mcp list

# Get details for a specific server
claude mcp get my-server

# Remove a server
claude mcp remove my-server
```




  Tips:

* Use the `-s` or `--scope` flag to specify where the configuration is stored:
* `local` (default): Available only to you in the current project (was called `project` in older versions)
* `project`: Shared with everyone in the project via `.mcp.json` file
* `user`: Available to you across all projects (was called `global` in older versions)
* Set environment variables with `-e` or `--env` flags (e.g., `-e KEY=value`)
* Configure MCP server startup timeout using the MCP\_TIMEOUT environment variable (e.g., `MCP_TIMEOUT=10000 claude` sets a 10-second timeout)
* Check MCP server status any time using the `/mcp` command within Claude Code
* MCP follows a client-server architecture where Claude Code (the client) can connect to multiple specialized servers
* Claude Code supports SSE (Server-Sent Events) and streamable HTTP servers for real-time communication
* Use `/mcp` to authenticate with remote servers that require OAuth 2.0 authentication


## Understanding MCP server scopes

MCP servers can be configured at three different scope levels, each serving distinct purposes for managing server accessibility and sharing. Understanding these scopes helps you determine the best way to configure servers for your specific needs.

### Scope hierarchy and precedence

MCP server configurations follow a clear precedence hierarchy. When servers with the same name exist at multiple scopes, the system resolves conflicts by prioritizing local-scoped servers first, followed by project-scoped servers, and finally user-scoped servers. This design ensures that personal configurations can override shared ones when needed.

### Local scope

Local-scoped servers represent the default configuration level and are stored in your project-specific user settings. These servers remain private to you and are only accessible when working within the current project directory. This scope is ideal for personal development servers, experimental configurations, or servers containing sensitive credentials that shouldn't be shared.

```bash
# Add a local-scoped server (default)
claude mcp add my-private-server /path/to/server

# Explicitly specify local scope
claude mcp add my-private-server -s local /path/to/server
```

### Project scope

Project-scoped servers enable team collaboration by storing configurations in a `.mcp.json` file at your project's root directory. This file is designed to be checked into version control, ensuring all team members have access to the same MCP tools and services. When you add a project-scoped server, Claude Code automatically creates or updates this file with the appropriate configuration structure.

```bash
# Add a project-scoped server
claude mcp add shared-server -s project /path/to/server
```

The resulting `.mcp.json` file follows a standardized format:

```json
{
  "mcpServers": {
    "shared-server": {
      "command": "/path/to/server",
      "args": [],
      "env": {}
    }
  }
}
```

For security reasons, Claude Code prompts for approval before using project-scoped servers from `.mcp.json` files. If you need to reset these approval choices, use the `claude mcp reset-project-choices` command.

### User scope

User-scoped servers provide cross-project accessibility, making them available across all projects on your machine while remaining private to your user account. This scope works well for personal utility servers, development tools, or services you frequently use across different projects.

```bash
# Add a user server
claude mcp add my-user-server -s user /path/to/server
```

### Choosing the right scope

Select your scope based on:

* **Local scope**: Personal servers, experimental configurations, or sensitive credentials specific to one project
* **Project scope**: Team-shared servers, project-specific tools, or services required for collaboration
* **User scope**: Personal utilities needed across multiple projects, development tools, or frequently-used services

### Environment variable expansion in `.mcp.json`

Claude Code supports environment variable expansion in `.mcp.json` files, allowing teams to share configurations while maintaining flexibility for machine-specific paths and sensitive values like API keys.

**Supported syntax:**

* `${VAR}` - Expands to the value of environment variable `VAR`
* `${VAR:-default}` - Expands to `VAR` if set, otherwise uses `default`

**Expansion locations:**
Environment variables can be expanded in:

* `command` - The server executable path
* `args` - Command-line arguments
* `env` - Environment variables passed to the server
* `url` - For SSE/HTTP server types
* `headers` - For SSE/HTTP server authentication

**Example with variable expansion:**

```json
{
  "mcpServers": {
    "api-server": {
      "type": "sse",
      "url": "${API_BASE_URL:-https://api.example.com}/mcp",
      "headers": {
        "Authorization": "Bearer ${API_KEY}"
      }
    }
  }
}
```

If a required environment variable is not set and has no default value, Claude Code will fail to parse the config.

## Authenticate with remote MCP servers

Many remote MCP servers require authentication. Claude Code supports OAuth 2.0 authentication flow for secure connection to these servers.


Add a remote server requiring authentication">
```bash
# Add an SSE or HTTP server that requires OAuth
claude mcp add --transport sse github-server https://api.github.com/mcp
```


Authenticate using the /mcp command">
Within Claude Code, use the `/mcp` command to manage authentication:

```
> /mcp
```

This opens an interactive menu where you can:

* View connection status for all servers
* Authenticate with servers requiring OAuth
* Clear existing authentication
* View server capabilities


Complete the OAuth flow">
When you select "Authenticate" for a server:

1. Your browser opens automatically to the OAuth provider
2. Complete the authentication in your browser
3. Claude Code receives and securely stores the access token
4. The server connection becomes active


  Tips:

  * Authentication tokens are stored securely and refreshed automatically
  * Use "Clear authentication" in the `/mcp` menu to revoke access
  * If your browser doesn't open automatically, copy the provided URL
  * OAuth authentication works with both SSE and HTTP transports


## Connect to a Postgres MCP server

Suppose you want to give Claude read-only access to a PostgreSQL database for querying and schema inspection.


  Add the Postgres MCP server">
```bash
claude mcp add postgres-server /path/to/postgres-mcp-server --connection-string "postgresql://user:pass@localhost:5432/mydb"
```


Query your database with Claude">
```
> describe the schema of our users table
```

```
> what are the most recent orders in the system?
```

```
> show me the relationship between customers and invoices
```




  Tips:

  * The Postgres MCP server provides read-only access for safety
  * Claude can help you explore database structure and run analytical queries
  * You can use this to quickly understand database schemas in unfamiliar projects
  * Make sure your connection string uses appropriate credentials with minimum required permissions


## Add MCP servers from JSON configuration

Suppose you have a JSON configuration for a single MCP server that you want to add to Claude Code.


Add an MCP server from JSON">
```bash
# Basic syntax
claude mcp add-json <name> '<json>'

# Example: Adding a stdio server with JSON configuration
claude mcp add-json weather-api '{"type":"stdio","command":"/path/to/weather-cli","args":["--api-key","abc123"],"env":{"CACHE_DIR":"/tmp"}}'
```


Verify the server was added">
```bash
claude mcp get weather-api
```




Tips:

* Make sure the JSON is properly escaped in your shell
* The JSON must conform to the MCP server configuration schema
* You can use `-s global` to add the server to your global configuration instead of the project-specific one


## Import MCP servers from Claude Desktop

Suppose you have already configured MCP servers in Claude Desktop and want to use the same servers in Claude Code without manually reconfiguring them.


Import servers from Claude Desktop">
```bash
# Basic syntax 
claude mcp add-from-claude-desktop 
```


Select which servers to import">
After running the command, you'll see an interactive dialog that allows you to select which servers you want to import.


Verify the servers were imported">
```bash
claude mcp list 
```




Tips:

* This feature only works on macOS and Windows Subsystem for Linux (WSL)
* It reads the Claude Desktop configuration file from its standard location on those platforms
* Use the `-s global` flag to add servers to your global configuration
* Imported servers will have the same names as in Claude Desktop
* If servers with the same names already exist, they will get a numerical suffix (e.g., `server_1`)


## Use Claude Code as an MCP server

Suppose you want to use Claude Code itself as an MCP server that other applications can connect to, providing them with Claude's tools and capabilities.


Start Claude as an MCP server">
```bash
# Basic syntax
claude mcp serve
```


Connect from another application">
You can connect to Claude Code MCP server from any MCP client, such as Claude Desktop. If you're using Claude Desktop, you can add the Claude Code MCP server using this configuration:

```json
{
  "command": "claude",
  "args": ["mcp", "serve"],
  "env": {}
}
```




Tips:

* The server provides access to Claude's tools like View, Edit, LS, etc.
* In Claude Desktop, try asking Claude to read files in a directory, make edits, and more.
* Note that this MCP server is simply exposing Claude Code's tools to your MCP client, so your own client is responsible for implementing user confirmation for individual tool calls.


## Use MCP resources

MCP servers can expose resources that you can reference using @ mentions, similar to how you reference files.

### Reference MCP resources


List available resources">
Type `@` in your prompt to see available resources from all connected MCP servers. Resources appear alongside files in the autocomplete menu.


Reference a specific resource">
Use the format `@server:protocol://resource/path` to reference a resource:

```
> Can you analyze @github:issue://123 and suggest a fix?
```

```
> Please review the API documentation at @docs:file://api/authentication
```


Multiple resource references
You can reference multiple resources in a single prompt:

```
> Compare @postgres:schema://users with @docs:file://database/user-model
```



Tips:

* Resources are automatically fetched and included as attachments when referenced
* Resource paths are fuzzy-searchable in the @ mention autocomplete
* Claude Code automatically provides tools to list and read MCP resources when servers support them
* Resources can contain any type of content that the MCP server provides (text, JSON, structured data, etc.)


## Use MCP prompts as slash commands

MCP servers can expose prompts that become available as slash commands in Claude Code.

### Execute MCP prompts


Discover available prompts
Type `/` to see all available commands, including those from MCP servers. MCP prompts appear with the format `/mcp__servername__promptname`.


Execute a prompt without arguments
```
> /mcp__github__list_prs
```


Execute a prompt with arguments
Many prompts accept arguments. Pass them space-separated after the command:

```
> /mcp__github__pr_review 456
```

```
> /mcp__jira__create_issue "Bug in login flow" high
```


  Tips:

  * MCP prompts are dynamically discovered from connected servers
  * Arguments are parsed based on the prompt's defined parameters
  * Prompt results are injected directly into the conversation
  * Server and prompt names are normalized (spaces become underscores)


---
---

> [!NOTE]
> # Troubleshooting

> Discover solutions to common issues with Claude Code installation and usage.

## Common installation issues

### Windows installation issues: errors in WSL

You might encounter the following issues in WSL:

**OS/platform detection issues**: If you receive an error during installation, WSL may be using Windows `npm`. Try:

* Run `npm config set os linux` before installation
* Install with `npm install -g @anthropic-ai/claude-code --force --no-os-check` (Do NOT use `sudo`)

**Node not found errors**: If you see `exec: node: not found` when running `claude`, your WSL environment may be using a Windows installation of Node.js. You can confirm this with `which npm` and `which node`, which should point to Linux paths starting with `/usr/` rather than `/mnt/c/`. To fix this, try installing Node via your Linux distribution's package manager or via [`nvm`](https://github.com/nvm-sh/nvm).

### Linux installation issues: permission errors

When installing Claude Code with npm, you may encounter permission errors if your npm global prefix is not user writable (eg. `/usr`, or `/usr/local`).

#### Recommended solution: Migrate to local installation

The simplest solution is to migrate to a local installation:

```bash
claude migrate-installer
```

This moves Claude Code to `~/.claude/local/` and sets up an alias in your shell configuration. No `sudo` is required for future updates.

After migration, restart your shell, and then verify your installation:

```bash
which claude  # Should show an alias to ~/.claude/local/claude
claude doctor # Check installation health
```

#### Alternative solution: Create a user-writable npm prefix for global installs

You can configure npm to use a directory within your home folder:

```bash
# First, save a list of your existing global packages for later migration
npm list -g --depth=0 > ~/npm-global-packages.txt

# Create a directory for your global packages
mkdir -p ~/.npm-global

# Configure npm to use the new directory path
npm config set prefix ~/.npm-global

# Note: Replace ~/.bashrc with ~/.zshrc, ~/.profile, or other appropriate file for your shell
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc

# Apply the new PATH setting
source ~/.bashrc

# Now reinstall Claude Code in the new location
npm install -g @anthropic-ai/claude-code

# Optional: Reinstall your previous global packages in the new location
# Look at ~/npm-global-packages.txt and install packages you want to keep
```

This solution:

* Avoids modifying system directory permissions
* Creates a clean, dedicated location for your global npm packages
* Follows security best practices

#### System Recovery: If you have run commands that change ownership and permissions of system files or similar

If you've already run a command that changed system directory permissions (such as `sudo chown -R $USER:$(id -gn) /usr && sudo chmod -R u+w /usr`) and your system is now broken (for example, if you see `sudo: /usr/bin/sudo must be owned by uid 0 and have the setuid bit set`), you'll need to perform recovery steps.

##### Ubuntu/Debian Recovery Method:

1. While rebooting, hold **SHIFT** to access the GRUB menu

2. Select "Advanced options for Ubuntu/Debian"

3. Choose the recovery mode option

4. Select "Drop to root shell prompt"

5. Remount the filesystem as writable:
   ```bash
   mount -o remount,rw /
   ```

6. Fix permissions:

   ```bash
   # Restore root ownership
   chown -R root:root /usr
   chmod -R 755 /usr

   # Ensure /usr/local is owned by your user for npm packages
   chown -R YOUR_USERNAME:YOUR_USERNAME /usr/local

   # Set setuid bit for critical binaries
   chmod u+s /usr/bin/sudo
   chmod 4755 /usr/bin/sudo
   chmod u+s /usr/bin/su
   chmod u+s /usr/bin/passwd
   chmod u+s /usr/bin/newgrp
   chmod u+s /usr/bin/gpasswd
   chmod u+s /usr/bin/chsh
   chmod u+s /usr/bin/chfn

   # Fix sudo configuration
   chown root:root /usr/libexec/sudo/sudoers.so
   chmod 4755 /usr/libexec/sudo/sudoers.so
   chown root:root /etc/sudo.conf
   chmod 644 /etc/sudo.conf
   ```

7. Reinstall affected packages (optional but recommended):

   ```bash
   # Save list of installed packages
   dpkg --get-selections > /tmp/installed_packages.txt

   # Reinstall them
   awk '{print $1}' /tmp/installed_packages.txt | xargs -r apt-get install --reinstall -y
   ```

8. Reboot:
   ```bash
   reboot
   ```

##### Alternative Live USB Recovery Method:

If the recovery mode doesn't work, you can use a live USB:

1. Boot from a live USB (Ubuntu, Debian, or any Linux distribution)

2. Find your system partition:
   ```bash
   lsblk
   ```

3. Mount your system partition:
   ```bash
   sudo mount /dev/sdXY /mnt  # replace sdXY with your actual system partition
   ```

4. If you have a separate boot partition, mount it too:
   ```bash
   sudo mount /dev/sdXZ /mnt/boot  # if needed
   ```

5. Chroot into your system:

   ```bash
   # For Ubuntu/Debian:
   sudo chroot /mnt

   # For Arch-based systems:
   sudo arch-chroot /mnt
   ```

6. Follow steps 6-8 from the Ubuntu/Debian recovery method above

After restoring your system, follow the recommended solution above to set up a user-writable npm prefix.

## Auto-updater issues

If Claude Code can't update automatically (see [Update Claude Code](/en/docs/claude-code/setup#update-claude-code) for how updates work):

### For permission errors

This is typically due to permission issues with your npm global prefix directory. You have several options:

1. **Migrate to local installation** (recommended): Run `claude migrate-installer` to move to a local installation that avoids permission issues entirely
2. **Update manually**: Run `claude update` with appropriate permissions
3. **Fix npm permissions**: Follow the [recommended solution](#recommended-solution-create-a-user-writable-npm-prefix) above (more complex)

### To disable auto-updates

If you prefer to control when Claude Code updates:

```bash
# Via configuration
claude config set autoUpdates false --global

# Or via environment variable
export DISABLE_AUTOUPDATER=1
```

### To check your installation

* **Current version and diagnostics**: Run `claude doctor`
* **Check for updates**: Run `claude update`
* **View update settings**: Run `claude config get autoUpdates --global`
* **Verify installation location**: Run `which claude` - if this shows an alias pointing to `~/.claude/local/claude`, you're using the recommended local installation

## Permissions and authentication

### Repeated permission prompts

If you find yourself repeatedly approving the same commands, you can allow specific tools
to run without approval using the `/permissions` command. See [Permissions docs](/en/docs/claude-code/iam#configuring-permissions).

### Authentication issues

If you're experiencing authentication problems:

1. Run `/logout` to sign out completely
2. Close Claude Code
3. Restart with `claude` and complete the authentication process again

If problems persist, try:

```bash
rm -rf ~/.config/claude-code/auth.json
claude
```

This removes your stored authentication information and forces a clean login.

## Performance and stability

### High CPU or memory usage

Claude Code is designed to work with most development environments, but may consume significant resources when processing large codebases. If you're experiencing performance issues:

1. Use `/compact` regularly to reduce context size
2. Close and restart Claude Code between major tasks
3. Consider adding large build directories to your `.gitignore` file

### Command hangs or freezes

If Claude Code seems unresponsive:

1. Press Ctrl+C to attempt to cancel the current operation
2. If unresponsive, you may need to close the terminal and restart

### ESC key not working in JetBrains (IntelliJ, PyCharm, etc.) terminals

If you're using Claude Code in JetBrains terminals and the ESC key doesn't interrupt the agent as expected, this is likely due to a keybinding clash with JetBrains' default shortcuts.

To fix this issue:

1. Go to Settings → Tools → Terminal
2. Click the "Configure terminal keybindings" hyperlink next to "Override IDE Shortcuts"
3. Within the terminal keybindings, scroll down to "Switch focus to Editor" and delete that shortcut

This will allow the ESC key to properly function for canceling Claude Code operations instead of being captured by PyCharm's "Switch focus to Editor" action.

## Getting more help

If you're experiencing issues not covered here:

1. Use the `/bug` command within Claude Code to report problems directly to Anthropic
2. Check the [GitHub repository](https://github.com/anthropics/claude-code) for known issues
3. Run `/doctor` to check the health of your Claude Code installation


---
---

> [!NOTE]
> # Set up Claude Code

> Install, authenticate, and start using Claude Code on your development machine.

## System requirements

* **Operating Systems**: macOS 10.15+, Ubuntu 20.04+/Debian 10+, or Windows 10+ (with WSL 1, WSL 2, or Git for Windows)
* **Hardware**: 4GB+ RAM
* **Software**: [Node.js 18+](https://nodejs.org/en/download)
* **Network**: Internet connection required for authentication and AI processing
* **Shell**: Works best in Bash, Zsh or Fish
* **Location**: [Anthropic supported countries](https://www.anthropic.com/supported-countries)

## Standard installation

To install Claude Code, run the following command:

```sh
npm install -g @anthropic-ai/claude-code
```

<Warning>
  Do NOT use `sudo npm install -g` as this can lead to permission issues and security risks.
  If you encounter permission errors, see [configure Claude Code](/en/docs/claude-code/troubleshooting#linux-permission-issues) for recommended solutions.
</Warning>

<Note>
  Some users may be automatically migrated to an improved installation method.
  Run `claude doctor` after installation to check your installation type.
</Note>

After the installation process completes, navigate to your project and start Claude Code:

```bash
cd your-awesome-project
claude
```

Claude Code offers the following authentication options:

1. **Anthropic Console**: The default option. Connect through the Anthropic Console and complete the OAuth process. Requires active billing at [console.anthropic.com](https://console.anthropic.com).
2. **Claude App (with Pro or Max plan)**: Subscribe to Claude's [Pro or Max plan](https://www.anthropic.com/pricing) for a unified subscription that includes both Claude Code and the web interface. Get more value at the same price point while managing your account in one place. Log in with your Claude.ai account. During launch, choose the option that matches your subscription type.
3. **Enterprise platforms**: Configure Claude Code to use [Amazon Bedrock or Google Vertex AI](/en/docs/claude-code/third-party-integrations) for enterprise deployments with your existing cloud infrastructure.

## Windows setup

**Option 1: Claude Code within WSL**

* Both WSL 1 and WSL 2 are supported

**Option 2: Claude Code on native Windows with Git Bash**

* Requires [Git for Windows](https://git-scm.com/downloads/win)
* For portable Git installations, specify the path to your `bash.exe`:
  ```powershell
  $env:CLAUDE_CODE_GIT_BASH_PATH="C:\Program Files\Git\bin\bash.exe"
  ```

## Alternative installation methods

Claude Code offers multiple installation methods to suit different environments.

If you encounter any issues during installation, consult the [troubleshooting guide](/en/docs/claude-code/troubleshooting#linux-permission-issues).

<Tip>
  Run `claude doctor` after installation to check your installation type and version.
</Tip>

### Global npm installation

Traditional method shown in the [install steps above](#install-and-authenticate)

### Local installation

* After global install via npm, use `claude migrate-installer` to move to local
* Avoids autoupdater npm permission issues
* Some users may be automatically migrated to this method

### Native binary installation (Alpha)

* Use `claude install` from an existing installation
* or `curl -fsSL claude.ai/install.sh | bash` for a fresh install
* Currently in alpha testing
* Platform support: macOS, Linux, Windows (via WSL)

## Running on AWS or GCP

By default, Claude Code uses Anthropic's API.

For details on running Claude Code on AWS or GCP, see [third-party integrations](/en/docs/claude-code/third-party-integrations).

## Update Claude Code

### Auto updates

Claude Code automatically keeps itself up to date to ensure you have the latest features and security fixes.

* **Update checks**: Performed on startup and periodically while running
* **Update process**: Downloads and installs automatically in the background
* **Notifications**: You'll see a notification when updates are installed
* **Applying updates**: Updates take effect the next time you start Claude Code

**Disable auto-updates:**

```bash
# Via configuration
claude config set autoUpdates false --global

# Or via environment variable
export DISABLE_AUTOUPDATER=1
```

### Update manually

```bash
claude update
```

---
---

> [!NOTE]
> # Identity and Access Management

> Learn how to configure user authentication, authorization, and access controls for Claude Code in your organization.

## Authentication methods

Setting up Claude Code requires access to Anthropic models. For teams, you can set up Claude Code access in one of three ways:

* Anthropic API via the Anthropic Console
* Amazon Bedrock
* Google Vertex AI

### Anthropic API authentication

**To set up Claude Code access for your team via Anthropic API:**

1. Use your existing Anthropic Console account or create a new Anthropic Console account
2. You can add users through either method below:
   * Bulk invite users from within the Console (Console -> Settings -> Members -> Invite)
   * [Set up SSO](https://support.anthropic.com/en/articles/10280258-setting-up-single-sign-on-on-the-api-console)
3. When inviting users, they need one of the following roles:
   * "Claude Code" role means users can only create Claude Code API keys
   * "Developer" role means users can create any kind of API key
4. Each invited user needs to complete these steps:
   * Accept the Console invite
   * [Check system requirements](/en/docs/claude-code/setup#system-requirements)
   * [Install Claude Code](/en/docs/claude-code/setup#installation)
   * Login with Console account credentials

### Cloud provider authentication

**To set up Claude Code access for your team via Bedrock or Vertex:**

1. Follow the [Bedrock docs](/en/docs/claude-code/amazon-bedrock) or [Vertex docs](/en/docs/claude-code/google-vertex-ai)
2. Distribute the environment variables and instructions for generating cloud credentials to your users. Read more about how to [manage configuration here](/en/docs/claude-code/settings).
3. Users can [install Claude Code](/en/docs/claude-code/setup#installation)

## Access control and permissions

We support fine-grained permissions so that you're able to specify exactly what the agent is allowed to do (e.g. run tests, run linter) and what it is not allowed to do (e.g. update cloud infrastructure). These permission settings can be checked into version control and distributed to all developers in your organization, as well as customized by individual developers.

### Permission system

Claude Code uses a tiered permission system to balance power and safety:

| Tool Type         | Example              | Approval Required | "Yes, don't ask again" Behavior               |
| :---------------- | :------------------- | :---------------- | :-------------------------------------------- |
| Read-only         | File reads, LS, Grep | No                | N/A                                           |
| Bash Commands     | Shell execution      | Yes               | Permanently per project directory and command |
| File Modification | Edit/write files     | Yes               | Until session end                             |

### Configuring permissions

You can view & manage Claude Code's tool permissions with `/permissions`. This UI lists all permission rules and the settings.json file they are sourced from.

* **Allow** rules will allow Claude Code to use the specified tool without further manual approval.
* **Deny** rules will prevent Claude Code from using the specified tool. Deny rules take precedence over allow rules.
* **Additional directories** extend Claude's file access to directories beyond the initial working directory.
* **Default mode** controls Claude's permission behavior when encountering new requests.

Permission rules use the format: `Tool(optional-specifier)`

A rule that is just the tool name matches any use of that tool. For example, adding `Bash` to the list of allow rules would allow Claude Code to use the Bash tool without requiring user approval.

#### Permission modes

Claude Code supports several permission modes that can be set as the `defaultMode` in [settings files](/en/docs/claude-code/settings#settings-files):

| Mode                | Description                                                                  |
| :------------------ | :--------------------------------------------------------------------------- |
| `default`           | Standard behavior - prompts for permission on first use of each tool         |
| `acceptEdits`       | Automatically accepts file edit permissions for the session                  |
| `plan`              | Plan mode - Claude can analyze but not modify files or execute commands      |
| `bypassPermissions` | Skips all permission prompts (requires safe environment - see warning below) |

#### Working directories

By default, Claude has access to files in the directory where it was launched. You can extend this access:

* **During startup**: Use `--add-dir <path>` CLI argument
* **During session**: Use `/add-dir` slash command
* **Persistent configuration**: Add to `additionalDirectories` in [settings files](/en/docs/claude-code/settings#settings-files)

Files in additional directories follow the same permission rules as the original working directory - they become readable without prompts, and file editing permissions follow the current permission mode.

#### Tool-specific permission rules

Some tools use the optional specifier for more fine-grained permission controls. For example, an allow rule with `Bash(git diff:*)` would allow Bash commands that start with `git diff`. The following tools support permission rules with specifiers:

**Bash**

* `Bash(npm run build)` Matches the exact Bash command `npm run build`
* `Bash(npm run test:*)` Matches Bash commands starting with `npm run test`.

<Tip>
  Claude Code is aware of shell operators (like `&&`) so a prefix match rule like `Bash(safe-cmd:*)` won't give it permission to run the command `safe-cmd && other-cmd`
</Tip>

**Read & Edit**

`Edit` rules apply to all built-in tools that edit files. Claude will make a best-effort attempt to apply `Read` rules to all built-in tools that read files like Grep, Glob, and LS.

Read & Edit rules both follow the [gitignore](https://git-scm.com/docs/gitignore) specification. Patterns are resolved relative to the directory containing `.claude/settings.json`. To reference an absolute path, use `//`. For a path relative to your home directory, use `~/`.

* `Edit(docs/**)` Matches edits to files in the `docs` directory of your project
* `Read(~/.zshrc)` Matches reads to your `~/.zshrc` file
* `Edit(//tmp/scratch.txt)` Matches edits to `/tmp/scratch.txt`

**WebFetch**

* `WebFetch(domain:example.com)` Matches fetch requests to example.com

**MCP**

* `mcp__puppeteer` Matches any tool provided by the `puppeteer` server (name configured in Claude Code)
* `mcp__puppeteer__puppeteer_navigate` Matches the `puppeteer_navigate` tool provided by the `puppeteer` server

### Enterprise managed policy settings

For enterprise deployments of Claude Code, we support enterprise managed policy settings that take precedence over user and project settings. This allows system administrators to enforce security policies that users cannot override.

System administrators can deploy policies to:

* macOS: `/Library/Application Support/ClaudeCode/managed-settings.json`
* Linux and WSL: `/etc/claude-code/managed-settings.json`
* Windows: `C:\ProgramData\ClaudeCode\managed-settings.json`

These policy files follow the same format as regular [settings files](/en/docs/claude-code/settings#settings-files) but cannot be overridden by user or project settings. This ensures consistent security policies across your organization.

### Settings precedence

When multiple settings sources exist, they are applied in the following order (highest to lowest precedence):

1. Enterprise policies
2. Command line arguments
3. Local project settings (`.claude/settings.local.json`)
4. Shared project settings (`.claude/settings.json`)
5. User settings (`~/.claude/settings.json`)

This hierarchy ensures that organizational policies are always enforced while still allowing flexibility at the project and user levels where appropriate.

### Additional permission control with hooks

[Claude Code hooks](/en/docs/claude-code/hooks-guide) provide a way to register custom shell commands to perform permission evaluation at runtime. When Claude Code makes a tool call, PreToolUse hooks run before the permission system runs, and the hook output can determine whether to approve or deny the tool call in place of the permission system.

## Credential management

Claude Code supports authentication via Claude.ai credentials, Anthropic API credentials, Bedrock Auth, and Vertex Auth. On macOS, the API keys, OAuth tokens, and other credentials are stored on encrypted macOS Keychain. Alternately, the setting [apiKeyHelper](/en/docs/claude-code/settings#available-settings) can be set to a shell script which returns an API key. By default, this helper is called after 5 minutes or on HTTP 401 response; specifying environment variable `CLAUDE_CODE_API_KEY_HELPER_TTL_MS` defines a custom refresh interval.


---
---

> [!NOTE]
> # Security

> Learn about Claude Code's security safeguards and best practices for safe usage.

## How we approach security

### Security foundation

Your code's security is paramount. Claude Code is built with security at its core, developed according to Anthropic's comprehensive security program. Learn more and access resources (SOC 2 Type 2 report, ISO 27001 certificate, etc.) at [Anthropic Trust Center](https://trust.anthropic.com).

### Permission-based architecture

Claude Code uses strict read-only permissions by default. When additional actions are needed (editing files, running tests, executing commands), Claude Code requests explicit permission. Users control whether to approve actions once or allow them automatically.

We designed Claude Code to be transparent and secure. For example, we require approval for `git` commands before executing them, giving you direct control. This approach enables users and organizations to configure permissions directly.

For detailed permission configuration, see [Identity and Access Management](/en/docs/claude-code/iam).

### Built-in protections

To mitigate risks in agentic systems:

* **Folder access restriction**: Claude Code can only access the folder where it was started and its subfolders—it cannot go upstream to parent directories. This creates a clear security boundary, ensuring Claude Code only operates within the intended project scope
* **Prompt fatigue mitigation**: Support for allowlisting frequently used safe commands per-user, per-codebase, or per-organization
* **Accept Edits mode**: Batch accept multiple edits while maintaining permission prompts for commands with side effects

### User responsibility

Claude Code only has the permissions you grant it. You're responsible for reviewing proposed code and commands for safety before approval.

## Protect against prompt injection

Prompt injection is a technique where an attacker attempts to override or manipulate an AI assistant's instructions by inserting malicious text. Claude Code includes several safeguards against these attacks:

### Core protections

* **Permission system**: Sensitive operations require explicit approval
* **Context-aware analysis**: Detects potentially harmful instructions by analyzing the full request
* **Input sanitization**: Prevents command injection by processing user inputs
* **Command blocklist**: Blocks risky commands that fetch arbitrary content from the web like `curl` and `wget`

### Additional safeguards

* **Network request approval**: Tools that make network requests require user approval by default
* **Isolated context windows**: Web fetch uses a separate context window to avoid injecting potentially malicious prompts
* **Trust verification**: First-time codebase runs and new MCP servers require trust verification
* **Command injection detection**: Suspicious bash commands require manual approval even if previously allowlisted
* **Fail-closed matching**: Unmatched commands default to requiring manual approval
* **Natural language descriptions**: Complex bash commands include explanations for user understanding

**Best practices for working with untrusted content**:

1. Review suggested commands before approval
2. Avoid piping untrusted content directly to Claude
3. Verify proposed changes to critical files
4. Use virtual machines (VMs) to run scripts and make tool calls, especially when interacting with external web services
5. Report suspicious behavior with `/bug`

<Warning>
  While these protections significantly reduce risk, no system is completely
  immune to all attacks. Always maintain good security practices when working
  with any AI tool.
</Warning>

## MCP security

Claude Code allows users to configure Model Context Protocol (MCP) servers. The list of allowed MCP servers is configured in your source code, as part of Claude Code settings engineers check into source control.

We encourage either writing your own MCP servers or using MCP servers from providers that you trust. You are able to configure Claude Code permissions for MCP servers. Anthropic does not manage or audit any MCP servers.

## Security best practices

### Working with sensitive code

* Review all suggested changes before approval
* Use project-specific permission settings for sensitive repositories
* Consider using [devcontainers](/en/docs/claude-code/devcontainer) for additional isolation
* Regularly audit your permission settings with `/permissions`

### Team security

* Use [enterprise managed policies](/en/docs/claude-code/iam#enterprise-managed-policy-settings) to enforce organizational standards
* Share approved permission configurations through version control
* Train team members on security best practices
* Monitor Claude Code usage through [OpenTelemetry metrics](/en/docs/claude-code/monitoring-usage)

### Reporting security issues

If you discover a security vulnerability in Claude Code:

1. Do not disclose it publicly
2. Report it through our [HackerOne program](https://hackerone.com/anthropic-vdp/reports/new?type=team\&report_type=vulnerability)
3. Include detailed reproduction steps
4. Allow time for us to address the issue before public disclosure

## Related resources

* [Identity and Access Management](/en/docs/claude-code/iam) - Configure permissions and access controls
* [Monitoring usage](/en/docs/claude-code/monitoring-usage) - Track and audit Claude Code activity
* [Development containers](/en/docs/claude-code/devcontainer) - Secure, isolated environments
* [Anthropic Trust Center](https://trust.anthropic.com) - Security certifications and compliance


---
---

> [!NOTE]
> # Monitoring

> Learn how to enable and configure OpenTelemetry for Claude Code.

Claude Code supports OpenTelemetry (OTel) metrics and events for monitoring and observability.

All metrics are time series data exported via OpenTelemetry's standard metrics protocol, and events are exported via OpenTelemetry's logs/events protocol. It is the user's responsibility to ensure their metrics and logs backends are properly configured and that the aggregation granularity meets their monitoring requirements.

<Note>
  OpenTelemetry support is currently in beta and details are subject to change.
</Note>

## Quick Start

Configure OpenTelemetry using environment variables:

```bash
# 1. Enable telemetry
export CLAUDE_CODE_ENABLE_TELEMETRY=1

# 2. Choose exporters (both are optional - configure only what you need)
export OTEL_METRICS_EXPORTER=otlp       # Options: otlp, prometheus, console
export OTEL_LOGS_EXPORTER=otlp          # Options: otlp, console

# 3. Configure OTLP endpoint (for OTLP exporter)
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# 4. Set authentication (if required)
export OTEL_EXPORTER_OTLP_HEADERS="Authorization=Bearer your-token"

# 5. For debugging: reduce export intervals
export OTEL_METRIC_EXPORT_INTERVAL=10000  # 10 seconds (default: 60000ms)
export OTEL_LOGS_EXPORT_INTERVAL=5000     # 5 seconds (default: 5000ms)

# 6. Run Claude Code
claude
```

<Note>
  The default export intervals are 60 seconds for metrics and 5 seconds for logs. During setup, you may want to use shorter intervals for debugging purposes. Remember to reset these for production use.
</Note>

For full configuration options, see the [OpenTelemetry specification](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/protocol/exporter.md#configuration-options).

## Administrator Configuration

Administrators can configure OpenTelemetry settings for all users through the managed settings file. This allows for centralized control of telemetry settings across an organization. See the [settings precedence](/en/docs/claude-code/settings#settings-precedence) for more information about how settings are applied.

The managed settings file is located at:

* macOS: `/Library/Application Support/ClaudeCode/managed-settings.json`
* Linux and WSL: `/etc/claude-code/managed-settings.json`
* Windows: `C:\ProgramData\ClaudeCode\managed-settings.json`

Example managed settings configuration:

```json
{
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp",
    "OTEL_LOGS_EXPORTER": "otlp",
    "OTEL_EXPORTER_OTLP_PROTOCOL": "grpc",
    "OTEL_EXPORTER_OTLP_ENDPOINT": "http://collector.company.com:4317",
    "OTEL_EXPORTER_OTLP_HEADERS": "Authorization=Bearer company-token"
  }
}
```

<Note>
  Managed settings can be distributed via MDM (Mobile Device Management) or other device management solutions. Environment variables defined in the managed settings file have high precedence and cannot be overridden by users.
</Note>

## Configuration Details

### Common Configuration Variables

| Environment Variable                            | Description                                               | Example Values                       |
| ----------------------------------------------- | --------------------------------------------------------- | ------------------------------------ |
| `CLAUDE_CODE_ENABLE_TELEMETRY`                  | Enables telemetry collection (required)                   | `1`                                  |
| `OTEL_METRICS_EXPORTER`                         | Metrics exporter type(s) (comma-separated)                | `console`, `otlp`, `prometheus`      |
| `OTEL_LOGS_EXPORTER`                            | Logs/events exporter type(s) (comma-separated)            | `console`, `otlp`                    |
| `OTEL_EXPORTER_OTLP_PROTOCOL`                   | Protocol for OTLP exporter (all signals)                  | `grpc`, `http/json`, `http/protobuf` |
| `OTEL_EXPORTER_OTLP_ENDPOINT`                   | OTLP collector endpoint (all signals)                     | `http://localhost:4317`              |
| `OTEL_EXPORTER_OTLP_METRICS_PROTOCOL`           | Protocol for metrics (overrides general)                  | `grpc`, `http/json`, `http/protobuf` |
| `OTEL_EXPORTER_OTLP_METRICS_ENDPOINT`           | OTLP metrics endpoint (overrides general)                 | `http://localhost:4318/v1/metrics`   |
| `OTEL_EXPORTER_OTLP_LOGS_PROTOCOL`              | Protocol for logs (overrides general)                     | `grpc`, `http/json`, `http/protobuf` |
| `OTEL_EXPORTER_OTLP_LOGS_ENDPOINT`              | OTLP logs endpoint (overrides general)                    | `http://localhost:4318/v1/logs`      |
| `OTEL_EXPORTER_OTLP_HEADERS`                    | Authentication headers for OTLP                           | `Authorization=Bearer token`         |
| `OTEL_EXPORTER_OTLP_METRICS_CLIENT_KEY`         | Client key for mTLS authentication                        | Path to client key file              |
| `OTEL_EXPORTER_OTLP_METRICS_CLIENT_CERTIFICATE` | Client certificate for mTLS authentication                | Path to client cert file             |
| `OTEL_METRIC_EXPORT_INTERVAL`                   | Export interval in milliseconds (default: 60000)          | `5000`, `60000`                      |
| `OTEL_LOGS_EXPORT_INTERVAL`                     | Logs export interval in milliseconds (default: 5000)      | `1000`, `10000`                      |
| `OTEL_LOG_USER_PROMPTS`                         | Enable logging of user prompt content (default: disabled) | `1` to enable                        |

### Metrics Cardinality Control

The following environment variables control which attributes are included in metrics to manage cardinality:

| Environment Variable                | Description                                     | Default Value | Example to Disable |
| ----------------------------------- | ----------------------------------------------- | ------------- | ------------------ |
| `OTEL_METRICS_INCLUDE_SESSION_ID`   | Include session.id attribute in metrics         | `true`        | `false`            |
| `OTEL_METRICS_INCLUDE_VERSION`      | Include app.version attribute in metrics        | `false`       | `true`             |
| `OTEL_METRICS_INCLUDE_ACCOUNT_UUID` | Include user.account\_uuid attribute in metrics | `true`        | `false`            |

These variables help control the cardinality of metrics, which affects storage requirements and query performance in your metrics backend. Lower cardinality generally means better performance and lower storage costs but less granular data for analysis.

### Dynamic Headers

For enterprise environments that require dynamic authentication, you can configure a script to generate headers dynamically:

#### Settings Configuration

Add to your `.claude/settings.json`:

```json
{
  "otelHeadersHelper": "/bin/generate_opentelemetry_headers.sh"
}
```

#### Script Requirements

The script must output valid JSON with string key-value pairs representing HTTP headers:

```bash
#!/bin/bash
# Example: Multiple headers
echo "{\"Authorization\": \"Bearer $(get-token.sh)\", \"X-API-Key\": \"$(get-api-key.sh)\"}"
```

#### Important Limitations

**Headers are fetched only at startup, not during runtime.** This is due to OpenTelemetry exporter architecture limitations.

For scenarios requiring frequent token refresh, use an OpenTelemetry Collector as a proxy that can refresh its own headers.

### Multi-Team Organization Support

Organizations with multiple teams or departments can add custom attributes to distinguish between different groups using the `OTEL_RESOURCE_ATTRIBUTES` environment variable:

```bash
# Add custom attributes for team identification
export OTEL_RESOURCE_ATTRIBUTES="department=engineering,team.id=platform,cost_center=eng-123"
```

These custom attributes will be included in all metrics and events, allowing you to:

* Filter metrics by team or department
* Track costs per cost center
* Create team-specific dashboards
* Set up alerts for specific teams

### Example Configurations

```bash
# Console debugging (1-second intervals)
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=console
export OTEL_METRIC_EXPORT_INTERVAL=1000

# OTLP/gRPC
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# Prometheus
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=prometheus

# Multiple exporters
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=console,otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=http/json

# Different endpoints/backends for metrics and logs
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=otlp
export OTEL_LOGS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_METRICS_PROTOCOL=http/protobuf
export OTEL_EXPORTER_OTLP_METRICS_ENDPOINT=http://metrics.company.com:4318
export OTEL_EXPORTER_OTLP_LOGS_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_LOGS_ENDPOINT=http://logs.company.com:4317

# Metrics only (no events/logs)
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# Events/logs only (no metrics)
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_LOGS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
```

## Available Metrics and Events

### Standard Attributes

All metrics and events share these standard attributes:

| Attribute           | Description                                                   | Controlled By                                       |
| ------------------- | ------------------------------------------------------------- | --------------------------------------------------- |
| `session.id`        | Unique session identifier                                     | `OTEL_METRICS_INCLUDE_SESSION_ID` (default: true)   |
| `app.version`       | Current Claude Code version                                   | `OTEL_METRICS_INCLUDE_VERSION` (default: false)     |
| `organization.id`   | Organization UUID (when authenticated)                        | Always included when available                      |
| `user.account_uuid` | Account UUID (when authenticated)                             | `OTEL_METRICS_INCLUDE_ACCOUNT_UUID` (default: true) |
| `terminal.type`     | Terminal type (e.g., `iTerm.app`, `vscode`, `cursor`, `tmux`) | Always included when detected                       |

### Metrics

Claude Code exports the following metrics:

| Metric Name                           | Description                                     | Unit   |
| ------------------------------------- | ----------------------------------------------- | ------ |
| `claude_code.session.count`           | Count of CLI sessions started                   | count  |
| `claude_code.lines_of_code.count`     | Count of lines of code modified                 | count  |
| `claude_code.pull_request.count`      | Number of pull requests created                 | count  |
| `claude_code.commit.count`            | Number of git commits created                   | count  |
| `claude_code.cost.usage`              | Cost of the Claude Code session                 | USD    |
| `claude_code.token.usage`             | Number of tokens used                           | tokens |
| `claude_code.code_edit_tool.decision` | Count of code editing tool permission decisions | count  |
| `claude_code.active_time.total`       | Total active time in seconds                    | s      |

### Metric Details

#### Session Counter

Incremented at the start of each session.

**Attributes**:

* All [standard attributes](#standard-attributes)

#### Lines of Code Counter

Incremented when code is added or removed.

**Attributes**:

* All [standard attributes](#standard-attributes)
* `type`: (`"added"`, `"removed"`)

#### Pull Request Counter

Incremented when creating pull requests via Claude Code.

**Attributes**:

* All [standard attributes](#standard-attributes)

#### Commit Counter

Incremented when creating git commits via Claude Code.

**Attributes**:

* All [standard attributes](#standard-attributes)

#### Cost Counter

Incremented after each API request.

**Attributes**:

* All [standard attributes](#standard-attributes)
* `model`: Model identifier (e.g., "claude-3-5-sonnet-20241022")

#### Token Counter

Incremented after each API request.

**Attributes**:

* All [standard attributes](#standard-attributes)
* `type`: (`"input"`, `"output"`, `"cacheRead"`, `"cacheCreation"`)
* `model`: Model identifier (e.g., "claude-3-5-sonnet-20241022")

#### Code Edit Tool Decision Counter

Incremented when user accepts or rejects Edit, MultiEdit, Write, or NotebookEdit tool usage.

**Attributes**:

* All [standard attributes](#standard-attributes)
* `tool`: Tool name (`"Edit"`, `"MultiEdit"`, `"Write"`, `"NotebookEdit"`)
* `decision`: User decision (`"accept"`, `"reject"`)
* `language`: Programming language of the edited file (e.g., `"TypeScript"`, `"Python"`, `"JavaScript"`, `"Markdown"`). Returns `"unknown"` for unrecognized file extensions.

#### Active Time Counter

Tracks actual time spent actively using Claude Code (not idle time). This metric is incremented during user interactions such as typing prompts or receiving responses.

**Attributes**:

* All [standard attributes](#standard-attributes)

### Events

Claude Code exports the following events via OpenTelemetry logs/events (when `OTEL_LOGS_EXPORTER` is configured):

#### User Prompt Event

Logged when a user submits a prompt.

**Event Name**: `claude_code.user_prompt`

**Attributes**:

* All [standard attributes](#standard-attributes)
* `event.name`: `"user_prompt"`
* `event.timestamp`: ISO 8601 timestamp
* `prompt_length`: Length of the prompt
* `prompt`: Prompt content (redacted by default, enable with `OTEL_LOG_USER_PROMPTS=1`)

#### Tool Result Event

Logged when a tool completes execution.

**Event Name**: `claude_code.tool_result`

**Attributes**:

* All [standard attributes](#standard-attributes)
* `event.name`: `"tool_result"`
* `event.timestamp`: ISO 8601 timestamp
* `tool_name`: Name of the tool
* `success`: `"true"` or `"false"`
* `duration_ms`: Execution time in milliseconds
* `error`: Error message (if failed)
* `decision`: Either `"accept"` or `"reject"`
* `source`: Decision source - `"config"`, `"user_permanent"`, `"user_temporary"`, `"user_abort"`, or `"user_reject"`
* `tool_parameters`: JSON string containing tool-specific parameters (when available)
  * For Bash tool: includes `bash_command`, `full_command`, `timeout`, `description`, `sandbox`

#### API Request Event

Logged for each API request to Claude.

**Event Name**: `claude_code.api_request`

**Attributes**:

* All [standard attributes](#standard-attributes)
* `event.name`: `"api_request"`
* `event.timestamp`: ISO 8601 timestamp
* `model`: Model used (e.g., "claude-3-5-sonnet-20241022")
* `cost_usd`: Estimated cost in USD
* `duration_ms`: Request duration in milliseconds
* `input_tokens`: Number of input tokens
* `output_tokens`: Number of output tokens
* `cache_read_tokens`: Number of tokens read from cache
* `cache_creation_tokens`: Number of tokens used for cache creation

#### API Error Event

Logged when an API request to Claude fails.

**Event Name**: `claude_code.api_error`

**Attributes**:

* All [standard attributes](#standard-attributes)
* `event.name`: `"api_error"`
* `event.timestamp`: ISO 8601 timestamp
* `model`: Model used (e.g., "claude-3-5-sonnet-20241022")
* `error`: Error message
* `status_code`: HTTP status code (if applicable)
* `duration_ms`: Request duration in milliseconds
* `attempt`: Attempt number (for retried requests)

#### Tool Decision Event

Logged when a tool permission decision is made (accept/reject).

**Event Name**: `claude_code.tool_decision`

**Attributes**:

* All [standard attributes](#standard-attributes)
* `event.name`: `"tool_decision"`
* `event.timestamp`: ISO 8601 timestamp
* `tool_name`: Name of the tool (e.g., "Read", "Edit", "MultiEdit", "Write", "NotebookEdit", etc.)
* `decision`: Either `"accept"` or `"reject"`
* `source`: Decision source - `"config"`, `"user_permanent"`, `"user_temporary"`, `"user_abort"`, or `"user_reject"`

## Interpreting Metrics and Events Data

The metrics exported by Claude Code provide valuable insights into usage patterns and productivity. Here are some common visualizations and analyses you can create:

### Usage Monitoring

| Metric                                                        | Analysis Opportunity                                      |
| ------------------------------------------------------------- | --------------------------------------------------------- |
| `claude_code.token.usage`                                     | Break down by `type` (input/output), user, team, or model |
| `claude_code.session.count`                                   | Track adoption and engagement over time                   |
| `claude_code.lines_of_code.count`                             | Measure productivity by tracking code additions/removals  |
| `claude_code.commit.count` & `claude_code.pull_request.count` | Understand impact on development workflows                |

### Kostenüberwachung

Die Metrik `claude_code.cost.usage` hilft bei:

* Verfolgung von Nutzungstrends über Teams oder Einzelpersonen hinweg
* Identifizierung von Sitzungen mit hoher Nutzung zur Optimierung

<Hinweis>
  Kostenmetriken sind Näherungswerte. Offizielle Abrechnungsdaten finden Sie bei Ihrem API-Anbieter (Anthropic Console, AWS Bedrock oder Google Cloud Vertex).
</Hinweis>

### Alerting und Segmentierung

Zu berücksichtigende allgemeine Warnmeldungen:

* Kostenspitzen
* Ungewöhnlicher Token-Verbrauch
* Hohes Sitzungsvolumen von bestimmten Nutzern

Alle Metriken können nach `user.account_uuid`, `organization.id`, `session.id`, `model` und `app.version` segmentiert werden.

### Ereignisanalyse

Die Ereignisdaten bieten detaillierte Einblicke in die Interaktionen von Claude Code:

**Tool-Nutzungsmuster**: Analysieren Sie Tool-Ergebnis-Ereignisse, um sie zu identifizieren:

* Die am häufigsten verwendeten Werkzeuge
* Erfolgsraten von Werkzeugen
* Durchschnittliche Ausführungszeiten von Werkzeugen
* Fehlermuster nach Werkzeugtyp

**Leistungsüberwachung**: Verfolgen Sie die Dauer von API-Anfragen und Tool-Ausführungszeiten, um Leistungsengpässe zu ermitteln.

## Überlegungen zum Backend

Die Wahl der Backends für Metriken und Protokolle bestimmt die Arten von Analysen, die Sie durchführen können:

### Für Metriken:

* **Zeitreihen-Datenbanken (z. B. Prometheus)**: Ratenberechnungen, aggregierte Metriken
* **Kolumnenspeicher (z. B. ClickHouse)**: Komplexe Abfragen, einzigartige Benutzeranalyse
* **Voll funktionsfähige Beobachtungsplattformen (z. B. Honeycomb, Datadog)**: Erweiterte Abfragen, Visualisierung, Warnmeldungen

### Für Ereignisse/Protokolle:

* **Log-Aggregationssysteme (z. B. Elasticsearch, Loki)**: Volltextsuche, Log-Analyse
* **Kolumnenspeicher (z. B. ClickHouse)**: Strukturierte Ereignisanalyse
* **Voll funktionsfähige Beobachtungsplattformen (z. B. Honeycomb, Datadog)**: Korrelation zwischen Metriken und Ereignissen

Unternehmen, die täglich/wöchentlich/monatlich aktive Nutzer (DAU/WAU/MAU) benötigen, sollten Backends in Betracht ziehen, die effiziente Abfragen von Einzelwerten unterstützen.

## Dienstinformationen

Alle Metriken und Ereignisse werden mit den folgenden Ressourcenattributen exportiert:

* dienst.name": "claude-code"
* service.version`: Aktuelle Claude-Code-Version
* `os.type`: Typ des Betriebssystems (z.B. `Linux`, `Darwin`, `Windows`)
* `os.version`: Versionsstring des Betriebssystems
* host.arch`: Architektur des Hosts (z. B. `amd64`, `arm64`)
* `wsl.version`: WSL-Versionsnummer (nur vorhanden, wenn unter Windows Subsystem für Linux ausgeführt)
* Meter Name: `com.anthropic.claude_code`

## Überlegungen zur Sicherheit/Privatsphäre

* Telemetrie ist opt-in und erfordert eine explizite Konfiguration
* Sensible Informationen wie API-Schlüssel oder Dateiinhalte werden niemals in Metriken oder Ereignisse aufgenommen
* Der Inhalt der Benutzereingabeaufforderung wird standardmäßig unkenntlich gemacht - nur die Länge der Eingabeaufforderung wird aufgezeichnet. Um die Aufzeichnung von Benutzerprompts zu aktivieren, setzen Sie `OTEL_LOG_USER_PROMPTS=1`


---
---

> [!NOTE]
> # Manage costs effectively

> Learn how to track and optimize token usage and costs when using Claude Code.

Claude Code consumes tokens for each interaction. The average cost is \$6 per developer per day, with daily costs remaining below \$12 for 90% of users.

For team usage, Claude Code charges by API token consumption. On average, Claude Code costs \~\$50-60/developer per month with Sonnet 4 though there is large variance depending on how many instances users are running and whether they're using it in automation.

## Track your costs

* Use `/cost` to see current session usage
* **Anthropic Console users**:
  * Check [historical usage](https://support.anthropic.com/en/articles/9534590-cost-and-usage-reporting-in-console) in the Anthropic Console (requires Admin or Billing role)
  * Set [workspace spend limits](https://support.anthropic.com/en/articles/9796807-creating-and-managing-workspaces) for the Claude Code workspace (requires Admin role)
* **Pro and Max plan users**: Usage is included in your subscription

## Managing costs for teams

When using Anthropic API, you can limit the total Claude Code workspace spend. To configure, [follow these instructions](https://support.anthropic.com/en/articles/9796807-creating-and-managing-workspaces). Admins can view cost and usage reporting by [following these instructions](https://support.anthropic.com/en/articles/9534590-cost-and-usage-reporting-in-console).

On Bedrock and Vertex, Claude Code does not send metrics from your cloud. In order to get cost metrics, several large enterprises reported using [LiteLLM](/en/docs/claude-code/bedrock-vertex-proxies#litellm), which is an open-source tool that helps companies [track spend by key](https://docs.litellm.ai/docs/proxy/virtual_keys#tracking-spend). This project is unaffiliated with Anthropic and we have not audited its security.

## Reduce token usage

* **Compact conversations:**

  * Claude uses auto-compact by default when context exceeds 95% capacity
  * Toggle auto-compact: Run `/config` and navigate to "Auto-compact enabled"
  * Use `/compact` manually when context gets large
  * Add custom instructions: `/compact Focus on code samples and API usage`
  * Customize compaction by adding to CLAUDE.md:

    ```markdown
    # Summary instructions

    When you are using compact, please focus on test output and code changes
    ```

* **Write specific queries:** Avoid vague requests that trigger unnecessary scanning

* **Break down complex tasks:** Split large tasks into focused interactions

* **Clear history between tasks:** Use `/clear` to reset context

Costs can vary significantly based on:

* Size of codebase being analyzed
* Complexity of queries
* Number of files being searched or modified
* Length of conversation history
* Frequency of compacting conversations
* Background processes (haiku generation, conversation summarization)

## Background token usage

Claude Code uses tokens for some background functionality even when idle:

* **Haiku generation**: Small creative messages that appear while you type (approximately 1 cent per day)
* **Conversation summarization**: Background jobs that summarize previous conversations for the `claude --resume` feature
* **Command processing**: Some commands like `/cost` may generate requests to check status

These background processes consume a small amount of tokens (typically under \$0.04 per session) even without active interaction.

<Note>
  For team deployments, we recommend starting with a small pilot group to
  establish usage patterns before wider rollout.
</Note>

---
---


> [!NOTE]
> # Analytics

> View detailed usage insights and productivity metrics for your organization's Claude Code deployment.

Claude Code provides an analytics dashboard that helps organizations understand developer usage patterns, track productivity metrics, and optimize their Claude Code adoption.

<Note>
  Analytics are currently available only for organizations using Claude Code with the Anthropic API through the Anthropic Console.
</Note>

## Access analytics

Navigate to the analytics dashboard at [console.anthropic.com/claude\_code](https://console.anthropic.com/claude_code).

### Required roles

* **Primary Owner**
* **Owner**
* **Billing**
* **Admin**
* **Developer**

<Note>
  Users with **User**, **Claude Code User** or **Membership Admin** roles cannot access analytics.
</Note>

## Available metrics

### Lines of code accepted

Total lines of code written by Claude Code that users have accepted in their sessions.

* Excludes rejected code suggestions
* Doesn't track subsequent deletions

### Suggestion accept rate

Percentage of times users accept code editing tool usage, including:

* Edit
* MultiEdit
* Write
* NotebookEdit

### Activity

**users**: Number of active users in a given day (number on left Y-axis)

**sessions**: Number of active sessions in a given day (number on right Y-axis)

### Spend

**users**: Number of active users in a given day (number on left Y-axis)

**spend**: Total dollars spent in a given day (number on right Y-axis)

### Team insights

**Members**: All users who have authenticated to Claude Code

* API key users are displayed by **API key identifier**
* OAuth users are displayed by **email address**

**Avg daily spend:** Per-user average spend for the current month. For example, on July 10, this reflects the average daily spend over 10 days.

**Avg lines/day:** Per-user average of accepted code lines for the current month.

## Using analytics effectively

### Monitor adoption

Track team member status to identify:

* Active users who can share best practices
* Overall adoption trends across your organization

### Measure productivity

Tool acceptance rates and code metrics help you:

* Understand developer satisfaction with Claude Code suggestions
* Track code generation effectiveness
* Identify opportunities for training or process improvements

## Related resources

* [Monitoring usage with OpenTelemetry](/en/docs/claude-code/monitoring-usage) for custom metrics and alerting
* [Identity and access management](/en/docs/claude-code/iam) for role configuration

---
---

> [!NOTE]
> # Claude Code settings

> Configure Claude Code with global and project-level settings, and environment variables.

Claude Code offers a variety of settings to configure its behavior to meet your needs. You can configure Claude Code by running the `/config` command when using the interactive REPL.

## Settings files

The `settings.json` file is our official mechanism for configuring Claude
Code through hierarchical settings:

* **User settings** are defined in `~/.claude/settings.json` and apply to all
  projects.
* **Project settings** are saved in your project directory:
  * `.claude/settings.json` for settings that are checked into source control and shared with your team
  * `.claude/settings.local.json` for settings that are not checked in, useful for personal preferences and experimentation. Claude Code will configure git to ignore `.claude/settings.local.json` when it is created.
* For enterprise deployments of Claude Code, we also support **enterprise
  managed policy settings**. These take precedence over user and project
  settings. System administrators can deploy policies to:
  * macOS: `/Library/Application Support/ClaudeCode/managed-settings.json`
  * Linux and WSL: `/etc/claude-code/managed-settings.json`
  * Windows: `C:\ProgramData\ClaudeCode\managed-settings.json`

```JSON Example settings.json
{
  "permissions": {
    "allow": [
      "Bash(npm run lint)",
      "Bash(npm run test:*)",
      "Read(~/.zshrc)"
    ],
    "deny": [
      "Bash(curl:*)"
    ]
  },
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp"
  }
}
```

### Available settings

`settings.json` supports a number of options:

| Key                          | Description                                                                                                                                                                                                    | Example                                                 |
| :--------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------ |
| `apiKeyHelper`               | Custom script, to be executed in `/bin/sh`, to generate an auth value. This value will generally be sent as `X-Api-Key`, `Authorization: Bearer`, and `Proxy-Authorization: Bearer` headers for model requests | `/bin/generate_temp_api_key.sh`                         |
| `cleanupPeriodDays`          | How long to locally retain chat transcripts (default: 30 days)                                                                                                                                                 | `20`                                                    |
| `env`                        | Environment variables that will be applied to every session                                                                                                                                                    | `{"FOO": "bar"}`                                        |
| `includeCoAuthoredBy`        | Whether to include the `co-authored-by Claude` byline in git commits and pull requests (default: `true`)                                                                                                       | `false`                                                 |
| `permissions`                | See table below for structure of permissions.                                                                                                                                                                  |                                                         |
| `hooks`                      | Configure custom commands to run before or after tool executions. See [hooks documentation](hooks)                                                                                                             | `{"PreToolUse": {"Bash": "echo 'Running command...'"}}` |
| `model`                      | Override the default model to use for Claude Code                                                                                                                                                              | `"claude-3-5-sonnet-20241022"`                          |
| `forceLoginMethod`           | Use `claudeai` to restrict login to Claude.ai accounts, `console` to restrict login to Anthropic Console (API usage billing) accounts                                                                          | `claudeai`                                              |
| `enableAllProjectMcpServers` | Automatically approve all MCP servers defined in project `.mcp.json` files                                                                                                                                     | `true`                                                  |
| `enabledMcpjsonServers`      | List of specific MCP servers from `.mcp.json` files to approve                                                                                                                                                 | `["memory", "github"]`                                  |
| `disabledMcpjsonServers`     | List of specific MCP servers from `.mcp.json` files to reject                                                                                                                                                  | `["filesystem"]`                                        |

### Permission settings

| Keys                           | Description                                                                                                                                        | Example                          |
| :----------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------- |
| `allow`                        | Array of [permission rules](/en/docs/claude-code/iam#configuring-permissions) to allow tool use                                                    | `[ "Bash(git diff:*)" ]`         |
| `deny`                         | Array of [permission rules](/en/docs/claude-code/iam#configuring-permissions) to deny tool use                                                     | `[ "WebFetch", "Bash(curl:*)" ]` |
| `additionalDirectories`        | Additional [working directories](iam#working-directories) that Claude has access to                                                                | `[ "../docs/" ]`                 |
| `defaultMode`                  | Default [permission mode](iam#permission-modes) when opening Claude Code                                                                           | `"acceptEdits"`                  |
| `disableBypassPermissionsMode` | Set to `"disable"` to prevent `bypassPermissions` mode from being activated. See [managed policy settings](iam#enterprise-managed-policy-settings) | `"disable"`                      |

### Settings precedence

Settings are applied in order of precedence:

1. Enterprise policies (see [IAM documentation](/en/docs/claude-code/iam#enterprise-managed-policy-settings))
2. Command line arguments
3. Local project settings
4. Shared project settings
5. User settings

## Environment variables

Claude Code supports the following environment variables to control its behavior:

<Note>
  All environment variables can also be configured in [`settings.json`](#available-settings). This is useful as a way to automatically set environment variables for each session, or to roll out a set of environment variables for your whole team or organization.
</Note>

| Variable                                   | Purpose                                                                                                                                                            |
| :----------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ANTHROPIC_API_KEY`                        | API key sent as `X-Api-Key` header, typically for the Claude SDK (for interactive usage, run `/login`)                                                             |
| `ANTHROPIC_AUTH_TOKEN`                     | Custom value for the `Authorization` and `Proxy-Authorization` headers (the value you set here will be prefixed with `Bearer `)                                    |
| `ANTHROPIC_CUSTOM_HEADERS`                 | Custom headers you want to add to the request (in `Name: Value` format)                                                                                            |
| `ANTHROPIC_MODEL`                          | Name of custom model to use (see [Model Configuration](/en/docs/claude-code/bedrock-vertex-proxies#model-configuration))                                           |
| `ANTHROPIC_SMALL_FAST_MODEL`               | Name of [Haiku-class model for background tasks](/en/docs/claude-code/costs)                                                                                       |
| `ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION`    | Override AWS region for the small/fast model when using Bedrock                                                                                                    |
| `AWS_BEARER_TOKEN_BEDROCK`                 | Bedrock API key for authentication (see [Bedrock API keys](https://aws.amazon.com/blogs/machine-learning/accelerate-ai-development-with-amazon-bedrock-api-keys/)) |
| `BASH_DEFAULT_TIMEOUT_MS`                  | Default timeout for long-running bash commands                                                                                                                     |
| `BASH_MAX_TIMEOUT_MS`                      | Maximum timeout the model can set for long-running bash commands                                                                                                   |
| `BASH_MAX_OUTPUT_LENGTH`                   | Maximum number of characters in bash outputs before they are middle-truncated                                                                                      |
| `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR` | Return to the original working directory after each Bash command                                                                                                   |
| `CLAUDE_CODE_API_KEY_HELPER_TTL_MS`        | Interval in milliseconds at which credentials should be refreshed (when using `apiKeyHelper`)                                                                      |
| `CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL`        | Skip auto-installation of IDE extensions                                                                                                                           |
| `CLAUDE_CODE_MAX_OUTPUT_TOKENS`            | Set the maximum number of output tokens for most requests                                                                                                          |
| `CLAUDE_CODE_USE_BEDROCK`                  | Use [Bedrock](/en/docs/claude-code/amazon-bedrock)                                                                                                                 |
| `CLAUDE_CODE_USE_VERTEX`                   | Use [Vertex](/en/docs/claude-code/google-vertex-ai)                                                                                                                |
| `CLAUDE_CODE_SKIP_BEDROCK_AUTH`            | Skip AWS authentication for Bedrock (e.g. when using an LLM gateway)                                                                                               |
| `CLAUDE_CODE_SKIP_VERTEX_AUTH`             | Skip Google authentication for Vertex (e.g. when using an LLM gateway)                                                                                             |
| `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` | Equivalent of setting `DISABLE_AUTOUPDATER`, `DISABLE_BUG_COMMAND`, `DISABLE_ERROR_REPORTING`, and `DISABLE_TELEMETRY`                                             |
| `CLAUDE_CODE_DISABLE_TERMINAL_TITLE`       | Set to `1` to disable automatic terminal title updates based on conversation context                                                                               |
| `DISABLE_AUTOUPDATER`                      | Set to `1` to disable automatic updates. This takes precedence over the `autoUpdates` configuration setting.                                                       |
| `DISABLE_BUG_COMMAND`                      | Set to `1` to disable the `/bug` command                                                                                                                           |
| `DISABLE_COST_WARNINGS`                    | Set to `1` to disable cost warning messages                                                                                                                        |
| `DISABLE_ERROR_REPORTING`                  | Set to `1` to opt out of Sentry error reporting                                                                                                                    |
| `DISABLE_NON_ESSENTIAL_MODEL_CALLS`        | Set to `1` to disable model calls for non-critical paths like flavor text                                                                                          |
| `DISABLE_TELEMETRY`                        | Set to `1` to opt out of Statsig telemetry (note that Statsig events do not include user data like code, file paths, or bash commands)                             |
| `HTTP_PROXY`                               | Specify HTTP proxy server for network connections                                                                                                                  |
| `HTTPS_PROXY`                              | Specify HTTPS proxy server for network connections                                                                                                                 |
| `MAX_THINKING_TOKENS`                      | Force a thinking for the model budget                                                                                                                              |
| `MCP_TIMEOUT`                              | Timeout in milliseconds for MCP server startup                                                                                                                     |
| `MCP_TOOL_TIMEOUT`                         | Timeout in milliseconds for MCP tool execution                                                                                                                     |
| `MAX_MCP_OUTPUT_TOKENS`                    | Maximum number of tokens allowed in MCP tool responses (default: 25000)                                                                                            |
| `VERTEX_REGION_CLAUDE_3_5_HAIKU`           | Override region for Claude 3.5 Haiku when using Vertex AI                                                                                                          |
| `VERTEX_REGION_CLAUDE_3_5_SONNET`          | Override region for Claude 3.5 Sonnet when using Vertex AI                                                                                                         |
| `VERTEX_REGION_CLAUDE_3_7_SONNET`          | Override region for Claude 3.7 Sonnet when using Vertex AI                                                                                                         |
| `VERTEX_REGION_CLAUDE_4_0_OPUS`            | Override region for Claude 4.0 Opus when using Vertex AI                                                                                                           |
| `VERTEX_REGION_CLAUDE_4_0_SONNET`          | Override region for Claude 4.0 Sonnet when using Vertex AI                                                                                                         |

## Configuration options

To manage your configurations, use the following commands:

* List settings: `claude config list`
* See a setting: `claude config get <key>`
* Change a setting: `claude config set <key> <value>`
* Push to a setting (for lists): `claude config add <key> <value>`
* Remove from a setting (for lists): `claude config remove <key> <value>`

By default `config` changes your project configuration. To manage your global configuration, use the `--global` (or `-g`) flag.

### Global configuration

To set a global configuration, use `claude config set -g <key> <value>`:

| Key                     | Description                                                                                                                                                                                        | Example                                                                    |
| :---------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------- |
| `autoUpdates`           | Whether to enable automatic updates (default: `true`). When enabled, Claude Code automatically downloads and installs updates in the background. Updates are applied when you restart Claude Code. | `false`                                                                    |
| `preferredNotifChannel` | Where you want to receive notifications (default: `iterm2`)                                                                                                                                        | `iterm2`, `iterm2_with_bell`, `terminal_bell`, or `notifications_disabled` |
| `theme`                 | Color theme                                                                                                                                                                                        | `dark`, `light`, `light-daltonized`, or `dark-daltonized`                  |
| `verbose`               | Whether to show full bash and command outputs (default: `false`)                                                                                                                                   | `true`                                                                     |

## Tools available to Claude

Claude Code has access to a set of powerful tools that help it understand and modify your codebase:

| Tool             | Description                                          | Permission Required |
| :--------------- | :--------------------------------------------------- | :------------------ |
| **Bash**         | Executes shell commands in your environment          | Yes                 |
| **Edit**         | Makes targeted edits to specific files               | Yes                 |
| **Glob**         | Finds files based on pattern matching                | No                  |
| **Grep**         | Searches for patterns in file contents               | No                  |
| **LS**           | Lists files and directories                          | No                  |
| **MultiEdit**    | Performs multiple edits on a single file atomically  | Yes                 |
| **NotebookEdit** | Modifies Jupyter notebook cells                      | Yes                 |
| **NotebookRead** | Reads and displays Jupyter notebook contents         | No                  |
| **Read**         | Reads the contents of files                          | No                  |
| **Task**         | Runs a sub-agent to handle complex, multi-step tasks | No                  |
| **TodoWrite**    | Creates and manages structured task lists            | No                  |
| **WebFetch**     | Fetches content from a specified URL                 | Yes                 |
| **WebSearch**    | Performs web searches with domain filtering          | Yes                 |
| **Write**        | Creates or overwrites files                          | Yes                 |

Permission rules can be configured using `/allowed-tools` or in [permission settings](/en/docs/claude-code/settings#available-settings).

### Extending tools with hooks

You can run custom commands before or after any tool executes using
[Claude Code hooks](/en/docs/claude-code/hooks-guide).

For example, you could automatically run a Python formatter after Claude
modifies Python files, or prevent modifications to production configuration
files by blocking Write operations to certain paths.

## See also

* [Identity and Access Management](/en/docs/claude-code/iam#configuring-permissions) - Learn about Claude Code's permission system
* [IAM and access control](/en/docs/claude-code/iam#enterprise-managed-policy-settings) - Enterprise policy management
* [Troubleshooting](/en/docs/claude-code/troubleshooting#auto-updater-issues) - Solutions for common configuration issues


---
---

> [!NOTE]
> # Add Claude Code to your IDE

> Learn how to add Claude Code to your favorite IDE

Claude Code works great with any Integrated Development Environment (IDE) that has a terminal. Just run `claude`, and you're ready to go.

In addition, Claude Code provides dedicated integrations for popular IDEs, which provide features like interactive diff viewing, selection context sharing, and more. These integrations currently exist for:

* **Visual Studio Code** (including popular forks like Cursor, Windsurf, and VSCodium)
* **JetBrains IDEs** (including IntelliJ, PyCharm, Android Studio, WebStorm, PhpStorm and GoLand)

## Features

* **Quick launch**: Use `Cmd+Esc` (Mac) or `Ctrl+Esc` (Windows/Linux) to open
  Claude Code directly from your editor, or click the Claude Code button in the
  UI
* **Diff viewing**: Code changes can be displayed directly in the IDE diff
  viewer instead of the terminal. You can configure this in `/config`
* **Selection context**: The current selection/tab in the IDE is automatically
  shared with Claude Code
* **File reference shortcuts**: Use `Cmd+Option+K` (Mac) or `Alt+Ctrl+K`
  (Linux/Windows) to insert file references (e.g., @File#L1-99)
* **Diagnostic sharing**: Diagnostic errors (lint, syntax, etc.) from the IDE
  are automatically shared with Claude as you work

## Installation

<Tabs>
  <Tab title="VS Code+">
    To install Claude Code on VS Code and popular forks like Cursor, Windsurf, and VSCodium:

    1. Open VS Code
    2. Open the integrated terminal
    3. Run `claude` - the extension will auto-install
  </Tab>

  <Tab title="JetBrains">
    To install Claude Code on JetBrains IDEs like IntelliJ, PyCharm, Android Studio, WebStorm, PhpStorm and GoLand, find and install the [Claude Code plugin](https://docs.anthropic.com/s/claude-code-jetbrains) from the marketplace and restart your IDE.

    <Note>
      The plugin may also be auto-installed when you run `claude` in the integrated terminal. The IDE must be restarted completely to take effect.
    </Note>

    <Warning>
      **Remote Development Limitations**: When using JetBrains Remote Development, you must install the plugin in the remote host via `Settings > Plugin (Host)`.
    </Warning>
  </Tab>
</Tabs>

## Usage

### From your IDE

Run `claude` from your IDE's integrated terminal, and all features will be active.

### From external terminals

Use the `/ide` command in any external terminal to connect Claude Code to your IDE and activate all features.

If you want Claude to have access to the same files as your IDE, start Claude Code from the same directory as your IDE project root.

## Configuration

IDE integrations work with Claude Code's configuration system:

1. Run `claude`
2. Enter the `/config` command
3. Adjust your preferences. Setting the diff tool to `auto` will enable automatic IDE detection

## Troubleshooting

### VS Code extension not installing

* Ensure you're running Claude Code from VS Code's integrated terminal
* Ensure that the CLI corresponding to your IDE is installed:
  * For VS Code: `code` command should be available
  * For Cursor: `cursor` command should be available
  * For Windsurf: `windsurf` command should be available
  * For VSCodium: `codium` command should be available
  * If not installed, use `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
    and search for "Shell Command: Install 'code' command in PATH" (or the
    equivalent for your IDE)
* Check that VS Code has permission to install extensions

### JetBrains plugin not working

* Ensure you're running Claude Code from the project root directory
* Check that the JetBrains plugin is enabled in the IDE settings
* Completely restart the IDE. You may need to do this multiple times
* For JetBrains Remote Development, ensure that the Claude Code plugin is
  installed in the remote host and not locally on the client

For additional help, refer to our
[troubleshooting guide](/en/docs/claude-code/troubleshooting).

---
---

> [!NOTE]
> # Optimize your terminal setup

> Claude Code works best when your terminal is properly configured. Follow these guidelines to optimize your experience.

### Themes and appearance

Claude cannot control the theme of your terminal. That's handled by your terminal application. You can match Claude Code's theme to your terminal any time via the `/config` command.

### Line breaks

You have several options for entering linebreaks into Claude Code:

* **Quick escape**: Type `\` followed by Enter to create a newline
* **Keyboard shortcut**: Set up a keybinding to insert a newline

#### Set up Shift+Enter (VS Code or iTerm2):

Run `/terminal-setup` within Claude Code to automatically configure Shift+Enter.

#### Set up Option+Enter (VS Code, iTerm2 or macOS Terminal.app):

**For Mac Terminal.app:**

1. Open Settings → Profiles → Keyboard
2. Check "Use Option as Meta Key"

**For iTerm2 and VS Code terminal:**

1. Open Settings → Profiles → Keys
2. Under General, set Left/Right Option key to "Esc+"

### Notification setup

Never miss when Claude completes a task with proper notification configuration:

#### Terminal bell notifications

Enable sound alerts when tasks complete:

```sh
claude config set --global preferredNotifChannel terminal_bell
```

**For macOS users**: Don't forget to enable notification permissions in System Settings → Notifications → \[Your Terminal App].

#### iTerm 2 system notifications

For iTerm 2 alerts when tasks complete:

1. Open iTerm 2 Preferences
2. Navigate to Profiles → Terminal
3. Enable "Silence bell" and Filter Alerts → "Send escape sequence-generated alerts"
4. Set your preferred notification delay

Note that these notifications are specific to iTerm 2 and not available in the default macOS Terminal.

#### Custom notification hooks

For advanced notification handling, you can create [notification hooks](/en/docs/claude-code/hooks#notification) to run your own logic.

### Handling large inputs

When working with extensive code or long instructions:

* **Avoid direct pasting**: Claude Code may struggle with very long pasted content
* **Use file-based workflows**: Write content to a file and ask Claude to read it
* **Be aware of VS Code limitations**: The VS Code terminal is particularly prone to truncating long pastes

### Vim Mode

Claude Code supports a subset of Vim keybindings that can be enabled with `/vim` or configured via `/config`.

The supported subset includes:

* Mode switching: `Esc` (to NORMAL), `i`/`I`, `a`/`A`, `o`/`O` (to INSERT)
* Navigation: `h`/`j`/`k`/`l`, `w`/`e`/`b`, `0`/`$`/`^`, `gg`/`G`
* Editing: `x`, `dw`/`de`/`db`/`dd`/`D`, `cw`/`ce`/`cb`/`cc`/`C`, `.` (repeat)

---
---

> [!NOTE]
> # Manage Claude's memory

> Learn how to manage Claude Code's memory across sessions with different memory locations and best practices.

Claude Code can remember your preferences across sessions, like style guidelines and common commands in your workflow.

## Determine memory type

Claude Code offers three memory locations, each serving a different purpose:

| Memory Type                | Location              | Purpose                                  | Use Case Examples                                                |
| -------------------------- | --------------------- | ---------------------------------------- | ---------------------------------------------------------------- |
| **Project memory**         | `./CLAUDE.md`         | Team-shared instructions for the project | Project architecture, coding standards, common workflows         |
| **User memory**            | `~/.claude/CLAUDE.md` | Personal preferences for all projects    | Code styling preferences, personal tooling shortcuts             |
| **Project memory (local)** | `./CLAUDE.local.md`   | Personal project-specific preferences    | *(Deprecated, see below)* Your sandbox URLs, preferred test data |

All memory files are automatically loaded into Claude Code's context when launched.

## CLAUDE.md imports

CLAUDE.md files can import additional files using `@path/to/import` syntax. The following example imports 3 files:

```
See @README for project overview and @package.json for available npm commands for this project.

# Additional Instructions
- git workflow @docs/git-instructions.md
```

Both relative and absolute paths are allowed. In particular, importing files in user's home dir is a convenient way for your team members to provide individual instructions that are not checked into the repository. Previously CLAUDE.local.md served a similar purpose, but is now deprecated in favor of imports since they work better across multiple git worktrees.

```
# Individual Preferences
- @~/.claude/my-project-instructions.md
```

To avoid potential collisions, imports are not evaluated inside markdown code spans and code blocks.

```
This code span will not be treated as an import: `@anthropic-ai/claude-code`
```

Imported files can recursively import additional files, with a max-depth of 5 hops. You can see what memory files are loaded by running `/memory` command.

## How Claude looks up memories

Claude Code reads memories recursively: starting in the cwd, Claude Code recurses up to (but not including) the root directory */* and reads any CLAUDE.md or CLAUDE.local.md files it finds. This is especially convenient when working in large repositories where you run Claude Code in *foo/bar/*, and have memories in both *foo/CLAUDE.md* and *foo/bar/CLAUDE.md*.

Claude will also discover CLAUDE.md nested in subtrees under your current working directory. Instead of loading them at launch, they are only included when Claude reads files in those subtrees.

## Quickly add memories with the `#` shortcut

The fastest way to add a memory is to start your input with the `#` character:

```
# Always use descriptive variable names
```

You'll be prompted to select which memory file to store this in.

## Directly edit memories with `/memory`

Use the `/memory` slash command during a session to open any memory file in your system editor for more extensive additions or organization.

## Set up project memory

Suppose you want to set up a CLAUDE.md file to store important project information, conventions, and frequently used commands.

Bootstrap a CLAUDE.md for your codebase with the following command:

```
> /init 
```

<Tip>
  Tips:

  * Include frequently used commands (build, test, lint) to avoid repeated searches
  * Document code style preferences and naming conventions
  * Add important architectural patterns specific to your project
  * CLAUDE.md memories can be used for both instructions shared with your team and for your individual preferences.
</Tip>

## Memory best practices

* **Be specific**: "Use 2-space indentation" is better than "Format code properly".
* **Use structure to organize**: Format each individual memory as a bullet point and group related memories under descriptive markdown headings.
* **Review periodically**: Update memories as your project evolves to ensure Claude is always using the most up to date information and context.


---
---

> [!NOTE]
> # CLI reference

> Complete reference for Claude Code command-line interface, including commands and flags.

## CLI commands

| Command                            | Description                                    | Example                                                            |
| :--------------------------------- | :--------------------------------------------- | :----------------------------------------------------------------- |
| `claude`                           | Start interactive REPL                         | `claude`                                                           |
| `claude "query"`                   | Start REPL with initial prompt                 | `claude "explain this project"`                                    |
| `claude -p "query"`                | Query via SDK, then exit                       | `claude -p "explain this function"`                                |
| `cat file \| claude -p "query"`    | Process piped content                          | `cat logs.txt \| claude -p "explain"`                              |
| `claude -c`                        | Continue most recent conversation              | `claude -c`                                                        |
| `claude -c -p "query"`             | Continue via SDK                               | `claude -c -p "Check for type errors"`                             |
| `claude -r "<session-id>" "query"` | Resume session by ID                           | `claude -r "abc123" "Finish this PR"`                              |
| `claude update`                    | Update to latest version                       | `claude update`                                                    |
| `claude mcp`                       | Configure Model Context Protocol (MCP) servers | See the [Claude Code MCP documentation](/en/docs/claude-code/mcp). |

## CLI flags

Customize Claude Code's behavior with these command-line flags:

| Flag                             | Description                                                                                                                                              | Example                                                     |
| :------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------- |
| `--add-dir`                      | Add additional working directories for Claude to access (validates each path exists as a directory)                                                      | `claude --add-dir ../apps ../lib`                           |
| `--allowedTools`                 | A list of tools that should be allowed without prompting the user for permission, in addition to [settings.json files](/en/docs/claude-code/settings)    | `"Bash(git log:*)" "Bash(git diff:*)" "Read"`               |
| `--disallowedTools`              | A list of tools that should be disallowed without prompting the user for permission, in addition to [settings.json files](/en/docs/claude-code/settings) | `"Bash(git log:*)" "Bash(git diff:*)" "Edit"`               |
| `--print`, `-p`                  | Print response without interactive mode (see [SDK documentation](/en/docs/claude-code/sdk) for programmatic usage details)                               | `claude -p "query"`                                         |
| `--output-format`                | Specify output format for print mode (options: `text`, `json`, `stream-json`)                                                                            | `claude -p "query" --output-format json`                    |
| `--input-format`                 | Specify input format for print mode (options: `text`, `stream-json`)                                                                                     | `claude -p --output-format json --input-format stream-json` |
| `--verbose`                      | Enable verbose logging, shows full turn-by-turn output (helpful for debugging in both print and interactive modes)                                       | `claude --verbose`                                          |
| `--max-turns`                    | Limit the number of agentic turns in non-interactive mode                                                                                                | `claude -p --max-turns 3 "query"`                           |
| `--model`                        | Sets the model for the current session with an alias for the latest model (`sonnet` or `opus`) or a model's full name                                    | `claude --model claude-sonnet-4-20250514`                   |
| `--permission-mode`              | Begin in a specified [permission mode](iam#permission-modes)                                                                                             | `claude --permission-mode plan`                             |
| `--permission-prompt-tool`       | Specify an MCP tool to handle permission prompts in non-interactive mode                                                                                 | `claude -p --permission-prompt-tool mcp_auth_tool "query"`  |
| `--resume`                       | Resume a specific session by ID, or by choosing in interactive mode                                                                                      | `claude --resume abc123 "query"`                            |
| `--continue`                     | Load the most recent conversation in the current directory                                                                                               | `claude --continue`                                         |
| `--dangerously-skip-permissions` | Skip permission prompts (use with caution)                                                                                                               | `claude --dangerously-skip-permissions`                     |

<Tip>
  The `--output-format json` flag is particularly useful for scripting and
  automation, allowing you to parse Claude's responses programmatically.
</Tip>

For detailed information about print mode (`-p`) including output formats,
streaming, verbose logging, and programmatic usage, see the
[SDK documentation](/en/docs/claude-code/sdk).

## See also

* [Interactive mode](/en/docs/claude-code/interactive-mode) - Shortcuts, input modes, and interactive features
* [Slash commands](/en/docs/claude-code/slash-commands) - Interactive session commands
* [Quickstart guide](/en/docs/claude-code/quickstart) - Getting started with Claude Code
* [Common workflows](/en/docs/claude-code/common-workflows) - Advanced workflows and patterns
* [Settings](/en/docs/claude-code/settings) - Configuration options
* [SDK documentation](/en/docs/claude-code/sdk) - Programmatic usage and integrations


---
---

> [!NOTE]
> # Interactive mode

> Complete reference for keyboard shortcuts, input modes, and interactive features in Claude Code sessions.

## Keyboard shortcuts

### General controls

| Shortcut         | Description                        | Context                    |
| :--------------- | :--------------------------------- | :------------------------- |
| `Ctrl+C`         | Cancel current input or generation | Standard interrupt         |
| `Ctrl+D`         | Exit Claude Code session           | EOF signal                 |
| `Ctrl+L`         | Clear terminal screen              | Keeps conversation history |
| `Up/Down arrows` | Navigate command history           | Recall previous inputs     |
| `Esc` + `Esc`    | Edit previous message              | Double-escape to modify    |

### Multiline input

| Method         | Shortcut       | Context                 |
| :------------- | :------------- | :---------------------- |
| Quick escape   | `\` + `Enter`  | Works in all terminals  |
| macOS default  | `Option+Enter` | Default on macOS        |
| Terminal setup | `Shift+Enter`  | After `/terminal-setup` |
| Paste mode     | Paste directly | For code blocks, logs   |

### Quick commands

| Shortcut     | Description                        | Notes                                                     |
| :----------- | :--------------------------------- | :-------------------------------------------------------- |
| `#` at start | Memory shortcut - add to CLAUDE.md | Prompts for file selection                                |
| `/` at start | Slash command                      | See [slash commands](/en/docs/claude-code/slash-commands) |

## Vim mode

Enable vim-style editing with `/vim` command or configure permanently via `/config`.

### Mode switching

| Command | Action                      | From mode |
| :------ | :-------------------------- | :-------- |
| `Esc`   | Enter NORMAL mode           | INSERT    |
| `i`     | Insert before cursor        | NORMAL    |
| `I`     | Insert at beginning of line | NORMAL    |
| `a`     | Insert after cursor         | NORMAL    |
| `A`     | Insert at end of line       | NORMAL    |
| `o`     | Open line below             | NORMAL    |
| `O`     | Open line above             | NORMAL    |

### Navigation (NORMAL mode)

| Command         | Action                    |
| :-------------- | :------------------------ |
| `h`/`j`/`k`/`l` | Move left/down/up/right   |
| `w`             | Next word                 |
| `e`             | End of word               |
| `b`             | Previous word             |
| `0`             | Beginning of line         |
| `$`             | End of line               |
| `^`             | First non-blank character |
| `gg`            | Beginning of input        |
| `G`             | End of input              |

### Editing (NORMAL mode)

| Command        | Action                  |
| :------------- | :---------------------- |
| `x`            | Delete character        |
| `dd`           | Delete line             |
| `D`            | Delete to end of line   |
| `dw`/`de`/`db` | Delete word/to end/back |
| `cc`           | Change line             |
| `C`            | Change to end of line   |
| `cw`/`ce`/`cb` | Change word/to end/back |
| `.`            | Repeat last change      |

<Tip>
  Configure your preferred line break behavior in terminal settings. Run `/terminal-setup` to install Shift+Enter binding for iTerm2 and VS Code terminals.
</Tip>

## Command history

Claude Code maintains command history for the current session:

* History is stored per working directory
* Cleared with `/clear` command
* Use Up/Down arrows to navigate (see keyboard shortcuts above)
* **Ctrl+R**: Reverse search through history (if supported by terminal)
* **Note**: History expansion (`!`) is disabled by default

## See also

* [Slash commands](/en/docs/claude-code/slash-commands) - Interactive session commands
* [CLI reference](/en/docs/claude-code/cli-reference) - Command-line flags and options
* [Settings](/en/docs/claude-code/settings) - Configuration options
* [Memory management](/en/docs/claude-code/memory) - Managing CLAUDE.md files

---
---

> [!NOTE]
> # Slash commands

> Control Claude's behavior during an interactive session with slash commands.

## Built-in slash commands

| Command                   | Purpose                                                                        |
| :------------------------ | :----------------------------------------------------------------------------- |
| `/add-dir`                | Add additional working directories                                             |
| `/bug`                    | Report bugs (sends conversation to Anthropic)                                  |
| `/clear`                  | Clear conversation history                                                     |
| `/compact [instructions]` | Compact conversation with optional focus instructions                          |
| `/config`                 | View/modify configuration                                                      |
| `/cost`                   | Show token usage statistics                                                    |
| `/doctor`                 | Checks the health of your Claude Code installation                             |
| `/help`                   | Get usage help                                                                 |
| `/init`                   | Initialize project with CLAUDE.md guide                                        |
| `/login`                  | Switch Anthropic accounts                                                      |
| `/logout`                 | Sign out from your Anthropic account                                           |
| `/mcp`                    | Manage MCP server connections and OAuth authentication                         |
| `/memory`                 | Edit CLAUDE.md memory files                                                    |
| `/model`                  | Select or change the AI model                                                  |
| `/permissions`            | View or update [permissions](/en/docs/claude-code/iam#configuring-permissions) |
| `/pr_comments`            | View pull request comments                                                     |
| `/review`                 | Request code review                                                            |
| `/status`                 | View account and system statuses                                               |
| `/terminal-setup`         | Install Shift+Enter key binding for newlines (iTerm2 and VSCode only)          |
| `/vim`                    | Enter vim mode for alternating insert and command modes                        |

## Custom slash commands

Custom slash commands allow you to define frequently-used prompts as Markdown files that Claude Code can execute. Commands are organized by scope (project-specific or personal) and support namespacing through directory structures.

### Syntax

```
/<command-name> [arguments]
```

#### Parameters

| Parameter        | Description                                                       |
| :--------------- | :---------------------------------------------------------------- |
| `<command-name>` | Name derived from the Markdown filename (without `.md` extension) |
| `[arguments]`    | Optional arguments passed to the command                          |

### Command types

#### Project commands

Commands stored in your repository and shared with your team. When listed in `/help`, these commands show "(project)" after their description.

**Location**: `.claude/commands/`

In the following example, we create the `/optimize` command:

```bash
# Create a project command
mkdir -p .claude/commands
echo "Analyze this code for performance issues and suggest optimizations:" > .claude/commands/optimize.md
```

#### Personal commands

Commands available across all your projects. When listed in `/help`, these commands show "(user)" after their description.

**Location**: `~/.claude/commands/`

In the following example, we create the `/security-review` command:

```bash
# Create a personal command
mkdir -p ~/.claude/commands
echo "Review this code for security vulnerabilities:" > ~/.claude/commands/security-review.md
```

### Features

#### Namespacing

Organize commands in subdirectories. The subdirectories determine the command's
full name. The description will show whether the command comes from the project
directory (`.claude/commands`) or the user-level directory (`~/.claude/commands`).

Conflicts between user and project level commands are not supported. Otherwise,
multiple commands with the same base file name can coexist.

For example, a file at `.claude/commands/frontend/component.md` creates the command `/frontend:component` with description showing "(project)".
Meanwhile, a file at `~/.claude/commands/component.md` creates the command `/component` with description showing "(user)".

#### Arguments

Pass dynamic values to commands using the `$ARGUMENTS` placeholder.

For example:

```bash
# Command definition
echo 'Fix issue #$ARGUMENTS following our coding standards' > .claude/commands/fix-issue.md

# Usage
> /fix-issue 123
```

#### Bash command execution

Execute bash commands before the slash command runs using the `!` prefix. The output is included in the command context. You *must* include `allowed-tools` with the `Bash` tool, but you can choose the specific bash commands to allow.

For example:

```markdown
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
description: Create a git commit
---

## Context

- Current git status: !`git status`
- Current git diff (staged and unstaged changes): !`git diff HEAD`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`

## Your task

Based on the above changes, create a single git commit.
```

#### File references

Include file contents in commands using the `@` prefix to [reference files](/en/docs/claude-code/common-workflows#reference-files-and-directories).

For example:

```markdown
# Reference a specific file
Review the implementation in @src/utils/helpers.js

# Reference multiple files
Compare @src/old-version.js with @src/new-version.js
```

#### Thinking mode

Slash commands can trigger extended thinking by including [extended thinking keywords](/en/docs/claude-code/common-workflows#use-extended-thinking).

### File format

Command files support:

* **Markdown format** (`.md` extension)
* **YAML frontmatter** for metadata:
  * `allowed-tools`: List of tools the command can use
  * `description`: Brief description of the command
  * `argument-hint`: The arguments expected for the slash command. Example: `argument-hint: add [tagId] | remove [tagId] | list`. This hint is shown to the user when auto-completing the slash command.
* **Dynamic content** with bash commands (`!`) and file references (`@`)
* **Prompt instructions** as the main content

## MCP slash commands

MCP servers can expose prompts as slash commands that become available in Claude Code. These commands are dynamically discovered from connected MCP servers.

### Command format

MCP commands follow the pattern:

```
/mcp__<server-name>__<prompt-name> [arguments]
```

### Features

#### Dynamic discovery

MCP commands are automatically available when:

* An MCP server is connected and active
* The server exposes prompts through the MCP protocol
* The prompts are successfully retrieved during connection

#### Arguments

MCP prompts can accept arguments defined by the server:

```
# Without arguments
> /mcp__github__list_prs

# With arguments
> /mcp__github__pr_review 456
> /mcp__jira__create_issue "Bug title" high
```

#### Naming conventions

* Server and prompt names are normalized
* Spaces and special characters become underscores
* Names are lowercased for consistency

### Managing MCP connections

Use the `/mcp` command to:

* View all configured MCP servers
* Check connection status
* Authenticate with OAuth-enabled servers
* Clear authentication tokens
* View available tools and prompts from each server

## See also

* [Interactive mode](/en/docs/claude-code/interactive-mode) - Shortcuts, input modes, and interactive features
* [CLI reference](/en/docs/claude-code/cli-reference) - Command-line flags and options
* [Settings](/en/docs/claude-code/settings) - Configuration options
* [Memory management](/en/docs/claude-code/memory) - Managing Claude's memory across sessions

---
---

> [!NOTE]
> # Hooks reference

> This page provides reference documentation for implementing hooks in Claude Code.

<Tip>
  For a quickstart guide with examples, see [Get started with Claude Code hooks](/en/docs/claude-code/hooks-guide).
</Tip>

## Configuration

Claude Code hooks are configured in your
[settings files](/en/docs/claude-code/settings):

* `~/.claude/settings.json` - User settings
* `.claude/settings.json` - Project settings
* `.claude/settings.local.json` - Local project settings (not committed)
* Enterprise managed policy settings

### Structure

Hooks are organized by matchers, where each matcher can have multiple hooks:

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",
        "hooks": [
          {
            "type": "command",
            "command": "your-command-here"
          }
        ]
      }
    ]
  }
}
```

* **matcher**: Pattern to match tool names, case-sensitive (only applicable for
  `PreToolUse` and `PostToolUse`)
  * Simple strings match exactly: `Write` matches only the Write tool
  * Supports regex: `Edit|Write` or `Notebook.*`
  * If omitted or empty string, hooks run for all matching events
* **hooks**: Array of commands to execute when the pattern matches
  * `type`: Currently only `"command"` is supported
  * `command`: The bash command to execute
  * `timeout`: (Optional) How long a command should run, in seconds, before
    canceling that specific command.

For events like `UserPromptSubmit`, `Notification`, `Stop`, and `SubagentStop` that don't use matchers, you can omit the matcher field:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/prompt-validator.py"
          }
        ]
      }
    ]
  }
}
```

<Warning>
  `"matcher": "*"` is invalid. Instead, omit "matcher" or use `"matcher": ""`.
</Warning>

## Hook Events

### PreToolUse

Runs after Claude creates tool parameters and before processing the tool call.

**Common matchers:**

* `Task` - Agent tasks
* `Bash` - Shell commands
* `Glob` - File pattern matching
* `Grep` - Content search
* `Read` - File reading
* `Edit`, `MultiEdit` - File editing
* `Write` - File writing
* `WebFetch`, `WebSearch` - Web operations

### PostToolUse

Runs immediately after a tool completes successfully.

Recognizes the same matcher values as PreToolUse.

### Notification

Runs when Claude Code sends notifications. Notifications are sent when:

1. Claude needs your permission to use a tool. Example: "Claude needs your permission to use Bash"
2. The prompt input has been idle for at least 60 seconds. "Claude is waiting for your input"

### UserPromptSubmit

Runs when the user submits a prompt, before Claude processes it. This allows you to add additional context based on the prompt/conversation, validate prompts, or block certain types of prompts.

### Stop

Runs when the main Claude Code agent has finished responding. Does not run if the stoppage occurred due to a user interrupt.

### SubagentStop

Runs when a Claude Code subagent (Task tool call) has finished responding.

### PreCompact

Runs before Claude Code is about to run a compact operation.

**Matchers:**

* `manual` - Invoked from `/compact`
* `auto` - Invoked from auto-compact (due to full context window)

## Hook Input

Hooks receive JSON data via stdin containing session information and
event-specific data:

```typescript
{
  // Common fields
  session_id: string
  transcript_path: string  // Path to conversation JSON
  cwd: string              // The current working directory when the hook is invoked

  // Event-specific fields
  hook_event_name: string
  ...
}
```

### PreToolUse Input

The exact schema for `tool_input` depends on the tool.

```json
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "PreToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.txt",
    "content": "file content"
  }
}
```

### PostToolUse Input

The exact schema for `tool_input` and `tool_response` depends on the tool.

```json
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "PostToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.txt",
    "content": "file content"
  },
  "tool_response": {
    "filePath": "/path/to/file.txt",
    "success": true
  }
}
```

### Notification Input

```json
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "Notification",
  "message": "Task completed successfully"
}
```

### UserPromptSubmit Input

```json
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "UserPromptSubmit",
  "prompt": "Write a function to calculate the factorial of a number"
}
```

### Stop and SubagentStop Input

`stop_hook_active` is true when Claude Code is already continuing as a result of
a stop hook. Check this value or process the transcript to prevent Claude Code
from running indefinitely.

```json
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "hook_event_name": "Stop",
  "stop_hook_active": true
}
```

### PreCompact Input

For `manual`, `custom_instructions` comes from what the user passes into
`/compact`. For `auto`, `custom_instructions` is empty.

```json
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "hook_event_name": "PreCompact",
  "trigger": "manual",
  "custom_instructions": ""
}
```

## Hook Output

There are two ways for hooks to return output back to Claude Code. The output
communicates whether to block and any feedback that should be shown to Claude
and the user.

### Simple: Exit Code

Hooks communicate status through exit codes, stdout, and stderr:

* **Exit code 0**: Success. `stdout` is shown to the user in transcript mode
  (CTRL-R).
* **Exit code 2**: Blocking error. `stderr` is fed back to Claude to process
  automatically. See per-hook-event behavior below.
* **Other exit codes**: Non-blocking error. `stderr` is shown to the user and
  execution continues.

<Warning>
  Reminder: Claude Code does not see stdout if the exit code is 0.
</Warning>

#### Exit Code 2 Behavior

| Hook Event         | Behavior                                                           |
| ------------------ | ------------------------------------------------------------------ |
| `PreToolUse`       | Blocks the tool call, shows stderr to Claude                       |
| `PostToolUse`      | Shows stderr to Claude (tool already ran)                          |
| `Notification`     | N/A, shows stderr to user only                                     |
| `UserPromptSubmit` | Blocks prompt processing, erases prompt, shows stderr to user only |
| `Stop`             | Blocks stoppage, shows stderr to Claude                            |
| `SubagentStop`     | Blocks stoppage, shows stderr to Claude subagent                   |
| `PreCompact`       | N/A, shows stderr to user only                                     |

### Advanced: JSON Output

Hooks can return structured JSON in `stdout` for more sophisticated control:

#### Common JSON Fields

All hook types can include these optional fields:

```json
{
  "continue": true, // Whether Claude should continue after hook execution (default: true)
  "stopReason": "string" // Message shown when continue is false
  "suppressOutput": true, // Hide stdout from transcript mode (default: false)
}
```

If `continue` is false, Claude stops processing after the hooks run.

* For `PreToolUse`, this is different from `"decision": "block"`, which only
  blocks a specific tool call and provides automatic feedback to Claude.
* For `PostToolUse`, this is different from `"decision": "block"`, which
  provides automated feedback to Claude.
* For `UserPromptSubmit`, this prevents the prompt from being processed.
* For `Stop` and `SubagentStop`, this takes precedence over any
  `"decision": "block"` output.
* In all cases, `"continue" = false` takes precedence over any
  `"decision": "block"` output.

`stopReason` accompanies `continue` with a reason shown to the user, not shown
to Claude.

#### `PreToolUse` Decision Control

`PreToolUse` hooks can control whether a tool call proceeds.

* "approve" bypasses the permission system. `reason` is shown to the user but
  not to Claude.
* "block" prevents the tool call from executing. `reason` is shown to Claude.
* `undefined` leads to the existing permission flow. `reason` is ignored.

```json
{
  "decision": "approve" | "block" | undefined,
  "reason": "Explanation for decision"
}
```

#### `PostToolUse` Decision Control

`PostToolUse` hooks can control whether a tool call proceeds.

* "block" automatically prompts Claude with `reason`.
* `undefined` does nothing. `reason` is ignored.

```json
{
  "decision": "block" | undefined,
  "reason": "Explanation for decision"
}
```

#### `UserPromptSubmit` Decision Control

`UserPromptSubmit` hooks can control whether a user prompt is processed.

* `"block"` prevents the prompt from being processed. The submitted prompt is erased from context. `"reason"` is shown to the user but not added to context.
* `undefined` allows the prompt to proceed normally. `"reason"` is ignored.

```json
{
  "decision": "block" | undefined,
  "reason": "Explanation for decision"
}
```

#### `Stop`/`SubagentStop` Decision Control

`Stop` and `SubagentStop` hooks can control whether Claude must continue.

* "block" prevents Claude from stopping. You must populate `reason` for Claude
  to know how to proceed.
* `undefined` allows Claude to stop. `reason` is ignored.

```json
{
  "decision": "block" | undefined,
  "reason": "Must be provided when Claude is blocked from stopping"
}
```

#### JSON Output Example: Bash Command Editing

```python
#!/usr/bin/env python3
import json
import re
import sys

# Define validation rules as a list of (regex pattern, message) tuples
VALIDATION_RULES = [
    (
        r"\bgrep\b(?!.*\|)",
        "Use 'rg' (ripgrep) instead of 'grep' for better performance and features",
    ),
    (
        r"\bfind\s+\S+\s+-name\b",
        "Use 'rg --files | rg pattern' or 'rg --files -g pattern' instead of 'find -name' for better performance",
    ),
]


def validate_command(command: str) -> list[str]:
    issues = []
    for pattern, message in VALIDATION_RULES:
        if re.search(pattern, command):
            issues.append(message)
    return issues


try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
    sys.exit(1)

tool_name = input_data.get("tool_name", "")
tool_input = input_data.get("tool_input", {})
command = tool_input.get("command", "")

if tool_name != "Bash" or not command:
    sys.exit(1)

# Validate the command
issues = validate_command(command)

if issues:
    for message in issues:
        print(f"• {message}", file=sys.stderr)
    # Exit code 2 blocks tool call and shows stderr to Claude
    sys.exit(2)
```

#### UserPromptSubmit Example: Adding Context and Validation

```python
#!/usr/bin/env python3
import json
import sys
import re
import datetime

# Load input from stdin
try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
    sys.exit(1)

prompt = input_data.get("prompt", "")

# Check for sensitive patterns
sensitive_patterns = [
    (r"(?i)\b(password|secret|key|token)\s*[:=]", "Prompt contains potential secrets"),
]

for pattern, message in sensitive_patterns:
    if re.search(pattern, prompt):
        # Use JSON output to block with a specific reason
        output = {
            "decision": "block",
            "reason": f"Security policy violation: {message}. Please rephrase your request without sensitive information."
        }
        print(json.dumps(output))
        sys.exit(0)

# Add current time to context
context = f"Current time: {datetime.datetime.now()}"
print(context)

# Allow the prompt to proceed with the additional context
sys.exit(0)
```

## Working with MCP Tools

Claude Code hooks work seamlessly with
[Model Context Protocol (MCP) tools](/en/docs/claude-code/mcp). When MCP servers
provide tools, they appear with a special naming pattern that you can match in
your hooks.

### MCP Tool Naming

MCP tools follow the pattern `mcp__<server>__<tool>`, for example:

* `mcp__memory__create_entities` - Memory server's create entities tool
* `mcp__filesystem__read_file` - Filesystem server's read file tool
* `mcp__github__search_repositories` - GitHub server's search tool

### Configuring Hooks for MCP Tools

You can target specific MCP tools or entire MCP servers:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "mcp__memory__.*",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Memory operation initiated' >> ~/mcp-operations.log"
          }
        ]
      },
      {
        "matcher": "mcp__.*__write.*",
        "hooks": [
          {
            "type": "command",
            "command": "/home/user/scripts/validate-mcp-write.py"
          }
        ]
      }
    ]
  }
}
```

## Examples

<Tip>
  For practical examples including code formatting, notifications, and file protection, see [More Examples](/en/docs/claude-code/hooks-guide#more-examples) in the get started guide.
</Tip>

## Security Considerations

### Disclaimer

**USE AT YOUR OWN RISK**: Claude Code hooks execute arbitrary shell commands on
your system automatically. By using hooks, you acknowledge that:

* You are solely responsible for the commands you configure
* Hooks can modify, delete, or access any files your user account can access
* Malicious or poorly written hooks can cause data loss or system damage
* Anthropic provides no warranty and assumes no liability for any damages
  resulting from hook usage
* You should thoroughly test hooks in a safe environment before production use

Always review and understand any hook commands before adding them to your
configuration.

### Security Best Practices

Here are some key practices for writing more secure hooks:

1. **Validate and sanitize inputs** - Never trust input data blindly
2. **Always quote shell variables** - Use `"$VAR"` not `$VAR`
3. **Block path traversal** - Check for `..` in file paths
4. **Use absolute paths** - Specify full paths for scripts
5. **Skip sensitive files** - Avoid `.env`, `.git/`, keys, etc.

### Configuration Safety

Direct edits to hooks in settings files don't take effect immediately. Claude
Code:

1. Captures a snapshot of hooks at startup
2. Uses this snapshot throughout the session
3. Warns if hooks are modified externally
4. Requires review in `/hooks` menu for changes to apply

This prevents malicious hook modifications from affecting your current session.

## Hook Execution Details

* **Timeout**: 60-second execution limit by default, configurable per command.
  * A timeout for an individual command does not affect the other commands.
* **Parallelization**: All matching hooks run in parallel
* **Environment**: Runs in current directory with Claude Code's environment
* **Input**: JSON via stdin
* **Output**:
  * PreToolUse/PostToolUse/Stop: Progress shown in transcript (Ctrl-R)
  * Notification: Logged to debug only (`--debug`)

## Debugging

### Basic Troubleshooting

If your hooks aren't working:

1. **Check configuration** - Run `/hooks` to see if your hook is registered
2. **Verify syntax** - Ensure your JSON settings are valid
3. **Test commands** - Run hook commands manually first
4. **Check permissions** - Make sure scripts are executable
5. **Review logs** - Use `claude --debug` to see hook execution details

Common issues:

* **Quotes not escaped** - Use `\"` inside JSON strings
* **Wrong matcher** - Check tool names match exactly (case-sensitive)
* **Command not found** - Use full paths for scripts

### Advanced Debugging

For complex hook issues:

1. **Inspect hook execution** - Use `claude --debug` to see detailed hook execution
2. **Validate JSON schemas** - Test hook input/output with external tools
3. **Check environment variables** - Verify Claude Code's environment is correct
4. **Test edge cases** - Try hooks with unusual file paths or inputs
5. **Monitor system resources** - Check for resource exhaustion during hook execution
6. **Use structured logging** - Implement logging in your hook scripts

### Debug Output Example

Use `claude --debug` to see hook execution details:

```
[DEBUG] Executing hooks for PostToolUse:Write
[DEBUG] Getting matching hook commands for PostToolUse with query: Write
[DEBUG] Found 1 hook matchers in settings
[DEBUG] Matched 1 hooks for query "Write"
[DEBUG] Found 1 hook commands to execute
[DEBUG] Executing hook command: <Your command> with timeout 60000ms
[DEBUG] Hook command completed with status 0: <Your stdout>
```

Progress messages appear in transcript mode (Ctrl-R) showing:

* Which hook is running
* Command being executed
* Success/failure status
* Output or error messages

---
---
