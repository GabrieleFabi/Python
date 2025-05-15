# Altium BOM Formatter

Questo repository contiene uno script Python per convertire e formattare automaticamente un file CSV esportato da Altium in un formato standardizzato, pronto per l'importazione in altri strumenti o sistemi di gestione componenti.

## 📋 Funzionalità

- Rilevamento automatico dell’intestazione dati effettiva nel file CSV Altium.
- Mappatura e riformattazione dei campi secondo uno schema predefinito.
- Supporto per campi fissi (es. `supplier`, `tag`, `favourite`, ecc.).
- Gestione robusta di intestazioni con maiuscole/minuscole e spazi/virgolette.
- Output in formato `.csv` con delimitatore `;`, compatibile con Excel.

## 🗂️ Struttura dei file

```
.
├── Altium.csv                 # File CSV esportato da Altium
├── formatted_output.csv       # File CSV generato dallo script
├── format_bom.py              # Script Python per la formattazione
└── README.md                  # Questo file
```

## 🧰 Requisiti

- Python 3.6 o superiore

## ▶️ Utilizzo

1. Esporta la BOM da Altium come file `.csv` (usa `;` come separatore).
2. Salva il file nella cartella del progetto come `Altium.csv`.
3. Esegui lo script Python:

```bash
python format_bom.py
```

4. Il file `formatted_output.csv` verrà generato con i campi nel formato corretto.

## 📝 Mappatura dei campi

| Campo in Altium      | Campo nel file finale | Note                                |
|----------------------|------------------------|--------------------------------------|
| `MPN1`               | `name`, `mpn`          | Valore duplicato                     |
| `Description`        | `description`          |                                      |
| `Designator`         | `notes`                |                                      |
| `Quantity`           | `quantity`             |                                      |
| `MFG1`               | `manufacturer`         |                                      |
| *(fisso)*            | `supplier`             | Sempre impostato a `"Mouser"`        |
| *(fisso)*            | `tag`                  | Impostato su `"Inverte Logica"`      |
| *(fisso)*            | `favourite`            | `"0"`                                |
| *(fisso)*            | `needs_review`         | `"0"`                                |
| *(nessuna corrispondenza)* | Altri campi     | Lasciati vuoti                       |

## 🛠 Personalizzazione

Puoi modificare lo script per:
- Cambiare il valore del campo `tag`
- Aggiungere o unire righe con lo stesso `mpn`
- Modificare i valori fissi (`supplier`, `favourite`, ecc.)
