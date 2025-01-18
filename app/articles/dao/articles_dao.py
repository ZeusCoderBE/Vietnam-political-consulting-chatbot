from app.articles.dto.articles import Articles
import pyodbc

class Articles_Dao:
    def __init__(self, connection_string: str) -> None:
        self.connection_string = connection_string
    def insert_articles(self, article: Articles) -> None:
        try:
            with pyodbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                query = """
                INSERT INTO Articles (links)
                VALUES (?)
                """
                cursor.execute(query, (article.links))
                conn.commit()
                print("Article inserted successfully.")
        except pyodbc.Error as e:
            print(f"An error occurred: {e}")
