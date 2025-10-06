# 🎬 Data Folder — MovieLens Dataset

This folder contains the raw CSV files from the [MovieLens Dataset](https://grouplens.org/datasets/movielens/), used to build the SQLite database for analysis.

---

##  Required Files

Please download the **MovieLens Latest Small** dataset (recommended for testing):

🔗 **Download:** [ml-latest-small.zip](https://files.grouplens.org/datasets/movielens/ml-latest-small.zip)

After extracting the ZIP file, copy the following CSVs into this folder:

data/
├─ movies.csv
├─ ratings.csv
└─ tags.csv

yaml

>  Do **not** commit these CSV files to GitHub — they are large and automatically excluded using `.gitignore`.

---

## Optional: Full Dataset

If you want to work with the full dataset:

🔗 **Download:** [ml-latest.zip](https://files.grouplens.org/datasets/movielens/ml-latest.zip)

Unzip and place the same CSVs in this directory.  
Be aware that this version is very large (~335 MB) and may take longer to process.

---

## Notes

- These datasets are provided by **GroupLens Research** for **educational and development use only**.  
- The data will change over time, so do not use it for published research.  
- Once the data is downloaded, you can run:

```bash
python load_data.py
````
to load and clean it into a local SQLite database at:

```bash
data/movies.db
````

© GroupLens Research — MovieLens Dataset
Used here for learning and non-commercial analysis.

yaml
Copy code
