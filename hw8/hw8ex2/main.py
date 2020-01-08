from dp import DpQuerySession

DB = 'imdb-dp.csv'
BUDGET = 1

querier = DpQuerySession("imdb-dp.csv", privacy_budget=1000)
for _ in range(10):
    count = querier.get_count("Seven Samurai", rating_threshold=3, epsilon=1000)

    print(count)