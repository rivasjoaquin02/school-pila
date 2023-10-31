from fastapi import Query
from pydantic import BaseModel, Field


# schemas
class ArticleSchema(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    serial_no: str = Field(..., min_length=3, max_length=50)
    # derivate field from catalog
    line: str = Field(..., min_length=3, max_length=50)
    brand: str

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Macbook Pro 16",
                "serial_no": "1234",
                "line": "Macbook",
                "brand": "Apple",
            }
        }


class ArticleDBSchema(ArticleSchema):
    id: str


class UpdatedArticleSchema(BaseModel):
    name: str | None = None
    serial_no: str | None = None
    line: str | None = None
    brand: str | None = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Macbook Air",
            }
        }


# helpers
def map_to_article_db_schema(article: dict) -> ArticleDBSchema:
    return ArticleDBSchema(
        id=str(article["_id"]),
        name=str(article["name"]),
        serial_no=str(article["serial_no"]),
        line=str(article["line"]),
        brand=str(article["brand"]),
    )


def map_article_to_dict(article: ArticleSchema) -> dict:
    return {
        "name": article.name,
        "serial_no": article.serial_no,
        "line": article.line,
        "brand": article.brand,
    }
