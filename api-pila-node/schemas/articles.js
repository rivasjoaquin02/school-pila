import z from "zod";

const articleSchema = z.object({
	name: z
		.string({
			invalid_type_error: "Article name must be a string",
			required_error: "Article name is required",
		})
		.max(100),
	line: z
		.string({
			invalid_type_error: "Article line must be a string",
			required_error: "Article line is required",
		})
		.max(100),
	brand: z
		.string({
			invalid_type_error: "Article brand must be a string",
			required_error: "Article brand is required",
		})
		.max(100),
});

export function validateArticle(object) {
	return articleSchema.safeParse(object);
}

export function validatePartialArticle(object) {
	return articleSchema.partial().safeParse(object);
}
