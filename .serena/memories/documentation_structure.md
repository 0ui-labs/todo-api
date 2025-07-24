# Dokumentationsstruktur

## Hauptdokumentation
- **CLAUDE.md**: Projektspezifische Anleitung (automatisch gelesen)
  - Quick Start, Commands, Architecture
  - Max. 200 Zeilen für schnelle Referenz

## Detaillierte Guides in docs/
- **docs/PYTHON-GUIDE.md**: Python-Standards, Testing, Best Practices
- **docs/PRP-FRAMEWORK.md**: PRP-Methodologie, Validation Gates

## Verwendung:
1. CLAUDE.md wird automatisch gelesen
2. Explizit auf Guides verweisen bei Bedarf:
   - "Befolge Python-Standards aus docs/PYTHON-GUIDE.md"
   - "Erstelle PRP nach docs/PRP-FRAMEWORK.md"
3. Guides bei spezifischen Aufgaben konsultieren

## Hook-System (NEU):
Der "Task Processing Hook" in CLAUDE.md instruiert Claude automatisch:
- Bei Code-Keywords (implement, test, api, etc.) → Python-Guide nutzen
- Bei PRP-Keywords (plan, feature, requirement) → PRP-Framework nutzen  
- Bei Slash-Commands (/prp-base-create, etc.) → PRP-Framework nutzen
- Keine manuelle Erwähnung der Guides mehr nötig!