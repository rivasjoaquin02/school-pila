import postgres from "postgres";

const DEFAULT_CONFIG = {
	host: "localhost",
	user: process.env.POSTGRES_USER ?? "postgres",
	password: process.env.POSTGRES_PASSWORD ?? "1234",
	database: process.env.POSTGRES_DB ?? "articlesdb",
	port: process.env.POSTGRES_PORT ?? 5432,
};

const sql = postgres(process.env.POSTGRES_URI ?? DEFAULT_CONFIG);

export class ArticleModel {
	static async getAll({ name, line, brand }) {
		const articles = await sql`SELECT * FROM article`;

		let filteredArticles = articles;

		if (name)
			filteredArticles = filteredArticles.filter((article) =>
				article.name.toLowerCase().includes(name.toLowerCase())
			);

		if (line)
			filteredArticles = filteredArticles.filter((article) =>
				article.line.toLowerCase().includes(line.toLowerCase())
			);

		if (brand)
			filteredArticles = filteredArticles.filter((article) =>
				article.brand.toLowerCase().includes(brand.toLowerCase())
			);

		return filteredArticles;
	}

	static async getSerialNo({ serial_no }) {
		const article =
			await sql`SELECT * FROM article WHERE serial_no = ${serial_no}`;
		return article;
	}
	static async create({ input }) {
		const { name, line, brand } = input;

		// check if exist first
		const articleAlreadyInDb = await this.getAll({ name, line, brand });
		if (articleAlreadyInDb)
			return { success: false, error: "Article already exist" };

		const [{ uuid: serial_no }] = await sql`SELECT gen_random_uuid() uuid;`;
		await sql`
            INSERT INTO
            article (serial_no, name, line, brand)
            VALUES (${serial_no}, ${name}, ${line}, ${brand});
        `;

		const article = await this.getSerialNo({ serial_no });
		return { success: true, data: article[0] };
	}
	static async delete({ serial_no }) {
		const res =
			await sql`DELETE FROM article WHERE serial_no = ${serial_no}`;
		return res;
	}
	static async update({ serial_no, input }) {
		const [originalArticle] = await this.getSerialNo({ serial_no });

		const updatedArticle = {
			...originalArticle,
			...input,
		};

		const { name, line, brand } = updatedArticle;
		await sql`
            UPDATE article
            SET name  = ${name},
                line  = ${line},
                brand = ${brand}
            WHERE serial_no = ${serial_no}
        `;

		return updatedArticle;
	}
}
