from operator import ge
import httpx
import pprint
import asyncio
import json
from pathlib import Path
from app.db import get_db

# Настройки лимитов TMDb и HTTP-клиента
SEMAPHORE_LIMIT = 10  # max параллельных HTTP-запросов
RATE_LIMIT = 40  # max запросов в секунду
semaphore = asyncio.Semaphore(SEMAPHORE_LIMIT)


async def fetch_movies(client: httpx.AsyncClient, page: int = 1):
    url = f"https://api.themoviedb.org/3/discover/movie?include_adult=true&include_video=false&language=en-US&page={page}&primary_release_date.gte=2023-01-01&primary_release_date.lte=2023-03-01&sort_by=popularity.desc"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzZGY4NzE1YTU2YTZjY2E1MzUwY2RkNjQ5ZDU4YjhkMCIsIm5iZiI6MTc1MDQxNDM0Mi45NzIsInN1YiI6IjY4NTUzNDA2YzBhZGU2YTE2NDI5ZTU1OSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.7rmPV08xEEYELDENnuPBPsl3lUCtJ-yLykRb1iUZuQM",
    }
    async with semaphore:
        response = await client.get(url=url, headers=headers)
        data = response.json()
        return data.get("results", [])


def save_movies(movies: list[dict]):
    for m in movies:
        movie = Movie(
            id=m["id"],
            title=m["title"],
            release_date=m.get("release_date"),
            popularity=m.get("popularity"),
        )
        get_db().add(movie)
        



def save_to_json(data, filename=r"database_movies.json"):
    path = Path("app") / "management" / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


async def get_():
    async with httpx.AsyncClient(
        limits=httpx.Limits(max_connections=SEMAPHORE_LIMIT)
    ) as client:
        all_movies = []
    
        pages = 500
        for batch_start in range(RATE_LIMIT, pages + 1, RATE_LIMIT):
            batch_end = min(batch_start + RATE_LIMIT, pages + 1)
            tasks = [fetch_movies(client, p) for p in range(batch_start, batch_end)]
            pages_data = await asyncio.gather(*tasks)
            for movies in pages_data:
                all_movies.extend(movies)
            await asyncio.sleep(2)
        save_to_json(all_movies)


if __name__ == "__main__":
    asyncio.run(get_())
