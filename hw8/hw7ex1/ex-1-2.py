import pandas as pd

ANON_DATA_FOLDER = 'anon_data/'
COM_402_DB = 'com402-2.csv'
IMD_DB = 'imdb-2.csv'
SOLUTIONS_FOLDER = 'real_data/'
SOLUTION_FILE = 'user-2.csv'
CLEAR_COLUMN_NAMES = ['email', 'movie', 'date', 'rating']
HASHED_COLUMN_NAMES = ['hashed_email', 'hashed_movie', 'date', 'rating']
DONALD_EMAIL = 'donald.trump@whitehouse.gov'

def main():
    # Read files
    com401 = pd.read_csv(ANON_DATA_FOLDER + COM_402_DB, header=None, names=HASHED_COLUMN_NAMES)
    imdb = pd.read_csv(ANON_DATA_FOLDER + IMD_DB, header=None, names=CLEAR_COLUMN_NAMES)
    
    grouped_hashed_movies = (
        com401.groupby('hashed_movie')
            .count()
            .sort_values(by='date', ascending=False)
            .reset_index()
    )
    
    grouped_clear_movies = (
        imdb.groupby('movie')
            .count()
            .sort_values(by='date', ascending=False)
            .reset_index()
    )

    movies_hashes = (
        pd.concat([grouped_hashed_movies, grouped_clear_movies], axis=1)[['hashed_movie', 'movie']]
    )
    
    clear_watched_movies = imdb[imdb['email'] == DONALD_EMAIL]
    
    com401_with_clear_movies = com401.merge(movies_hashes, on='hashed_movie')

    donald_hashed_email = (
        com401_with_clear_movies
            .merge(clear_watched_movies, on='movie', how='inner')
            .groupby('hashed_email')
            .filter(lambda x: x['hashed_movie'].count() == clear_watched_movies.shape[0])
            .reset_index()
    ).loc[0, 'hashed_email']
    
    hashed_movies_watched_by_donald = com401[com401['hashed_email'] == donald_hashed_email]

    movies_watched_by_donald = (
        hashed_movies_watched_by_donald
            .merge(movies_hashes, on='hashed_movie')['movie'].drop_duplicates()
    )

    # Print result
    [print(movie) for movie in movies_watched_by_donald]

    check(movies_watched_by_donald)

def check(found):
    solution = pd.read_csv(SOLUTIONS_FOLDER + SOLUTION_FILE, header=None, names=['movie'])
    
    merged = solution.merge(found, on='movie')

    assert merged.size == solution.size and found.size == merged.size

    print('Success!')

if __name__ == '__main__':
    main()