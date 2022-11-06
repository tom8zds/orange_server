from app.dev_config import api_key
import tmdbsimple as tmdb
tmdb.API_KEY = api_key

search = tmdb.Search()
response = search.tv (query='bangumi_name')
for s in search.results:
    print(s['title'], s['id'], s['release_date'], s['popularity'])