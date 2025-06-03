CREATE DATABASE Ludoteca;

use Ludoteca;

CREATE TABLE Usuario(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
<<<<<<< Updated upstream
    password_ VARCHAR(50) NOT NULL,
=======
    contraseña VARCHAR(255) NOT NULL,
    role ENUM('admin', 'user') NOT NULL DEFAULT 'user',
>>>>>>> Stashed changes
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
