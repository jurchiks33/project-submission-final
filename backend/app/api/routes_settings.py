from fastapi import APIRouter

from app.models.schemas import RuntimeSettings
from app.services import settings_service

router = APIRouter(prefix="/settings", tags=["settings"])


@router.get("", response_model=RuntimeSettings)
def get_settings() -> RuntimeSettings:
    return settings_service.get_settings()
