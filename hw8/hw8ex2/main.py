from dp import DpQuerySession

DB = 'imdb-dp.csv'
BUDGET = 1

querier = DpQuerySession("imdb-dp.csv", privacy_budget=10)
for _ in range(10):
    count = querier.get_count("Seven Samurai", rating_threshold=3, epsilon=0.25)

    print(count)