from slugify import slugify
from app.movie.models import Genre, Category
from app.db import get_db
from sqlmodel import select



# JSON данных от TMDB
genre_data = {
    "genres": [
        {"id": 28, "name": "Action"},
        {"id": 12, "name": "Adventure"},
        {"id": 16, "name": "Animation"},
        {"id": 35, "name": "Comedy"},
        {"id": 80, "name": "Crime"},
        {"id": 99, "name": "Documentary"},
        {"id": 18, "name": "Drama"},
        {"id": 10751, "name": "Family"},
        {"id": 14, "name": "Fantasy"},
        {"id": 36, "name": "History"},
        {"id": 27, "name": "Horror"},
        {"id": 10402, "name": "Music"},
        {"id": 9648, "name": "Mystery"},
        {"id": 10749, "name": "Romance"},
        {"id": 878, "name": "Science Fiction"},
        {"id": 10770, "name": "TV Movie"},
        {"id": 53, "name": "Thriller"},
        {"id": 10752, "name": "War"},
        {"id": 37, "name": "Western"},
    ]
}


category_data = {
    "categories": ["Movies", "TV Series", "Anime", "Documentaries", "Kids", "Cartoons"]
}


async def add_genres_to_db():
    async for db in get_db():
        for genre in genre_data["genres"]:
            slug = slugify(genre["name"], separator="-")
            stmt = select(Genre).where(Genre.slug == slug)
            existing = (await db.exec(stmt)).first()

            if existing:
                continue

            genre_obj = Genre(name=genre["name"], id_tmdb=genre["id"], slug=slug)
            db.add(genre_obj)

        await db.commit()
    print(f"Added {len(genre_data['genres'])} genres to the database.")


async def add_categories_to_db():
    async for db in get_db():
        for category in category_data["categories"]:
            slug = slugify(category, separator="-")

            stmt = select(Category).where(Category.slug == slug)
            existing = (await db.exec(stmt)).first()

            if existing:
                continue  # уже есть — пропускаем

            category_obj = Category(name=category, slug=slug)
            db.add(category_obj)
        await db.commit()
    print(f"Added {len(category_data['categories'])} categories to the database.")


if __name__ == "__main__":
    # add_genres_to_db()
    # add_categories_to_db()

    pass
