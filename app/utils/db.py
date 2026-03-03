from app.db_config import local_session

from app.models.video_snapshots import VideoSnapshot
from app.models.videos import Video
from datetime import datetime
import json
import asyncio
from pathlib import Path


async def json_file_to_dict(file_path: Path) -> dict:
    return await asyncio.to_thread(
        lambda: json.loads(file_path.read_text(encoding="utf-8"))
    )


async def fill_db():
    file_path = Path(__file__).parent.resolve() / "videos.json"
    data = await json_file_to_dict(file_path)

    async with local_session() as db:
        for video_data in data["videos"]:
            video = Video(
                id=video_data["id"],
                creator_id=video_data["creator_id"],
                video_created_at=datetime.fromisoformat(video_data["video_created_at"]),
                views_count=video_data["views_count"],
                likes_count=video_data["likes_count"],
                comments_count=video_data["comments_count"],
                reports_count=video_data["reports_count"],
                created_at=datetime.fromisoformat(video_data["created_at"]),
                updated_at=datetime.fromisoformat(video_data["updated_at"]),
            )

            db.add(video)

            for snapshot_data in video_data.get("snapshots", []):
                snapshot = VideoSnapshot(
                    id=snapshot_data["id"],
                    video_id=snapshot_data["video_id"],
                    views_count=snapshot_data["views_count"],
                    likes_count=snapshot_data["likes_count"],
                    comments_count=snapshot_data["comments_count"],
                    reports_count=snapshot_data["reports_count"],
                    delta_views_count=snapshot_data["delta_views_count"],
                    delta_likes_count=snapshot_data["delta_likes_count"],
                    delta_comments_count=snapshot_data["delta_comments_count"],
                    delta_reports_count=snapshot_data["delta_reports_count"],
                    created_at=datetime.fromisoformat(snapshot_data["created_at"]),
                    updated_at=datetime.fromisoformat(snapshot_data["updated_at"]),
                )

                db.add(snapshot)

        await db.commit()
