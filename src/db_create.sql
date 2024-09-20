CREATE TABLE product (
	id_product int NOT NULL,
	asin varchar(10) NOT NULL UNIQUE,
	title varchar(460),
	product_group varchar(13),
	salesrank int,
	review_total int DEFAULT 0,
	review_downloaded int DEFAULT 0,
	review_avg float DEFAULT 0.0,
	PRIMARY KEY (id_product)
);

CREATE TABLE similar_products (
	product_asin varchar(10) NOT NULL,
	similar_asin varchar(10) NOT NULL,
	PRIMARY KEY (product_asin, similar_asin),
	FOREIGN KEY (product_asin) REFERENCES product(asin)
);

CREATE TABLE category (
	id_category int NOT NULL,
	name varchar(60),
	id_parent int,
	PRIMARY KEY (id_category),
	FOREIGN KEY (id_parent) REFERENCES category(id_category)
);

CREATE TABLE product_category (
	id_product int NOT NULL,
	id_category int NOT NULL,
	PRIMARY KEY (id_product, id_category),
	FOREIGN KEY (id_product) REFERENCES product(id_product),
	FOREIGN KEY (id_category) REFERENCES category(id_category)
);

CREATE TABLE review (
	id_product int NOT NULL,
	id_customer varchar(15) NOT NULL,
	review_date date NOT NULL,
	rating int DEFAULT 0,
	votes int DEFAULT 0,
	helpful int DEFAULT 0,
	FOREIGN KEY (id_product) REFERENCES product(id_product)
);