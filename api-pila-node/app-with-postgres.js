import { createApp } from "./app.js";
import { ArticleModel } from "./models/postgres/article.js";

createApp({ articleModel: ArticleModel });
