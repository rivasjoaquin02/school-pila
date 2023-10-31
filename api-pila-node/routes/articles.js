import { Router } from "express";
import { ArticleController } from "../controllers/articles.js";

export const createArticleRouter = ({ articleModel }) => {
	const articlesRouter = Router();
	const articleController = new ArticleController({ articleModel });

	articlesRouter.get("/", articleController.getAll);
	articlesRouter.get("/:serial_no", articleController.getSerialNo);

	articlesRouter.post("/", articleController.create);
	articlesRouter.patch("/:serial_no", articleController.update);
	articlesRouter.delete("/:serial_no", articleController.delete);

	return articlesRouter;
};
