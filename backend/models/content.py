
from pydantic import BaseModel
from datetime import datetime

from models.database import connection, execute, query, safe_format, guid, execute_param


class Content(BaseModel):
    content_id: int = None
    date: str = None
    word: str = None
    quote: str = None
    author: str = None
    category: datetime = None
    difficulty_level: str = None
    created_at: datetime = None

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        if len(args) > 0:
            self.content_id = args[0]
            self.date = args[1]
            self.word = args[2]
            self.quote = args[3]
            self.author = args[4]
            self.category = args[5]
            self.difficulty_level = args[6]
            self.created_at = args[7]

    @classmethod
    def create_table(self):
        sql = """
            CREATE TABLE daily_content (
                content_id character varying(24) PRIMARY KEY,
                date text NOT NULL,
                word text NOT NULL,
                quote text NOT NULL,
                author text NOT NULL,
                category text,
                difficulty_level text,
                created_at TIMESTAMP NOT NULL
            );
        """
        execute(sql)

    @classmethod
    def drop_table(self):
        print(f"Dropping Table")
        sql = """
            DROP TABLE daily_content
        """
        execute(sql)

    @classmethod
    def by_date(self, date):
        sql = f"""
            SELECT * FROM daily_content WHERE date = '{date}'
        """
        ret = query(sql)
        print(f"by_date: {ret}")
        if ret:
            return Content(*ret[0])
        return None

    @classmethod
    def by_content_id(self, content_id):
        sql = f"""
            SELECT * FROM daily_content WHERE content_id = '{content_id}'
        """
        print(sql)
        ret = query(sql)
        return Content(*ret[0])

    def delete(self, cursor):
        if self.content_id is not None:
            sql = f"""
                    DELETE FROM daily_content
                    where content_id = '{self.content_id}'
                """
            execute(sql)

    def save(self):
        print(f"content_id: {self.content_id}")

        if self.content_id is not None:
            print("updating existing content")
            sql = """
                UPDATE daily_content SET
                date = %s,
                word = %s,
                quote = %s,
                author = %s,
                category = %s,
                difficulty_level = %s,
                created_at = %s
                WHERE content_id = %s
            """
            params = (
                self.date,
                self.word,
                self.quote,
                self.author,
                self.category,
                self.difficulty_level,
                self.created_at,
                self.content_id
            )
            execute_param(sql, params)
        else:
            print("creating new content")
            self.content_id = guid()
            
            sql = """
                INSERT INTO daily_content VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s
                )
            """
            params = (
                self.content_id,
                self.date,
                self.word,
                self.quote,
                self.author,
                self.category,
                self.difficulty_level,
                self.created_at
            )
            execute_param(sql, params)
