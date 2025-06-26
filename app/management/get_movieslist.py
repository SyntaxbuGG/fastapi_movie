import httpx
from pprint import pprint  # noqa: F401
import asyncio
import json
from pathlib import Path
from slugify import slugify
from sqlmodel import select, Session

from app.db import get_db
from app.movie.models import Genre, Movie, Category

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


async def get_genres_by_tmdb_ids(tmdb_ids: list[int], db: Session) -> list[Genre]:
    if not tmdb_ids:
        return []
    stmt = select(Genre).where(Genre.id_tmdb.in_(tmdb_ids))
    result = await db.exec(stmt)
    return result.all()


async def save_movies_to_movies_category():
    path = Path("app") / "management" / "database_movies.json"
    if not path.exists():
        print(f"File {path} does not exist. Please run get_movieslist.py first.")
        return

    with path.open("r", encoding="utf-8") as f:
        movies_data = json.load(f)

    async for db in get_db():
        movies_data_objects = []
        user_slugs = set()

        for movie in movies_data:
            slug = slugify(movie.get("title"), separator="-")

            stmt = select(Movie).where(Movie.id_tmdb == movie["id"])
            existing_id = (await db.exec(stmt)).first()
            stmt = select(Movie).where(
                Movie.slug == slugify(movie.get("title"), separator="-")
            )
            existing_slug = (await db.exec(stmt)).first()
            stmt = select(Category).where(Category.slug == "movies")
            category_result = (await db.exec(stmt)).first()
            if existing_id or existing_slug or slug in user_slugs:
                continue

            user_slugs.add(slug)

            movie_obj = Movie(
                id_tmdb=movie.get("id"),
                title=movie.get("title"),
                original_title=movie.get("original_title"),
                original_language=movie.get("original_language"),
                description=movie.get("overview"),
                slug=slugify(movie.get("title", ""), separator="-"),
                poster=movie.get("poster_path"),
                backdrop=movie.get("backdrop_path"),
                release_date=movie.get("release_date"),
                vote_average=movie.get("vote_average"),
                vote_count=movie.get("vote_count"),
                popularity=movie.get("popularity"),
                genres=await get_genres_by_tmdb_ids(
                    [genre for genre in movie.get("genre_ids", [])], db
                ),
                adult=movie.get("adult", False),
                category=category_result,
            )
            movies_data_objects.append(movie_obj)
        db.add_all(movies_data_objects)
        await db.commit()
    print(f"Saved {len(movies_data_objects)} movies to the database.")


if __name__ == "__main__":
    # asyncio.run(get_())
    save_movies_to_movies_category()
