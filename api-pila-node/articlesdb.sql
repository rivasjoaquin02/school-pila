DROP DATABASE IF EXISTS articlesdb;
CREATE DATABASE articlesdb;

CREATE TABLE article
(
    serial_no UUID PRIMARY KEY,
    name      VARCHAR(255) NOT NULL,
    line      VARCHAR(255) NOT NULL,
    brand     VARCHAR(255) NOT NULL
);

INSERT INTO article (serial_no, name, line, brand)
VALUES (gen_random_uuid(), 'Air 13', 'Macbook', 'Apple'),
       (gen_random_uuid(), 'iPhone 14', 'Iphone', 'Apple'),
       (gen_random_uuid(), 'Watch 2', 'Watch', 'Apple');


-- SELECT * FROM article
-- INSERT INTO article (serial_no, name, line, brand) VALUES (gen_random_uuid(), 'Air 15', 'Macbook', 'Apple');
