from openai import AsyncOpenAI

from app.config import settings

DEFAULT_PROMPT = """
Ты — эксперт по PostgreSQL. Твоя задача — переводить вопросы пользователя на русском языке в SQL-запросы.
Имеются следующие таблицы:

class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        onupdate=func.now(),
    )

class Video(Base):
    __tablename__ = "videos"

    id: Mapped[str] = mapped_column(primary_key=True)
    creator_id: Mapped[str] = mapped_column()
    video_created_at: Mapped[datetime] = mapped_column()
    views_count: Mapped[int] = mapped_column()
    likes_count: Mapped[int] = mapped_column()
    comments_count: Mapped[int] = mapped_column()
    reports_count: Mapped[int] = mapped_column()

    video_snapshots: Mapped[list["VideoSnapshot"]] = relationship(
        back_populates="video"
    )

и 

class VideoSnapshot(Base):
    __tablename__ = "video_snapshots"

    id: Mapped[str] = mapped_column(primary_key=True)
    video_id: Mapped[str] = mapped_column(ForeignKey("videos.id", ondelete="SET NULL"))
    video: Mapped["Video"] = relationship()

    views_count: Mapped[int] = mapped_column()
    likes_count: Mapped[int] = mapped_column()
    comments_count: Mapped[int] = mapped_column()
    reports_count: Mapped[int] = mapped_column()

    # Разница между значениями из прошлого snapshot и этого
    delta_views_count: Mapped[int] = mapped_column()
    delta_likes_count: Mapped[int] = mapped_column()
    delta_comments_count: Mapped[int] = mapped_column()
    delta_reports_count: Mapped[int] = mapped_column()


Ты должен уметь переводить запросы типа

«Сколько всего видео есть в системе?»
«Сколько видео у креатора с id ... вышло с 1 ноября 2025 по 5 ноября 2025 включительно?»
«Сколько видео набрало больше 100 000 просмотров за всё время?»
«На сколько просмотров в сумме выросли все видео 28 ноября 2025?»
«Сколько разных видео получали новые просмотры 27 ноября 2025?»

в код SQL на основе моделей, которые я описал.
В качестве ответа просто верни SQL запрос без каких либо пояснений или форматирования.
То есть верни чистый текст SQL кода и ничего больше!
Только текст!!! Никаких спецсимволов типа ` \n и т.д.!
Верни ПРОСТО СЫРОЙ ТЕКСТ ОДНОЙ СТРОКОЙ!!! Обычный ТЕКСТ!!!
Не в формате кода! А просто ТЕКСТ ОДНОЙ СТРОКОЙ!!!
БЕЗ MARKDOWN СИМВОЛОВ!

А теперь переведи запрос ниже в SQL код:
"""

client = AsyncOpenAI(
    api_key=settings.openai_api_key,
    base_url="https://openrouter.ai/api/v1",
)


async def create_sql_query(msg: str):
    """Convert text to raw SQL query using LLM"""
    try:
        res = await client.responses.create(
            model="stepfun/step-3.5-flash:free",
            input=DEFAULT_PROMPT + "\n" + msg,
        )
        print("SQL запрос от LLM: ", res.output_text)
        return [str(res.output_text), None]
    except:
        return [None, "LLM не отвечает"]
