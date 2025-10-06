# MovieLens Data Analysis — SQLite + Pandas + Power BI

This project demonstrates a complete end-to-end **data analysis workflow** using the [MovieLens Dataset](https://grouplens.org/datasets/movielens/).  
It covers **data transformation, cleaning, SQL querying, and visualization** using modern tools.

---

## Overview

The goal of this project is to:
1. Convert the **MovieLens dataset** into a structured **SQLite database**.
2. Use **Pandas** for cleaning and validating data.
3. Perform **SQL-based analytics** and export results.
4. Visualize insights using **Microsoft Power BI**.

This project is **recommended for learning and educational purposes** in data analysis, SQL, and visualization.

---

## Tech Stack

| Component | Tool / Library |
|------------|----------------|
| Database | SQLite3 |
| Data Processing | Python (Pandas) |
| Data Visualization | Power BI |
| Dataset | MovieLens (Latest Small / Full Dataset) |

---

## Dataset Details

The dataset is provided by [GroupLens](https://grouplens.org/datasets/movielens/).

| Version | Size | Description |
|----------|------|-------------|
| **Small** | 100,000 ratings and 3,600 tags | 9,000 movies rated by 600 users |
| **Full** | 33,000,000 ratings and 2,000,000 tags | 86,000 movies rated by 330,975 users |

> **Note:** These datasets change over time and are not intended for published research.

---

##  Project Structure
```
📦 movielens-sqlite-pandas-powerbi
┣ 📂 data/ # Raw MovieLens CSVs (movies.csv, ratings.csv, tags.csv)
┣ 📂 analysis/ # Output CSVs from SQL analytics
┣ 📜 load_data.py # Loads and cleans CSVs, builds SQLite database
┣ 📜 analyze.py # Runs analytical SQL queries and exports results
┣ 📜 PowerBI_Report.pbix # (Optional) Power BI dashboard file
┗ 📜 README.md
```


##  How to Run

### Setup Environment
```bash
pip install pandas sqlite3
```

### Load and Clean Data

Place your MovieLens CSV files in the data/ folder:

kotlin

data/
 ├─ movies.csv
 ├─ ratings.csv
 └─ tags.csv
Run the loader script:

```bash
python load_data.py
```

This creates a local database at data/movies.db.

### Run Analytics
```bash
python analyze.py
```

This script:

Calculates top-rated and most-rated movies

Finds genre popularity

Analyzes rating trends over time

Categorizes movies by average rating

Exports all insights as .csv files inside /analysis

## Power BI Visualization
Once the CSVs are generated, open Power BI and import them from the analysis/ folder.

Recommended dashboards:

Top 20 Rated Movies

Rating Distribution

Genre Popularity

Rating Trends Over Time

Movie Categories (Excellent → Poor)

Example Insights

## Metric	Example
Top Movie	The Shawshank Redemption
Common Rating	⭐ 4.0
Popular Genre	Drama
Rating Range	0.5 – 5.0
Avg. Rating	~3.5

## Educational Focus

This project demonstrates:

Data modeling and cleaning using Pandas

SQL database creation and indexing in SQLite

Query optimization and data analysis

Exporting clean data for BI tools like Power BI

## Author
Farhan Fahim Taimoor
🎓 B.Sc. Artificial Intelligence — Deggendorf Institute of Technology

## License
This project is licensed under the MIT License.
Dataset © GroupLens — for educational and development use only.

