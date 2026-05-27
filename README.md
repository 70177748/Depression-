# Reddit Depression in Indian Society — Premium EDA Dashboard

A professional Streamlit dashboard for the Kaggle dataset: `parthanimesh/reddit-posts-on-depression-in-indian-society`.

## Features
- Premium dark responsive interface
- KPI cards: total records, average words, average risk score, critical share
- Linked sidebar filters: date range, category, numerical range, multi-select, keyword search, reset
- 10 required charts: pie, histogram, line, bar, scatter, box, heatmap, area, count, violin
- Bonus text analytics: word cloud, risk bands, negative/positive signal counts
- Modular code structure: `app.py`, `charts.py`, `filters.py`

## Folder Structure
```text
reddit_depression_premium_dashboard/
├── data/
│   └── Put the original dataset file here without renaming it
├── notebooks/
│   └── analysis.ipynb
├── app.py
├── charts.py
├── filters.py
├── download_dataset.py
├── requirements.txt
└── README.md
```

## Local Setup
```bash
pip install -r requirements.txt
python download_dataset.py
streamlit run app.py
```

If Kaggle asks for login, manually download the dataset from Kaggle and place the original CSV/XLSX/JSON file inside the `data/` folder without renaming it.

## Streamlit Cloud Deployment
1. Upload this full folder to GitHub.
2. Go to Streamlit Community Cloud.
3. Create a new app from your GitHub repository.
4. Main file path: `app.py`.
5. Deploy.

## Notes
- This project is for exploratory data analysis and education only.
- The risk score is a simple keyword-based signal for EDA, not a clinical diagnosis.
- Keep the dataset filename unchanged to match project rules.
