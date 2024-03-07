DROP DATABASE IF EXISTS revou_review;
CREATE DATABASE revou_product_review;
USE revou_product_review;

CREATE TABLE produk (
	produk_id INTEGER PRIMARY KEY auto_increment,
    nama_produk VARCHAR(100) NOT NULL,
    harga_produk INTEGER NOT NULL,
    deskripsi TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE product_review (
	id INTEGER PRIMARY KEY auto_increment,
    product_id INTEGER NOT NULL,
    email VARCHAR(100) NOT NULL,
    rating INTEGER NOT NULL,
    review_content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);