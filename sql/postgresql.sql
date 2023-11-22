CREATE TABLE IF NOT EXISTS Account(
    account_id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    payment_method VARCHAR(255) NOT NULL,
    blocked BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS Profile(
    profile_id SERIAL PRIMARY KEY,
    account_id INTEGER NOT NULL,
    profile_image VARCHAR(255) NOT NULL DEFAULT 'placeholder.jpeg',
    profile_child BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS Subscription(
    subscription_id SERIAL PRIMARY KEY,
    description VARCHAR(255) NOT NULL,
    subscription_price REAL NOT NULL DEFAULT 7.99    
);

CREATE TABLE IF NOT EXISTS Movie(
    movie_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    duration INTERVAL NOT NULL DEFAULT '00:00:00', 
    genre_id INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS Episode(
    episode_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    duration INTERVAL NOT NULL DEFAULT '00:00:00',
    season_id INTEGER NOT NULL
);