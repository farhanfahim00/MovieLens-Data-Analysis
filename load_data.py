import pandas
import sqlite3

connection= sqlite3.connect("data/movies.db")
cursor= connection.cursor()

#Create Movies Table
cursor.execute('''CREATE TABLE IF NOT EXISTS movies (
    movie_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    genres TEXT,
    release_year INTEGER
)''')

#Create Ratings Table
cursor.execute('''CREATE TABLE IF NOT EXISTS ratings (
    rating_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    movie_id INTEGER NOT NULL,
    rating REAL NOT NULL CHECK(rating >= 0.5 AND rating <= 5.0),
    timestamp INTEGER NOT NULL,
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
)''')

#Create Tags Table 

cursor.execute('''CREATE TABLE IF NOT EXISTS tags (
    tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    movie_id INTEGER NOT NULL,
    tag TEXT NOT NULL,
    timestamp INTEGER NOT NULL,
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
)''')

#Load Movies Data
movies_df= pandas.read_csv("data/movies.csv")
ratings_df= pandas.read_csv("data/ratings.csv")
tags_df= pandas.read_csv("data/tags.csv")

#Extract year from title
def extract_year(title):
    """
    Extract year from title like 'Toy Story (1995)'
    Returns the year as integer, or None if not found
    """
    # Checking if title ends with (YYYY)
    if title.endswith(')') and '(' in title:
        #Get the last part between parentheses
        year_str = title[-5:-1]  
        
        #Checking if it's actually a number
        if year_str.isdigit():
            return int(year_str)
    
    return None  # No year found

#Applying to all movies
movies_df['release_year'] = movies_df['title'].apply(extract_year)

#Checking results
print(movies_df[['title', 'release_year']].head())

def clean_title(title):
    """
    Remove year from title
    'Toy Story (1995)' -> 'Toy Story'
    """
    #Finding last occurrence of (
    if '(' in title:
        #Split at last ( and take first part, strip whitespace
        return title.rsplit('(', 1)[0].strip()
    
    return title

#creating clean title column
movies_df['title_clean'] = movies_df['title'].apply(clean_title)

#Checking how many movies are missing years
missing_years = movies_df['release_year'].isna().sum()
print(f"Movies without year: {missing_years}")

#Fill with a default value (e.g., 0 or 1900)
movies_df['release_year'] = movies_df['release_year'].fillna(0)

#Replacing "(no genres listed)" with empty string
movies_df['genres'] = movies_df['genres'].replace('(no genres listed)', '')

print("\nRenaming columns...")

#Renaming movies columns
movies_df = movies_df.rename(columns={
    'movieId': 'movie_id'
})

#Renaming ratings columns
ratings_df = ratings_df.rename(columns={
    'userId': 'user_id',
    'movieId': 'movie_id'
})

#Renaming tags columns
tags_df = tags_df.rename(columns={
    'userId': 'user_id',
    'movieId': 'movie_id'
})

print("✓ Columns renamed")


print("\nSelecting final columns...")

movies_final = movies_df[['movie_id', 'title', 'genres', 'release_year']]

ratings_final = ratings_df[['user_id', 'movie_id', 'rating', 'timestamp']]

tags_final = tags_df[['user_id', 'movie_id', 'tag', 'timestamp']]

print(f"✓ Movies: {len(movies_final)} rows, {len(movies_final.columns)} columns")
print(f"✓ Ratings: {len(ratings_final)} rows, {len(ratings_final.columns)} columns")
print(f"✓ Tags: {len(tags_final)} rows, {len(tags_final.columns)} columns")




print("\nValidating data...")

#DATA VALIDATION

#Checking for duplicates
dup_movies = movies_final.duplicated(subset=['movie_id']).sum()
dup_ratings = ratings_final.duplicated().sum()
print(f"  Duplicate movies: {dup_movies}")
print(f"  Duplicate ratings: {dup_ratings}")

#Checking rating range
min_rating = ratings_final['rating'].min()
max_rating = ratings_final['rating'].max()
print(f"  Rating range: {min_rating} to {max_rating}")

#Checking for NULL in required fields
null_movie_ids = movies_final['movie_id'].isna().sum()
null_titles = movies_final['title'].isna().sum()
print(f"  Movies with NULL movie_id: {null_movie_ids}")
print(f"  Movies with NULL title: {null_titles}")

if dup_movies > 0 or null_movie_ids > 0 or null_titles > 0:
    print("⚠️  WARNING: Data quality issues detected!")
else:
    print("✓ Data validation passed")

#INSERT DATA INTO DATABASE


print("\nInserting data into database...")

try:
    # Insert movies first (because ratings reference movies)
    print("  Inserting movies...")
    movies_final.to_sql('movies', connection, if_exists='replace', index=False)
    print(f"  ✓ Inserted {len(movies_final)} movies")
    
    # Insert ratings
    print("  Inserting ratings...")
    ratings_final.to_sql('ratings', connection, if_exists='replace', index=False)
    print(f"  ✓ Inserted {len(ratings_final)} ratings")
    
    # Insert tags
    print("  Inserting tags...")
    tags_final.to_sql('tags', connection, if_exists='replace', index=False)
    print(f"  ✓ Inserted {len(tags_final)} tags")
    
except Exception as e:
    print(f"❌ Error inserting data: {e}")
    connection.close()
    exit(1)


#CREATING INDEXES FOR PERFORMANCE

print("\nCreating indexes...")

try:
    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_ratings_movie 
    ON ratings(movie_id)
    """)
    print("  ✓ Created index on ratings.movie_id")
    
    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_ratings_user 
    ON ratings(user_id)
    """)
    print("  ✓ Created index on ratings.user_id")
    
    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_tags_movie 
    ON tags(movie_id)
    """)
    print("  ✓ Created index on tags.movie_id")
    
except Exception as e:
    print(f"⚠️  Warning creating indexes: {e}")



#COMMITING AND CLOSE

print("\nFinalizing...")
connection.commit()
connection.close()
print("✓ Database connection closed")



#FINAL SUMMARY

print("\n" + "="*50)
print("🎉 DATABASE SETUP COMPLETE!")
print("="*50)
print(f"Database location: data/movies.db")
print(f"Total movies: {len(movies_final):,}")
print(f"Total ratings: {len(ratings_final):,}")
print(f"Total tags: {len(tags_final):,}")
print(f"Unique users: {ratings_final['user_id'].nunique():,}")
print(f"Average rating: {ratings_final['rating'].mean():.2f}")
print(f"Movies with release year: {(movies_final['release_year'] > 0).sum():,}")
print("="*50)