from dateparser import parse, _Settings
from datetime import datetime
from fastapi import HTTPException

languages = [
    "en"
]  # TODO: change to be a variable in .env file and load the languages variable from there

settings: _Settings = {
    "PREFER_DATES_FROM": "future",
    "PREFER_DAY_OF_MONTH": "first",
}


def parse_date(raw_date: str) -> datetime | None:
    if not raw_date:
        raise HTTPException(
            status_code=400, detail="Due date cannot be an empty string"
        )

    return parse(raw_date, languages=languages, settings=settings)
