from models.content import Content
from fastapi import APIRouter
from datetime import datetime

from models.database import query

router = APIRouter()

@router.get("/get_word_history")
async def get_word_history() -> dict:
    sql = f"""
        SELECT word
        FROM (
            SELECT DISTINCT ON (word) word, created_at
            FROM daily_content
            WHERE created_at >= current_date - INTERVAL '30 days'
            ORDER BY word, created_at DESC
        ) AS subquery
        ORDER BY created_at DESC;
    """
    ret = query(sql)
    word_list = [word[0] for word in ret]
    
    print(f"get_word_history: {word_list}")

    if ret:
        return {'word_history': word_list}

@router.get("/get_content")
async def get_content(date: str) -> dict:
    print(f"Getting content for {date}")

    content = Content.by_date(date)

    if content is None:
        return {"quote": None, "author": None, "word": None}

    return {
            "content_id": content.content_id,
            "date": content.date,
            "word": content.word,
            "quote": content.quote,
            "author": content.author,
            "category": content.category,
            "difficulty_level": content.difficulty_level
        }

@router.post("/save_content")
async def save_content(date:str, word:str, quote:str, author:str) -> dict:
    print(f"Saving content for {date}")

    content = Content.by_date(date)

    if content: # updating existing entry
        content.date = date
        content.word = word
        content.quote = quote
        content.author = author
        content.save()
    else: # creating new entry
        content = Content()
        content.created_at = datetime.now()
        content.date = date
        content.word = word
        content.quote = quote
        content.author = author
        content.save()

    return {"status": "ok", "code": 200}
