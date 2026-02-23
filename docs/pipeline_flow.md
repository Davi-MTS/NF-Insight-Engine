# Pipeline Flow — FISCALIS

## Sequential Execution Model

Step 1:
QR Code → Extract URL → Store Access Key

Step 2:
URL → Selenium Scraping → Structured Data Extraction → Database

Step 3:
Database → Aggregation → Metrics → Graphical Visualization

---

## Execution Order

```bash
python fase1.py
python fase2.py
streamlit run visualizacao.py
```
