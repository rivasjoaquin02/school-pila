from fastapi import FastAPI
from api.routes.article import router as ArticleRouter

# env = dotenv_values(".env")


app = FastAPI()
app.include_router(ArticleRouter, tags=["Article"], prefix="/article")


@app.get("/", tags=["Root"])
async def root():
    return {"message", "my exam"}
