import logging
import re

from ..models.schemas import MovieRecommendation, RecommendRequest, RecommendResponse

logger = logging.getLogger(__name__)

MOVIES = [
    {
        "title": "Inception",
        "year": 2010,
        "genres": ["sci-fi", "thriller"],
        "tags": ["dream", "mind-bending", "heist", "intense", "smart"],
    },
    {
        "title": "Interstellar",
        "year": 2014,
        "genres": ["sci-fi", "drama"],
        "tags": ["space", "emotional", "epic", "thoughtful", "family"],
    },
    {
        "title": "The Dark Knight",
        "year": 2008,
        "genres": ["action", "crime", "drama"],
        "tags": ["dark", "intense", "hero", "smart", "psychological"],
    },
    {
        "title": "Arrival",
        "year": 2016,
        "genres": ["sci-fi", "drama"],
        "tags": ["linguistics", "slow-burn", "emotional", "thoughtful"],
    },
    {
        "title": "Blade Runner 2049",
        "year": 2017,
        "genres": ["sci-fi", "drama", "thriller"],
        "tags": ["visual", "atmospheric", "slow", "philosophical"],
    },
    {
        "title": "The Social Network",
        "year": 2010,
        "genres": ["drama", "biography"],
        "tags": ["startup", "dialogue", "fast-paced", "intense"],
    },
    {
        "title": "Everything Everywhere All at Once",
        "year": 2022,
        "genres": ["sci-fi", "action", "comedy", "drama"],
        "tags": ["multiverse", "creative", "emotional", "chaotic"],
    },
    {
        "title": "Whiplash",
        "year": 2014,
        "genres": ["drama", "music"],
        "tags": ["intense", "driven", "performance", "psychological"],
    },
    {
        "title": "Parasite",
        "year": 2019,
        "genres": ["thriller", "drama"],
        "tags": ["social", "dark", "smart", "twist"],
    },
    {
        "title": "Her",
        "year": 2013,
        "genres": ["sci-fi", "romance", "drama"],
        "tags": ["emotional", "intimate", "future", "thoughtful"],
    },
]


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-zA-Z][a-zA-Z0-9-]*", text.lower()))


def _score_movie(movie: dict, query_tokens: set[str]) -> tuple[float, str]:
    genre_overlap = len(set(movie["genres"]) & query_tokens)
    tag_overlap = len(set(movie["tags"]) & query_tokens)
    title_overlap = len(_tokens(movie["title"]) & query_tokens)

    score = genre_overlap * 2.4 + tag_overlap * 1.7 + title_overlap * 2.0

    if "emotional" in query_tokens and "emotional" in movie["tags"]:
        score += 1.5
    if "intense" in query_tokens and "intense" in movie["tags"]:
        score += 1.2
    if "smart" in query_tokens and "smart" in movie["tags"]:
        score += 1.2

    reason_bits: list[str] = []
    if genre_overlap:
        reason_bits.append("genre match")
    if tag_overlap:
        reason_bits.append("theme match")
    if title_overlap:
        reason_bits.append("title/reference match")

    reason = ", ".join(reason_bits) if reason_bits else "closest semantic match from catalog"
    return score, reason


def recommend_movies(payload: RecommendRequest) -> RecommendResponse:
    query_tokens = _tokens(payload.query)
    logger.info("Scoring movie recommendations for %d query tokens", len(query_tokens))

    candidates = MOVIES
    if payload.year_min is not None:
        candidates = [m for m in candidates if m["year"] >= payload.year_min]
    if payload.year_max is not None:
        candidates = [m for m in candidates if m["year"] <= payload.year_max]

    scored: list[MovieRecommendation] = []
    for movie in candidates:
        score, reason = _score_movie(movie, query_tokens)
        scored.append(
            MovieRecommendation(
                title=movie["title"],
                year=movie["year"],
                genres=movie["genres"],
                score=round(score, 3),
                reason=reason,
            )
        )

    scored.sort(key=lambda x: x.score, reverse=True)
    recommendations = scored[: payload.top_k]

    return RecommendResponse(
        query=payload.query,
        top_k=payload.top_k,
        recommendations=recommendations,
    )
