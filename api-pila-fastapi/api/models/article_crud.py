from fastapi import HTTPException, status
from bson import ObjectId

from api.db.database import client
from api.db.schemas.article import (
    ArticleDBSchema,
    ArticleSchema,
    UpdatedArticleSchema,
    map_article_to_dict,
    map_to_article_db_schema,
)

# connection with database
articles_collection = client.articles.get_collection("articles_collection")


async def retrieve_articles() -> list[ArticleDBSchema]:
    articles = []
    async for article in articles_collection.find():
        articles.append(map_to_article_db_schema(article))
    return articles


async def retrieve_article(field: str, key: str | ObjectId) -> ArticleDBSchema | None:
    article_in_db: dict[str, str] = await articles_collection.find_one({field: key})

    if not article_in_db:
        return None

    return map_to_article_db_schema(article_in_db)


def valid_types(article_data: ArticleSchema) -> bool:
    # type validations
    if type(article_data.name) != str:
        return False
    if type(article_data.serial_no) != str:
        return False
    if type(article_data.line) != str:
        return False
    if type(article_data.brand) != str:
        return False
    return True


async def already_exist(article_data: ArticleSchema) -> bool:
    article_in_db = await retrieve_article("serial_no", article_data.serial_no)
    if article_in_db:
        return True
    return False


def is_empty(article_data: UpdatedArticleSchema) -> bool:
    if len(article_data.model_dump().items()) == 0:
        return True
    return False


async def add_article(article_data: ArticleSchema) -> ArticleDBSchema:
    """
    Add a new article to the DB
    """

    if not valid_types(article_data):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect data types",
        )
    if await already_exist(article_data):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Article with the same serial_number already exist",
        )

    normalized_article = map_article_to_dict(article_data)
    inserted_article = await articles_collection.insert_one(normalized_article)
    inserted_id = inserted_article.inserted_id

    article_in_db = await retrieve_article("_id", ObjectId(inserted_id))
    if not article_in_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Article not added",
        )

    return article_in_db


async def update_article(
    id: str, article_data: UpdatedArticleSchema
) -> ArticleDBSchema | None:
    """
    Update a article with matching ID
    """

    # if not valid_types(article_data):
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Incorrect data types",
    #     )
    # if not already_exist(article_data):
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Article with the same serial_number does not exist",
    #     )
    if is_empty(article_data):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="There is nothing to update"
        )

    normalized_article = {
        k: v for k, v in article_data.model_dump().items() if v is not None
    }
    updated_article = await articles_collection.update_one(
        {"_id": ObjectId(id)}, {"$set": normalized_article}
    )

    if updated_article.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No article found with this ID",
        )

    if updated_article.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_304_NOT_MODIFIED,
            detail="The article was not updated",
        )

    article_in_db = await retrieve_article("id", ObjectId(id))
    print(article_in_db)
    if not article_in_db:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Error while updating...",
        )

    return article_in_db


async def delete_article(id: str) -> ArticleDBSchema | None:
    """
    Delete an Article with a matching ID
    """

    article_in_db = await retrieve_article("_id", ObjectId(id))
    if not article_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Article not found"
        )

    deleted_article = await articles_collection.delete_one({"_id": ObjectId(id)})

    if not deleted_article:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Article not deleted"
        )

    return map_to_article_db_schema(deleted_article)
