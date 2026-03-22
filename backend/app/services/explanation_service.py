from app.adapters import pipeline_adapter
from app.models.schemas import ExplanationPayload


def get_explanation_for_ticker(ticker: str) -> ExplanationPayload:
    detail = pipeline_adapter.get_ticker_signal_detail(ticker)
    return ExplanationPayload.model_validate(detail["explanation"])
