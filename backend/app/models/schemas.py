from pydantic import BaseModel, Field


class RecommendRequest(BaseModel):
    query: str = Field(min_length=5, max_length=400)
    top_k: int = Field(default=5, ge=1, le=10)
    year_min: int | None = Field(default=None, ge=1950, le=2100)
    year_max: int | None = Field(default=None, ge=1950, le=2100)


class MovieRecommendation(BaseModel):
    title: str
    year: int
    genres: list[str]
    score: float
    reason: str


class RecommendResponse(BaseModel):
    query: str
    top_k: int
    recommendations: list[MovieRecommendation]
