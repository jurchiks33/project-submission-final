from app.adapters import pipeline_adapter
from app.models.schemas import RuntimeSettings


def get_settings() -> RuntimeSettings:
    return RuntimeSettings.model_validate(pipeline_adapter.get_settings_snapshot())
