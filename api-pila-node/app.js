import express, { json } from "express";
import { corsMiddleware } from "./middlewares/cors.js";
import { createArticleRouter } from "./routes/articles.js";
import "dotenv/config";

export const createApp = ({ articleModel }) => {
	const app = express();
	app.disable("x-powered-by");

	// middlewares
	app.use(json()); // for parsing json body
	app.use(corsMiddleware({ acceptedOrigins: ["http://localhost:8000"] })); // for CORS

	// routes
	app.get("/", (req, res) => {
		res.json({ message: "👋 api created by strange-devel" });
	});
	app.use("/article", createArticleRouter({ articleModel }));

	const PORT = process.env.PORT ?? 3000;
	app.listen(PORT, () => {
		console.log(`server listen on port http://localhost:${PORT}`);
	});
};
