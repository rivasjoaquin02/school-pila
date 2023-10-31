from bson import ObjectId
from fastapi import APIRouter, HTTPException, status

from api.db.schemas.article import ArticleDBSchema, ArticleSchema, UpdatedArticleSchema
from api.models.article_crud import add_article, delete_article, retrieve_article, retrieve_articles, update_article


router = APIRouter()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_description="Retrieves all the Articles",
    response_model=list[ArticleDBSchema],
)
async def get_articles() -> list[ArticleDBSchema]:
    articles_list = await retrieve_articles()
    if len(articles_list) == 0:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT, detail="No Articles to retrieve yet"
        )
    return articles_list


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_description="Retrieves article with matching ID",
    response_model=ArticleDBSchema,
)
async def get_article(id: str):
    article_in_db = await retrieve_article("_id", ObjectId(id))
    if not article_in_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No article with that id"
        )
    return article_in_db


@router.post(
    "/new",
    status_code=status.HTTP_200_OK,
    response_description="Insert new article",
    response_model=ArticleDBSchema,
)
async def add_problem_data(
    article_data: ArticleSchema,
) -> ArticleDBSchema:
    inserted_article = await add_article(article_data)
    if not inserted_article:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="article not added",
        )
    return inserted_article


@router.put(
    "/{id}",
    status_code=status.HTTP_206_PARTIAL_CONTENT,
    response_description="Updates the article info",
    response_model=ArticleDBSchema,
)
async def update_article_data(
    id: str,
    article_data: UpdatedArticleSchema,
):
    print (article_data)
    updated_article = await update_article(id, article_data)
    if not updated_article:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not update article info",
        )
    return updated_article


@router.delete(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_description="Deletes the article with matching ID",
    response_model=ArticleDBSchema,
)
async def delete_article_data(id: str) -> ArticleDBSchema:
    article_in_db = await retrieve_article("_id", ObjectId(id))
    if not article_in_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No article with that id"
        )

    deleted_article = await delete_article(id)
    if not deleted_article:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Could not delete article"
        )
    return deleted_article
