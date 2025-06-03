CREATE DATABASE Ludoteca;

use Ludoteca;

CREATE TABLE Usuario(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_ VARCHAR(255) NOT NULL,
    role ENUM('admin', 'user') NOT NULL DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE Stock(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    cantidad INT NOT NULL DEFAULT 0,
    categoria ENUM('Juego de mesa', 'Juego de Cartas', 'Juego de rol') NOT NULL,
    publico_destinado ENUM('Todo público', 'Adultos') NOT NULL,
    precio DECIMAL(10,2) NOT NULL 

);