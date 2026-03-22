from fastapi import APIRouter

from app.models.schemas import DashboardPayload
from app.services import dashboard_service

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("", response_model=DashboardPayload)
def get_dashboard() -> DashboardPayload:
    return dashboard_service.get_dashboard()
