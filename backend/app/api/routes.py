import logging

from fastapi import APIRouter

from ..models.schemas import RecommendRequest, RecommendResponse
from ..services.recommend import recommend_movies

router = APIRouter(prefix="/api")
logger = logging.getLogger(__name__)


@router.get("/health")
async def health():
    logger.info("Health endpoint called")
    return {"status": "ok"}


@router.post("/recommend")
async def recommend_route(payload: RecommendRequest) -> RecommendResponse:
    logger.info("Recommend endpoint called (query_chars=%d, top_k=%d)", len(payload.query), payload.top_k)
    result = recommend_movies(payload)
    logger.info("Recommendation completed with %d results", len(result.recommendations))
    return result
