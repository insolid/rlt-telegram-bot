## Описание
Телеграм бот для подсчета статистики по видео на основе запросов на русском языке.


## Запуск
1. Склонировать репозиторий
```bash
git clone https://github.com/insolid/rlt-telegram-bot.git
```
2. Создать в корне проекта файл **.env**, скопировать туда значения из **.env.example** и заполнить своими значениями ключи
`BOT_TOKEN` и `OPENAI_API_KEY`

4. Из папки проекта выполнить команду
```bash
docker compose up
```


## Архитектура
Для преобразования текстовых запросов в SQL используется бесплатное API LLM из https://openrouter.ai.
Для каждого запроса к LLM используется **промпт настройки** + **сам текстовый запрос**.
Промпт выглядит следующим образом:
```
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

и прочие похожие текстовые запросы в код SQL на основе моделей, которые я описал.
При этом ты умеешь возвращать ТОЛЬКО select запросы! То есть без insert, update, delete и прочих действий!
В качестве ответа просто верни SQL запрос без каких либо пояснений или форматирования.
То есть верни чистый текст SQL кода и ничего больше!
Только текст!!! Никаких спецсимволов типа ` \n и т.д.!
Верни ПРОСТО СЫРОЙ ТЕКСТ ОДНОЙ СТРОКОЙ!!! Обычный ТЕКСТ!!!
Не в формате кода! А просто ТЕКСТ ОДНОЙ СТРОКОЙ!!!
БЕЗ MARKDOWN СИМВОЛОВ!

А теперь переведи запрос ниже в SQL код:
```

## Стек
- Aiogram
- SQLAlchemy + Alembic
- Postgresql
- Docker
