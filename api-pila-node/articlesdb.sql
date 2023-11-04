DROP DATABASE IF EXIST  articlesdb;
CREATE DATABASE IF NOT EXISTS articlesdb;

CREATE TABLE IF NOT EXISTS article (
    serial_no UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    name      VARCHAR(255) NOT NULL,
    line      VARCHAR(255) NOT NULL,
    brand     VARCHAR(255) NOT NULL UNIQUE
);

INSERT INTO article (name, line, brand)
VALUES ('Air 13', 'Macbook', 'Apple'),
       ('iPhone 14', 'Iphone', 'Apple'),
       ('Watch 2', 'Watch', 'Apple');


-- SELECT * FROM article
-- INSERT INTO article (serial_no, name, line, brand) VALUES (gen_random_uuid(), 'Air 15', 'Macbook', 'Apple');
