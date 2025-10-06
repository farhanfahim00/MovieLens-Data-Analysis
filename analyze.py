import sqlite3
import pandas
import os

def get_connection():
    return sqlite3.connect("data/movies.db")

def top_rated_movies():
    conn = get_connection()
    query = """
    SELECT m.title, AVG(r.rating) as avg_rating, COUNT(r.rating) as num_ratings
    FROM movies m
    JOIN ratings r ON m.movie_id = r.movie_id
    GROUP BY m.movie_id
    HAVING num_ratings >= 50
    ORDER BY avg_rating DESC
    LIMIT 20;
    """
    df = pandas.read_sql_query(query, conn)
    conn.close()
    return df

def most_rated_movies():
    conn = get_connection()
    query = """
    SELECT m.title, COUNT(r.rating) as num_ratings
    FROM movies m
    JOIN ratings r ON m.movie_id = r.movie_id
    GROUP BY m.movie_id
    ORDER BY num_ratings DESC
    LIMIT 20;
    """
    df = pandas.read_sql_query(query, conn)
    conn.close()
    return df

def ratings_distribution():
    conn = get_connection()
    query = """
    SELECT rating, COUNT(*) as count
    FROM ratings
    GROUP BY rating
    ORDER BY rating;
    """
    df = pandas.read_sql_query(query, conn)
    conn.close()
    return df

def genre_popularity():
    """Analyze genre popularity - done in Python because SQLite can't split strings"""
    conn = get_connection()
    
    # Step 1: Get all movies with their genres
    query = "SELECT movie_id, genres FROM movies WHERE genres IS NOT NULL AND genres != ''"
    movies_df = pandas.read_sql_query(query, conn)
    
    # Step 2: Get all ratings
    ratings_query = "SELECT movie_id, rating FROM ratings"
    ratings_df = pandas.read_sql_query(query, conn)
    conn.close()
    
    # Step 3: Split genres and count
    genre_counts = {}
    
    for _, row in movies_df.iterrows():
        genres = row['genres'].split('|')  # Split by pipe
        for genre in genres:
            genre = genre.strip()  # Remove whitespace
            if genre:
                if genre not in genre_counts:
                    genre_counts[genre] = 0
                genre_counts[genre] += 1
    
    # Step 4: Create DataFrame
    genre_df = pandas.DataFrame([
        {'genre': genre, 'movie_count': count}
        for genre, count in genre_counts.items()
    ])
    
    # Sort by count
    genre_df = genre_df.sort_values('movie_count', ascending=False)
    
    return genre_df


def rating_trends_over_time():
    conn = get_connection()
    query = """
    SELECT STRFTIME('%Y-%m', DATETIME(timestamp, 'unixepoch')) as month, AVG(rating) as avg_rating
    FROM ratings
    GROUP BY month
    ORDER BY month;
    """
    df = pandas.read_sql_query(query, conn)
    conn.close()
    return df


def movies_by_rating_category():
    """Categorize movies by their average rating"""
    conn = get_connection()
    
    # Get average rating per movie
    query = """
    SELECT m.movie_id, m.title, AVG(r.rating) as avg_rating
    FROM movies m
    JOIN ratings r ON m.movie_id = r.movie_id
    GROUP BY m.movie_id
    HAVING COUNT(r.rating) >= 10
    """
    
    df = pandas.read_sql_query(query, conn)
    conn.close()
    
    # Categorize in Python
    def categorize_rating(avg_rating):
        if avg_rating >= 4.0:
            return 'Excellent'
        elif avg_rating >= 3.5:
            return 'Good'
        elif avg_rating >= 3.0:
            return 'Average'
        elif avg_rating >= 2.5:
            return 'Below Average'
        else:
            return 'Poor'
    
    df['category'] = df['avg_rating'].apply(categorize_rating)
    
    # Count movies in each category
    category_counts = df['category'].value_counts().reset_index()
    category_counts.columns = ['rating_category', 'movie_count']
    
    return category_counts


#ALL EXPORTS

def export_all():
    # Create analysis folder if it doesn't exist
    if not os.path.exists('analysis'):
        os.makedirs('analysis')
        print("Created 'analysis/' folder\n")
    
    print("="*60)
    print("🎬 RUNNING MOVIE ANALYTICS")
    print("="*60)
    
    # Analysis 1: Top Rated Movies
    print("\n1️⃣  Analyzing top rated movies...")
    try:
        df1 = top_rated_movies()
        df1.to_csv('analysis/top_rated_movies.csv', index=False)
        print(f"   ✓ Exported {len(df1)} movies")
        print(f"   📊 Top movie: {df1.iloc[0]['title']}")
        print(f"   ⭐ Rating: {df1.iloc[0]['avg_rating']:.2f} ({int(df1.iloc[0]['num_ratings'])} ratings)")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Analysis 2: Most Rated Movies
    print("\n2️⃣  Analyzing most rated movies...")
    try:
        df2 = most_rated_movies()
        df2.to_csv('analysis/most_rated_movies.csv', index=False)
        print(f"   ✓ Exported {len(df2)} movies")
        print(f"   📊 Most rated: {df2.iloc[0]['title']}")
        print(f"   🔢 Ratings: {int(df2.iloc[0]['num_ratings'])}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Analysis 3: Rating Distribution
    print("\n3️⃣  Analyzing rating distribution...")
    try:
        df3 = ratings_distribution()
        df3.to_csv('analysis/rating_distribution.csv', index=False)
        print(f"   ✓ Exported {len(df3)} rating levels")
        most_common_idx = df3['count'].idxmax()
        print(f"   📊 Most common rating: {df3.iloc[most_common_idx]['rating']} ⭐")
        print(f"   🔢 Count: {int(df3.iloc[most_common_idx]['count'])} ratings")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Analysis 4: Genre Popularity
    print("\n4️⃣  Analyzing genre popularity...")
    try:
        df4 = genre_popularity()
        df4.to_csv('analysis/genre_popularity.csv', index=False)
        print(f"   ✓ Exported {len(df4)} genres")
        if len(df4) > 0:
            print(f"   📊 Top 3 genres:")
            for i in range(min(3, len(df4))):
                print(f"      {i+1}. {df4.iloc[i]['genre']}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Analysis 5: Rating Trends Over Time
    print("\n5️⃣  Analyzing rating trends over time...")
    try:
        df5 = rating_trends_over_time()
        df5.to_csv('analysis/rating_trends_time.csv', index=False)
        print(f"   ✓ Exported {len(df5)} time periods")
        print(f"   📅 Date range: {df5.iloc[0]['month']} to {df5.iloc[-1]['month']}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Analysis 6: Movies by Rating Category
    print("\n6️⃣  Analyzing movies by rating category...")
    try:
        df6 = movies_by_rating_category()
        df6.to_csv('analysis/movies_by_category.csv', index=False)
        print(f"   ✓ Exported {len(df6)} categories")
        print(f"   📊 Category breakdown:")
        for _, row in df6.iterrows():
            print(f"      • {row['rating_category']}: {int(row['count'])} ratings")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Summary
    print("\n" + "="*60)
    print("✅ ANALYSIS COMPLETE!")
    print("="*60)
    print("📁 All CSV files saved in 'analysis/' folder")
    print("📊 Files created:")
    print("   1. top_rated_movies.csv")
    print("   2. most_rated_movies.csv")
    print("   3. rating_distribution.csv")
    print("   4. genre_popularity.csv")
    print("   5. rating_trends_time.csv")
    print("   6. movies_by_category.csv")
    print("\n🎯 Ready to import into Power BI!")
    print("="*60)


# Main execution
if __name__ == "__main__":
    export_all()