import {
	validateArticle,
	validatePartialArticle,
} from "../schemas/articles.js";

export class ArticleController {
	constructor({ articleModel }) {
		this.articleModel = articleModel;
	}

	getAll = async (req, res) => {
		const { name, line, brand } = req.query;
		const articles = await this.articleModel.getAll({ name, line, brand });
		res.json(articles);
	};

	getSerialNo = async (req, res) => {
		const { serial_no } = req.params;
		const article = await this.articleModel.getSerialNo({ serial_no });

		if (!article) res.status(404).json({ message: "Article not found" });

		return res.json(article);
	};

	create = async (req, res) => {
		const result = validateArticle(req.body);

		if (result.error)
			return res
				.status(422)
				.json({ error: JSON.parse(result.error.message) });

		const response = await this.articleModel.create({
			input: result.data,
		});

		if (!response.success)
			return res.status(400).json({ error: response.error });
		
		res.status(201).json(newArticle);
	};

	update = async (req, res) => {
		const result = validatePartialArticle(req.body);

		if (result.error)
			return res
				.status(422)
				.json({ error: JSON.parse(result.error.message) });

		const { serial_no } = req.params;
		const updatedArticle = await this.articleModel.update({
			serial_no,
			input: result.data,
		});

		return res.json(updatedArticle);
	};

	delete = async (req, res) => {
		const { serial_no } = req.params;

		const result = await this.articleModel.delete({ serial_no });

		if (!result)
			return res.status(404).json({ message: "Article not found" });

		return res.json({ message: "Article deleted " });
	};
}
