import requests, csv

API_KEY = "8265bd1679663a7ea12ac168da84d2e8"   # your key
BASE_URL = "https://api.themoviedb.org/3"

# 1. Get genre mapping (id → name)
genre_url = f"{BASE_URL}/genre/movie/list?api_key={API_KEY}&language=en-US"
genres = requests.get(genre_url).json()["genres"]
genre_map = {g["id"]: g["name"] for g in genres}

# 2. Collect top rated movies (you can loop over pages)
movies = []
for page in range(1, 470):
    url = f"{BASE_URL}/movie/top_rated?api_key={API_KEY}&language=en-US&page={page}"
    data = requests.get(url).json()
    for m in data.get("results", []):
        title = m.get("title", "")
        desc = m.get("overview", "")
        genre_names = [genre_map.get(gid, "") for gid in m.get("genre_ids", [])]
        movies.append([title, desc, ", ".join(genre_names)])

# 3. Save to CSV
with open("movies_dataset.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Movie name", "Description", "Genre"])
    writer.writerows(movies)

print(f"Saved {len(movies)} movies to movies_dataset.csv ✅")
