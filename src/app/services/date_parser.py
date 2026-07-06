from dateparser import parse
from datetime import date

languages = [
    "en"
]  # TODO: change to be a variable in .env file and load the languages variable from there

# settings = {
#     "PREFER_DATES_FROM": "future",
#     "PREFER_DAY_OF_MONTH": "first",
# }


def parse_date(raw_date: str) -> date | None:
    if not raw_date:
        return None

    parsed_date = parse(
        raw_date,
        languages=languages,
        settings={"PREFER_DATES_FROM": "future", "PREFER_DAY_OF_MONTH": "first"},
    )

    if parsed_date is None:
        return None

    return parsed_date.date()
