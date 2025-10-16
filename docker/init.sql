-- Cria tabelas compatíveis com data.py
CREATE TABLE IF NOT EXISTS users (
  username VARCHAR(100) PRIMARY KEY,
  password VARCHAR(200) NOT NULL,
  name VARCHAR(100),
  email VARCHAR(100),
  photo_path VARCHAR(255),
  user_type VARCHAR(20) DEFAULT 'student'
);

CREATE TABLE IF NOT EXISTS etecs (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  city VARCHAR(100),
  photo_path VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS ratings (
  id SERIAL PRIMARY KEY,
  etec_id INT NOT NULL REFERENCES etecs(id) ON DELETE CASCADE,
  username VARCHAR(100) REFERENCES users(username),
  stars SMALLINT CHECK (stars >= 0 AND stars <= 5),
  comment TEXT,
  date TIMESTAMPTZ DEFAULT now()
);

-- Dados de exemplo baseados em etecs.json
INSERT INTO etecs(id, name, city, photo_path) VALUES
(1, 'ETEC de São Paulo', 'São Paulo', 'images/etecs/etec_1.jpg'),
(2, 'ETEC de Campinas', 'Campinas', 'images/etecs/etec_2.jpg'),
(3, 'ETEC de Santos', 'Santos', 'images/etecs/etec_3.jpg'),
(4, 'ETEC de Ribeirão Preto', 'Ribeirão Preto', 'images/etecs/etec_4.jpg'),
(5, 'ETEC de São José dos Campos', 'São José dos Campos', 'images/etecs/etec_5.jpg');

-- Usuários de exemplo
INSERT INTO users(username, password, name, email, user_type) VALUES
('demo', 'demo123', 'Usuário Demo', 'demo@example.com', 'student'),
('admin', 'admin123', 'Administrador', 'admin@example.com', 'teacher');

-- Avaliações de exemplo
INSERT INTO ratings(etec_id, username, stars, comment) VALUES
(1, 'demo', 5, 'Ótima infraestrutura'),
(2, NULL, 4, 'Bom atendimento'),
(3, 'demo', 3, 'Precisa melhorar equipamentos');
