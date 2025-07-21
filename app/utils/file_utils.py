import os

from pathlib import Path
from fastapi import UploadFile
from anyio import open_file, to_thread


async def save_file_to_disk(file: UploadFile, directory: str, filename: str) -> str:
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    async with open_file(path, "wb") as buffer:
        while chunk := await file.read(size=64 * 1024):
            await buffer.write(chunk)
    return path


async def delete_file_from_disk(path: Path) -> None:
    def _delete():
        try:
            if path.exists():
                path.unlink()
        except Exception as e:
            print(f"⚠️ Ошибка при удалении изображение: {e}")

    await to_thread.run_sync(_delete)
