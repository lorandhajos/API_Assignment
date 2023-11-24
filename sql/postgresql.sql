CREATE TABLE IF NOT EXISTS Account(
    account_id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    payment_method VARCHAR(255) NOT NULL,
    blocked BOOLEAN DEFAULT FALSE,
    login_attempts INTEGER DEFAULT 0,
    last_login DATE
);

CREATE TABLE IF NOT EXISTS Profile(
    profile_id SERIAL PRIMARY KEY,
    account_id INTEGER NOT NULL,
    profile_image VARCHAR(255) NOT NULL DEFAULT 'placeholder.jpeg',
    profile_child BOOLEAN DEFAULT FALSE,
    age INTEGER,
    LANGUAGE VARCHAR(255) DEFAULT 'English',
    watchlist_id INTEGER NOT NULL,
    CONSTRAINT
    FOREIGN KEY(watchlist_id)
    REFERENCES(WatchList)
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
    genre_id INTEGER NOT NULL,
    number_watch INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS Episode(
    episode_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    duration INTERVAL NOT NULL DEFAULT '00:00:00',
    season_id INTEGER NOT NULL,
    series_id INTEGER NOT NULL

    CONSTRAINT series_id
    FOREIGN KEY(series_id)
    REFERENCES(Series)
);

CREATE TABLE IF NOT EXISTS Series(
    series_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Genere(
	genere_id SERIAL PRIMARY KEY,
	genere_name VARCHAR(255) NOT NULL,
	age_restriction VARCHAR(255) NOT NULL,

    CONSTRAINT age_restriction
    FOREIGN KEY(restriction_name)
    REFERENCES(AgeRestriction)
);

CREATE TABLE IF NOT EXISTS WatchList(
	watchlist_id SERIAL PRIMARY KEY,
	
);

CREATE TABLE IF NOT EXISTS AgeRestriction(
	restriction_id SERIAL PRIMARY KEY,
	restriction_name VARCHAR(255) NOT NULL
);