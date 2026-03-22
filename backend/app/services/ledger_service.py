from app.adapters import pipeline_adapter
from app.models.schemas import Position


def get_positions() -> list[Position]:
    return [Position.model_validate(item) for item in pipeline_adapter.get_positions_snapshot()]
