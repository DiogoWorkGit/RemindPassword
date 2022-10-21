CREATE TABLE gensen (
    id int PRIMARY KEY NOT NULL AUTO_INCREMENT,
	usuario varchar(50) NOT NULL,
	pass varchar(100) NOT NULL,
	email varchar(100),
    tipo varchar(5) NOT NULL,
	nome varchar(100) NOT NULL,
	url varchar(200),
	data_creation varchar(21) NOT NULL
)

