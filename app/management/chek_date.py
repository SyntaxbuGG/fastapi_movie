from datetime import datetime, timezone
from sqlmodel import SQLModel, Field


# ❌ created_static будет одинаковым во всех объектах
# Это значение вычисляется один раз при загрузке кода
created_once = datetime.now(timezone.utc)


class MyModel(SQLModel):
    created_static: datetime = Field(default_factory=lambda: created_once)
    created_dynamic: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# Создаём первый объект
a = MyModel()

# Подождём немного
import time
time.sleep(1)

# Создаём второй объект
b = MyModel()


print("created_static:")
print("a:", a.created_static)
print("b:", b.created_static)
print("Equal:", a.created_static == b.created_static)  # True ❌

print("\ncreated_dynamic:")
print("a:", a.created_dynamic)
print("b:", b.created_dynamic)
print("Equal:", a.created_dynamic == b.created_dynamic)  # False ✅
