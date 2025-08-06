CREATE DATABASE IF NOT EXISTS quiz_app2;

USE quiz_app2;

-- Drop tables if they exist
DROP TABLE IF EXISTS answers1;
DROP TABLE IF EXISTS questions1;
DROP TABLE IF EXISTS users1;

-- Users table
CREATE TABLE users1 (
id INT AUTO_INCREMENT PRIMARY KEY,
email VARCHAR(255) UNIQUE NOT NULL,
password VARCHAR(255) NOT NULL,
registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Questions table
CREATE TABLE questions1 (
id INT AUTO_INCREMENT PRIMARY KEY,
question TEXT NOT NULL,
option_a VARCHAR(255) NOT NULL,
option_b VARCHAR(255) NOT NULL,
option_c VARCHAR(255) NOT NULL,
option_d VARCHAR(255) NOT NULL,
correct_ans CHAR(1) NOT NULL -- 'A', 'B', 'C', or 'D'
);

-- User answers table
CREATE TABLE answers1 (
id INT AUTO_INCREMENT PRIMARY KEY,
user_id INT,
question_id INT,
selected_option CHAR(1),
is_correct BOOLEAN,
answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (user_id) REFERENCES users1(id),
FOREIGN KEY (question_id) REFERENCES questions1(id)
);

ALTER TABLE users1 ADD COLUMN is_admin BOOLEAN DEFAULT FALSE;
UPDATE users1 SET is_admin = TRUE WHERE email = 'admin@g.com';
INSERT INTO users1 (email, password, is_admin) VALUES ('admin@g.com', 'admin123', TRUE);