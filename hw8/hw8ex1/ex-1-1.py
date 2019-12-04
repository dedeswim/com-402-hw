import pandas as pd

ANON_DATA_FOLDER = 'anon_data/'
COM_402_DB = 'com402-1.csv'
IMD_DB = 'imdb-1.csv'
SOLUTIONS_FOLDER = 'real_data/'
SOLUTION_FILE = 'user-1.csv'
COLUMNS_NAMES = ['email', 'movie', 'date', 'rating']

def main():
    # Read files
    com401_1 = pd.read_csv(ANON_DATA_FOLDER + COM_402_DB, header=None, names=COLUMNS_NAMES)
    imdb_1 = pd.read_csv(ANON_DATA_FOLDER + IMD_DB, header=None, names=COLUMNS_NAMES)

    # Create a merged dataframe to couple the subset to the total set
    merged = imdb_1.merge(com401_1, on=['date', 'rating'], how='inner')

    # Get the email
    hashed_trump_email = merged.loc[merged['email_x'] == 'donald.trump@whitehouse.gov', 'email_y'].iloc[0]

    # Get the hashes of the movies
    movies_hashes = (
        merged.groupby(['movie_y', 'movie_x'])
            # Count the number of times a movie has a specifi hash
            .count()
            # Get the most frequent film per hash
            .sort_values('email_x', ascending=False)
            .groupby(level=0)
            .head(1).reset_index()
    )

    # Get hashed movies whatched by Donald
    hashed_movies_watched_by_donald = com401_1[com401_1['email'] == hashed_trump_email]

    # Get movies wathced by Donald
    movies_watched_by_donald = (
        hashed_movies_watched_by_donald
            .merge(movies_hashes, left_on=['movie'], right_on=['movie_y'])['movie_x'].drop_duplicates()
    )

    # Print result
    [print(movie) for movie in movies_watched_by_donald]

    check(movies_watched_by_donald)

def check(found):
    solution = pd.read_csv(SOLUTIONS_FOLDER + SOLUTION_FILE, header=None, names=['movie_x'])
    
    merged = solution.merge(found, on='movie_x')

    assert merged.size == solution.size and found.size == merged.size

    print('Success!')

if __name__ == '__main__':
    main()