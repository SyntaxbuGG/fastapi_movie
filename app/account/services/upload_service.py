from fastapi import UploadFile
from sqlmodel.ext.asyncio.session import AsyncSession
from pathlib import Path
from uuid import uuid4

from ..repositories import user_repo
from app.core.exceptions import (
    FileTooLargeError,
    InvalidInputError,
    ResourceNotFoundError,
)
from app.utils.file_utils import delete_file_from_disk, save_file_to_disk

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
ALLOWED_MIME_TYPES = {"image/png", "image/jpeg"}
MAX_FILE_SIZE_MB = 2
MAX_FILE_SIZE = MAX_FILE_SIZE_MB * 1024 * 1024


async def upload_user_image(session: AsyncSession, current_user: int, file: UploadFile):
    user = await user_repo.get_active_user(session=session, user_id=current_user)
    if not user:
        raise ResourceNotFoundError(resource="user")

    # 🔒 Проверка расширения
    ext = file.filename.split(".")[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise InvalidInputError(
            field="Image",
            message="Only .png, .jpg, .jpeg files are allowed",
        )

    # 🔒 Проверка MIME-типа
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise InvalidInputError(field="mime_type", message="Invalid Image MIME type")

    # 🔒 Проверка размера
    contents_image = await file.read()
    if len(contents_image) > MAX_FILE_SIZE:
        raise FileTooLargeError(limit_mb=MAX_FILE_SIZE_MB)

    #  внутреннего указателя в начало файла.
    file.file.seek(0)

    if user.user_image:
        # Удаление изображение из диска памяти
        await delete_file_from_disk(path=Path(f"app/{user.user_image}"))

    filename = f"{uuid4().hex}_{file.filename}"
    directory = "app/static/avatars"
    await save_file_to_disk(file=file, directory=directory, filename=filename)
    avatar_url = f"static/avatars/{filename}"

    user.user_image = avatar_url
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return avatar_url
