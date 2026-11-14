from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator

from router import answer

app = FastAPI(title="Adaptive Search Router", version="0.1.0")


class SearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=300)
    adaptive: bool = True

    @field_validator("query")
    @classmethod
    def nonblank(cls, value):
        if not value.strip():
            raise ValueError("Query must contain non-whitespace characters")
        return value.strip()


@app.post("/search")
def search(request: SearchRequest):
    return answer(request.query, adaptive=request.adaptive).payload()
