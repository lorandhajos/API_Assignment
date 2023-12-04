CREATE TABLE IF NOT EXISTS Subscription(
    subscription_id SERIAL PRIMARY KEY,
    description VARCHAR(255) NOT NULL,
    subscription_price REAL NOT NULL DEFAULT 7.99
);

CREATE TABLE IF NOT EXISTS Account(
    account_id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    payment_method VARCHAR(255) NOT NULL,
    blocked BOOLEAN DEFAULT FALSE,
    login_attempts INTEGER DEFAULT 0,
    last_login DATE,
    subscription_id INTEGER,
    CONSTRAINT fk_subscription
        FOREIGN KEY(subscription_id)
            REFERENCES Subscription(subscription_id)
);

CREATE TABLE IF NOT EXISTS Watchlist(
	watchlist_id SERIAL PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS Genre(
	genre_id SERIAL PRIMARY KEY,
	name VARCHAR(255) NOT NULL,
	age_restriction VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Profile(
    profile_id SERIAL PRIMARY KEY,
    account_id INTEGER NOT NULL,
    profile_image VARCHAR(255) NOT NULL DEFAULT 'placeholder.jpeg',
    profile_child BOOLEAN DEFAULT FALSE,
    age INTEGER,
    language VARCHAR(255) DEFAULT 'English',
    watchlist_id INTEGER NOT NULL,
    history_id INTEGER NOT NULL,
    CONSTRAINT fk_account
        FOREIGN KEY(account_id)
            REFERENCES Account(account_id),
    CONSTRAINT fk_watchlist
        FOREIGN KEY(watchlist_id)
            REFERENCES Watchlist(watchlist_id)
);

CREATE TABLE IF NOT EXISTS Interests(
    profile_id INTEGER NOT NULL,
    genre_id INTEGER NOT NULL,
    CONSTRAINT fk_profile
        FOREIGN KEY(profile_id)
            REFERENCES Profile(profile_id),
    CONSTRAINT fk_genre
        FOREIGN KEY(genre_id)
            REFERENCES Genre(genre_id)
);

CREATE TABLE IF NOT EXISTS Movie(
    movie_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    duration INTERVAL NOT NULL DEFAULT '00:00:00'
);

CREATE TABLE IF NOT EXISTS Series(
    series_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Episode(
    episode_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    duration INTERVAL NOT NULL DEFAULT '00:00:00',
    season_number INTEGER NOT NULL,
    series_id INTEGER NOT NULL,
    CONSTRAINT fk_series
        FOREIGN KEY(series_id)
            REFERENCES Series(series_id)
);

/* Genre stuff */
CREATE TABLE IF NOT EXISTS Movie_genre(
    movie_id INTEGER NOT NULL,
    genre_id INTEGER NOT NULL,
    CONSTRAINT fk_movie
        FOREIGN KEY(movie_id)
            REFERENCES Movie(movie_id),
    CONSTRAINT fk_genre
        FOREIGN KEY(genre_id)
            REFERENCES Genre(genre_id)
);

CREATE TABLE IF NOT EXISTS Series_genre(
    series_id INTEGER NOT NULL,
    genre_id INTEGER NOT NULL,
    CONSTRAINT fk_movie
        FOREIGN KEY(series_id)
            REFERENCES Series(series_id),
    CONSTRAINT fk_genre
        FOREIGN KEY(genre_id)
            REFERENCES Genre(genre_id)
);

/* Watchlist stuff */
CREATE TABLE IF NOT EXISTS Watchlist_movies(
    watchlist_movies_id SERIAL PRIMARY KEY,
    watchlist_id INTEGER NOT NULL,
    movie_id INTEGER NOT NULL,
    CONSTRAINT fk_watchlist
        FOREIGN KEY(watchlist_id)
            REFERENCES Watchlist(watchlist_id),
    CONSTRAINT fk_movie
        FOREIGN KEY(movie_id)
            REFERENCES Movie(movie_id)
);

CREATE TABLE IF NOT EXISTS Watchlist_series(
    watchlist_series_id SERIAL PRIMARY KEY,
    watchlist_id INTEGER NOT NULL,
    series_id INTEGER NOT NULL,
    CONSTRAINT fk_watchlist
        FOREIGN KEY(watchlist_id)
            REFERENCES Watchlist(watchlist_id),
    CONSTRAINT fk_series
        FOREIGN KEY(series_id)
            REFERENCES Series(series_id)
);

/* History stuff */
CREATE TABLE IF NOT EXISTS History(
    history_id SERIAL PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS History_movies(
    history_movies_id SERIAL PRIMARY KEY,
    history_id INTEGER NOT NULL,
    movie_id INTEGER NOT NULL,
    CONSTRAINT fk_history
        FOREIGN KEY(history_id)
            REFERENCES History(history_id),
    CONSTRAINT fk_movie
        FOREIGN KEY(movie_id)
            REFERENCES Movie(movie_id)
);

CREATE TABLE IF NOT EXISTS History_series(
    history_series_id SERIAL PRIMARY KEY,
    history_id INTEGER NOT NULL,
    series_id INTEGER NOT NULL,
    CONSTRAINT fk_history
        FOREIGN KEY(history_id)
            REFERENCES History(history_id),
    CONSTRAINT fk_series
        FOREIGN KEY(series_id)
            REFERENCES Series(series_id)
);