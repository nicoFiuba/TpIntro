CREATE DATABASE Ludoteca;

use Ludoteca;

CREATE TABLE Usuario(
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password_ VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    role ENUM('admin', 'user') NOT NULL DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE Productos(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    categoria ENUM('Juego de mesa', 'Juego de Cartas', 'Juego de rol', 'Otro') NOT NULL DEFAULT 'Otro',
    publico_destinado ENUM('Todo público', 'Adultos') NOT NULL DEFAULT 'Todo público',
    imagen LONGBLOB
);

CREATE TABLE Pedidos(
    id INT AUTO_INCREMENT PRIMARY KEY,
    idpedido INT NOT NULL,
    usuario VARCHAR(50) NOT NULL,
    producto VARCHAR(100) NOT NULL,
    cantidad INT NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO Usuario (username, password_, email, role) VALUES ('admin', 'admin', 'admin@example.com', 'admin')
