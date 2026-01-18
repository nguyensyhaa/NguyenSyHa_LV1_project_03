# 🎬 TMDB Movie Analysis (Pandas Refactor)

> **A High-Performance Data Engineering Showcase**  
> *Replicating Linux CMD analytics using optimized Python & Pandas.*

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Pandas](https://img.shields.io/badge/Pandas-Optimized-150458)
![Status](https://img.shields.io/badge/Build-Passing-brightgreen)

## 📌 Overview
This project is a professional refactor of the "Project 01 Linux CMD". It leverages the power of **Pandas Vectorization** to process movie datasets with 100% accuracy relative to legacy baselines. 

**Key Capabilities:**
- 🚀 **Direct Streaming**: Analyze data straight from the cloud (URL) without local storage overhead.
- 🛡️ **Robust ETL**: Auto-correction for "Future Year" errors (e.g., 2060 → 1960) and parsing of broken CSV records.
- ⚡ **High Performance**: Replaces O(n) manual loops with optimized C-engine parsing.

---

## 📊 Analysis Highlights (Tasks 1-8)

| Task | Description | Result Key Metrics |
| :--- | :--- | :--- |
| **1** | **Sorting** | Sorted 10,866 movies by release date. |
| **2** | **Filtering** | Found **350** movies with Rating > 7.5. |
| **3** | **Revenue Extremes** | 🏆 Max: **Avatar** ($2.78B)<br>🔻 Min: **Mallrats** ($2) |
| **4** | **Total Market** | **$432,720,192,875** (Exact Match with Ref) |
| **5** | **Top Profit** | #1 **Avatar** 📊 |
| **6** | **Top Talent** | 🎬 Director: **Woody Allen**<br>🎭 Actor: **Robert De Niro** 📊 |
| **7** | **Top Genres** | 1. **Drama** (4761)<br>2. **Comedy** (3793) 📊 |
| **8** | **ROI Analysis** | 💰 Top ROI: **The Gallows** (425x Return) 📊 |


---

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/Project01_Pandas.git

# Install dependencies
pip install -r requirements.txt
```

## 🚀 Usage

**Option 1: Stream directly from GitHub (Recommended)**
```bash
python main.py
```

**Option 2: Analyze a local file**
```bash
python main.py --local data/tmdb-movies.csv
```

## 📈 Visualizations
The project now generates insights charts (saved to `outputs/plots/`):
- **Movies per Year** (Task 1)
- **Rating Distribution** (Task 2)
- **Top Profit** (Task 5)
- **Top Talent** (Task 6)
- **Top Genres** (Task 7)
- **ROI Analysis** (Task 8)

Generate all charts:
```bash
python main.py --plot
```
(Or combine with `--task X` to generate specific charts)

## 📂 Project Structure


```text
Project01_Pandas/
├── outputs/            # [Generated] Analysis Results
│   ├── high_rated_movies.csv
│   ├── sorted_by_date.csv
│   └── plots/          # Generated Charts (Task 1, 2, 5-8)
├── src/
│   ├── etl.py          # Optimized Extraction & Cleaning Logic

│   └── tasks/          # [NEW] Modular Task Analysts
│       ├── task1_sorting.py
│       ├── ...
│       └── task8_roi.py
├── tests/
│   └── test_project.py # Regression Tests
├── main.py             # CLI Entry Point (Task Dispatcher)
└── requirements.txt

```

## 🔍 Quality Assurance
This project includes a regression test suite to ensure results identical to the legacy system:
- **Duplicates**: Preserved to match legacy reporting standards.
- **Date Handling**: Smart fixes for 2-digit years.

Running tests:
```bash
python -m pytest tests/test_project.py
```

---