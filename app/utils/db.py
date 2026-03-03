import asyncio
import json
from datetime import datetime
from pathlib import Path

from app.db_config import local_session
from app.models.video_snapshots import VideoSnapshot
from app.models.videos import Video


async def json_file_to_dict(file_path: Path) -> dict:
    return await asyncio.to_thread(
        lambda: json.loads(file_path.read_text(encoding="utf-8"))
    )


async def fill_db():
    """Fill db with initial data"""
    file_path = Path(__file__).parent.resolve() / "videos.json"
    data = await json_file_to_dict(file_path)

    # Create video and video_snapshot instances from file data
    videos = []
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
        videos.append(video)

        snapshots = []
        for snap_data in video_data.get("snapshots", []):
            snapshot = VideoSnapshot(
                id=snap_data["id"],
                video_id=snap_data["video_id"],
                views_count=snap_data["views_count"],
                likes_count=snap_data["likes_count"],
                comments_count=snap_data["comments_count"],
                reports_count=snap_data["reports_count"],
                delta_views_count=snap_data["delta_views_count"],
                delta_likes_count=snap_data["delta_likes_count"],
                delta_comments_count=snap_data["delta_comments_count"],
                delta_reports_count=snap_data["delta_reports_count"],
                created_at=datetime.fromisoformat(snap_data["created_at"]),
                updated_at=datetime.fromisoformat(snap_data["updated_at"]),
            )
            snapshots.append(snapshot)

        video.video_snapshots = snapshots

    # Save collected instances to DB
    async with local_session() as db:
        db.add_all(videos)
        await db.commit()
