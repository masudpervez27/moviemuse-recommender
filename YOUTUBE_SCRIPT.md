# MovieMuse Recommender - YouTube Transcript Script

## Title
Build a Semantic Movie Recommender with Explainable Ranking (Project 07)

## Intro
In this video we continue the portfolio plan with Project 07, MovieMuse Recommender.

We will implement a real feature slice:
- parse natural-language movie intent,
- score movies against genres and themes,
- filter by year,
- return ranked recommendations with clear reasons.

## Problem
Keyword search is too rigid for movie discovery. People ask things like:
"movies like Inception but more emotional".

We need soft matching and explainability.

## Backend
The backend uses:
- RecommendRequest schema,
- RecommendResponse schema,
- a recommendation service with scoring logic.

The score combines:
- genre overlap,
- tag overlap,
- title/reference overlap,
- mood boosts like emotional, intense, smart.

## Frontend
The frontend sends:
- query,
- top_k,
- year_min/year_max.

Then it renders card results with:
- title and year,
- genres,
- score,
- reason for recommendation.

## Logging
We log request size, top_k, and completion counts in backend.
Frontend logs API failures and bad responses using VITE_LOG_LEVEL.

## Outro
This is a functional recommendation slice and a clean base for adding embeddings, vector DB, and rerankers next.
