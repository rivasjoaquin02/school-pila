import { error } from "console";
import { articles } from "../lib/placeholder-data";

async function seedArticles(client) {
	try {
		const createDB = await client.sql`
            CREATE DATABASE IF NOT EXISTS articlesdb;
        `;
		console.log(`Created database "articlesdb"`);

		const createTable = await client.sql`
            CREATE TABLE IF NOT EXISTS article (
                serial_no UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
                name      VARCHAR(255) NOT NULL,
                line      VARCHAR(255) NOT NULL,
                brand     VARCHAR(255) NOT NULL UNIQUE
            );
        `;
		console.log(`Created table "article"`);

		const insertedArticles = await Promise.all(
			articles.map(
				async (article) => client.sql`
                INSERT INTO article (name, line, brand)
                VALUES (${article.name}, ${article.line}, ${article.brand})
                ON CONFLICT (serial_id) DO NOTHING;
            `
			)
		);
		console.log(`Seeded ${articles.length} articles`);

		return {
			createDB,
			createTable,
			articles: insertedArticles,
		};
	} catch (err) {
		console.error("Error seeding articles: ", error);
		throw error;
	}
}

async function main(client) {
	await seedArticles(client);

	await client.end();
}

main().catch((err) => {
	console.error(
		"An error occurred while attempting to seed the database:",
		err
	);
});
