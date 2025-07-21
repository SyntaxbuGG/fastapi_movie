from fastapi.concurrency import run_in_threadpool
import bcrypt



async def hash_password(password: str) -> str:
    return await run_in_threadpool(
        lambda: bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    )


async def verify_password(plain: str, hashed: str) -> bool:
    return await run_in_threadpool(
        lambda: bcrypt.checkpw(plain.encode(), hashed.encode())
    )


