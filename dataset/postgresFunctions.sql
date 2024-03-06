CREATE OR REPLACE FUNCTION getWatchlistFilmsForID(filmID int)
RETURNS TABLE(movie_id integer) AS
$$
   BEGIN
     RETURN QUERY SELECT watchlist_movies.movie_id FROM watchlist_movies WHERE watchlist_movies.watchlist_id = filmID;
   END;
$$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION getWatchlistSeriesForID(seriesID int)
RETURNS TABLE(series_id integer) AS
$$
   BEGIN
     RETURN QUERY SELECT watchlist_series.series_id FROM watchlist_series WHERE watchlist_series.watchlist_id = seriesID;
   END;
$$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION getHistoryMoviesForID(historyID int)
RETURNS TABLE(movie_id integer) AS
$$
   BEGIN
     RETURN QUERY SELECT history_movies.movie_id FROM history_movies WHERE history_movies.history_id = historyID;
   END;
$$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION getHistorySeriesForID(historyID int)
RETURNS TABLE(series_id integer) AS
$$
   BEGIN
     RETURN QUERY SELECT history_series.series_id FROM history_series WHERE history_series.history_id = historyID;
   END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION getAgeProfile(profileID int)
RETURNS TABLE(age integer) AS
$$
   BEGIN
     RETURN QUERY SELECT profile.age FROM profile WHERE profile_id = profileID;
   END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION getAgeRestrictorFilms(filmID int)
RETURNS TABLE(ageRestrictor integer) AS
$$
   BEGIN
     RETURN QUERY SELECT genre.age_restriction FROM genre INNER JOIN movie_genre ON genre.genre_id = movie_genre.genre_id WHERE movie_id = filmID;
   END;
$$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION getAgeRestrictorSeries(seriesID int)
RETURNS TABLE(ageRestrictor integer) AS
$$
   BEGIN
     RETURN QUERY SELECT genre.age_restriction FROM genre INNER JOIN series_genre ON genre.genre_id = series_genre.genre_id WHERE series_id = seriesID;
   END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION login(e_email VARCHAR, p_password VARCHAR)
RETURNS TABLE(accountID integer) AS
$$
   BEGIN
     RETURN QUERY SELECT account.account_id FROM account WHERE email = e_email AND password = p_password;
   END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION getMovieNames()
RETURNS TABLE(title VARCHAR) AS
$$
   BEGIN
     RETURN QUERY SELECT movie.title FROM movie ORDER BY movie.movie_id;
   END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION getMovieViews()
RETURNS TABLE(views integer) AS
$$
   BEGIN
     RETURN QUERY SELECT movie.views FROM movie ORDER BY movie.movie_id;
   END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION getSeriesTitle()
RETURNS TABLE(title VARCHAR) AS
$$
   BEGIN
     RETURN QUERY SELECT series.title FROM series;
   END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION getSeriesViews()
RETURNS TABLE(views integer) AS
$$
   BEGIN
     RETURN QUERY SELECT series.views FROM series;
   END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION getNOfUsersPerCountry()
RETURNS TABLE(count integer) AS
$$
   BEGIN
     RETURN QUERY SELECT COUNT(profile.country)::int FROM profile GROUP BY profile.country;
   END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION getUsersCountry()
RETURNS TABLE(country VARCHAR) AS
$$
   BEGIN
     RETURN QUERY SELECT profile.country FROM profile GROUP BY profile.country;
   END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE inputInterest(
  IN p_profileID integer,
  IN p_genre_id integer
)
LANGUAGE plpgsql
AS $$
BEGIN
  INSERT INTO interests (profile_id, genre_id)
  VALUES (p_profileID, p_genre_id);
END;
$$;

/*From here CRUD beggins*/

/*profile watchlist*/

/*movies*/
CREATE OR REPLACE PROCEDURE createWatchlistMoviesElement(
  IN p_watchlist_movies_id integer,
  IN p_watchlist_id integer,
  IN p_movie_id integer
)
LANGUAGE plpgsql
AS $$
BEGIN
  INSERT INTO watchlist_movies (watchlist_movies_id, watchlist_id, movie_id)
  VALUES (p_watchlist_movies_id, p_watchlist_id, p_movie_id);
END;
$$;

CREATE VIEW selectWatchlistMovies AS
SELECT * FROM watchlist_movies;

CREATE OR REPLACE PROCEDURE updateWatchlistMoviesElement(
  IN p_watchlist_movies_id integer,
  IN p_watchlist_id integer,
  IN p_movie_id integer
)
LANGUAGE plpgsql
AS $$
BEGIN
  UPDATE watchlist_movies
  SET watchlist_id = p_watchlist_id, movie_id = p_movie_id
  WHERE watchlist_movies_id = p_watchlist_movies_id;
END;
$$;

CREATE OR REPLACE PROCEDURE deleteWatchlistMoviesElement(
  IN p_watchlist_movies_id integer
)
LANGUAGE plpgsql
AS $$
BEGIN
  DELETE FROM watchlist_movies WHERE watchlist_movies_id = p_watchlist_movies_id;
END;
$$;

/*series*/
CREATE OR REPLACE PROCEDURE createWatchlistSeriesElement(
  IN p_watchlist_series_id integer,
  IN p_watchlist_id integer,
  IN p_series_id integer
)
LANGUAGE plpgsql
AS $$
BEGIN
  INSERT INTO watchlist_series (watchlist_series_id, watchlist_id, series_id)
  VALUES (p_watchlist_series_id, p_watchlist_id, p_series_id);
END;
$$;

CREATE VIEW selectWatchlistSeries AS
SELECT * FROM watchlist_series;

CREATE OR REPLACE PROCEDURE updateWatchlistSeriesElement(
  IN p_watchlist_series_id integer,
  IN p_watchlist_id integer,
  IN p_series_id integer
)
LANGUAGE plpgsql
AS $$
BEGIN
  UPDATE watchlist_series
  SET watchlist_id = p_watchlist_id, series_id = p_series_id
  WHERE watchlist_series_id = p_watchlist_series_id;
END;
$$;

CREATE OR REPLACE PROCEDURE deleteWatchlistSeriesElement(
  IN p_watchlist_series_id integer
)
LANGUAGE plpgsql
AS $$
BEGIN
  DELETE FROM watchlist_series WHERE watchlist_series_id = p_watchlist_series_id;
END;
$$;

/*history movies*/
CREATE OR REPLACE PROCEDURE createHistoryMoviesElement(
  IN p_history_movies_id integer,
  IN p_history_id integer,
  IN p_movie_id integer,
  IN p_status_finished boolean,
  IN p_status_time interval
)
LANGUAGE plpgsql
AS $$
BEGIN
  INSERT INTO history_movies (history_movies_id, history_id, movie_id, status_finished, status_time)
  VALUES (p_history_movies_id, p_history_id, p_movie_id, p_status_finished, p_status_time);
END;
$$;

CREATE VIEW selectHistoryMovies AS
SELECT * FROM history_movies;

CREATE OR REPLACE PROCEDURE updateHistoryMoviesElement(
  IN p_history_movies_id integer,
  IN p_history_id integer,
  IN p_movie_id integer,
  IN p_status_finished boolean,
  IN p_status_time interval
)
LANGUAGE plpgsql
AS $$
BEGIN
  UPDATE history_movies
  SET history_id = p_history_id, movie_id = p_movie_id, status_finished = p_status_finished, status_time = p_status_time
  WHERE history_movies_id = p_history_movies_id;
END;
$$;

CREATE OR REPLACE PROCEDURE deleteHistoryMoviesElement(
  IN p_history_movies_id integer
)
LANGUAGE plpgsql
AS $$
BEGIN
  DELETE FROM history_movies WHERE history_movies_id = p_history_movies_id;
END;
$$;

/*series*/

CREATE OR REPLACE PROCEDURE createHistorySeriesElement(
  IN p_history_series_id integer,
  IN p_history_id integer,
  IN p_series_id integer
)
LANGUAGE plpgsql
AS $$
BEGIN
  INSERT INTO history_series (history_series_id, history_id, series_id)
  VALUES (p_history_series_id, p_history_id, p_series_id);
END;
$$;

CREATE VIEW selectHistorySeries AS
SELECT * FROM history_series;

CREATE OR REPLACE PROCEDURE updateHistorySeriesElement(
  IN p_history_series_id integer,
  IN p_history_id integer,
  IN p_series_id integer
)
LANGUAGE plpgsql
AS $$
BEGIN
  UPDATE history_series
  SET history_id = p_history_id, series_id = p_series_id
  WHERE history_series_id = p_history_series_id;
END;
$$;

CREATE OR REPLACE PROCEDURE deleteHistorySeriesElement(
  IN p_history_series_id integer
)
LANGUAGE plpgsql
AS $$
BEGIN
  DELETE FROM history_series WHERE history_series_id = p_history_series_id;
END;
$$;

/*Interests*/

CREATE OR REPLACE PROCEDURE createInterestElement(
  IN p_profile_id integer,
  IN p_genre_id integer
)
LANGUAGE plpgsql
AS $$
BEGIN
  INSERT INTO interests (profile_id, genre_id)
  VALUES (p_profile_id, p_genre_id);
END;
$$;

CREATE VIEW selectInterests AS
SELECT * FROM interests;

CREATE OR REPLACE PROCEDURE updateInterestElement(
  IN p_profile_id integer,
  IN p_genre_id integer,
  IN p_desired_genre_id integer
)
LANGUAGE plpgsql
AS $$
BEGIN
  UPDATE interests
  SET genre_id = p_desired_genre_id
  WHERE profile_id = p_profile_id AND genre_id = p_genre_id;
END;
$$;

CREATE OR REPLACE PROCEDURE deleteInterestElement(
  IN p_profile_id integer,
  IN p_genre_id integer
)
LANGUAGE plpgsql
AS $$
BEGIN
  DELETE FROM interests WHERE profile_id = p_profile_id AND genre_id = p_genre_id;
END;
$$;

/*calss genre movies*/

CREATE OR REPLACE PROCEDURE createGenreMoviesElement(
  IN p_genre_id integer,
  IN p_movie_id integer
)
LANGUAGE plpgsql
AS $$
BEGIN
  INSERT INTO movie_genre (genre_id, movie_id)
  VALUES (p_genre_id, p_movie_id);
END;
$$;

CREATE VIEW selectMoviesGenre AS
SELECT * FROM movie_genre;

CREATE OR REPLACE PROCEDURE updateMovieGenreElement(
  IN p_genre_id integer,
  IN p_movie_id integer,
  IN p_desired_genre_id integer
)
LANGUAGE plpgsql
AS $$
BEGIN
  UPDATE movie_genre
  SET genre_id = p_desired_genre_id
  WHERE genre_id = p_genre_id AND movie_id = p_movie_id;
END;
$$;

CREATE OR REPLACE PROCEDURE deleteMoviesGenreElement(
  IN p_genre_id integer,
  IN p_movie_id integer
)
LANGUAGE plpgsql
AS $$
BEGIN
  DELETE FROM movie_genre WHERE genre_id = p_genre_id AND movie_id = p_movie_id;
END;
$$;

/*series*/

CREATE OR REPLACE PROCEDURE createGenreSeriesElement(
  IN p_genre_id integer,
  IN p_series_id integer
)
LANGUAGE plpgsql
AS $$
BEGIN
  INSERT INTO series_genre (genre_id, series_id)
  VALUES (p_genre_id, p_series_id);
END;
$$;

CREATE VIEW selectseriesGenre AS
SELECT * FROM series_genre;

CREATE OR REPLACE PROCEDURE updateSeriesGenreElement(
  IN p_genre_id integer,
  IN p_series_id integer,
  IN p_desired_genre_id integer
)
LANGUAGE plpgsql
AS $$
BEGIN
  UPDATE series_genre
  SET genre_id = p_desired_genre_id
  WHERE genre_id = p_genre_id AND series_id = p_series_id;
END;
$$;

CREATE OR REPLACE PROCEDURE deleteSeriesGenreElement(
  IN p_genre_id integer,
  IN p_series_id integer
)
LANGUAGE plpgsql
AS $$
BEGIN
  DELETE FROM series_genre WHERE genre_id = p_genre_id AND series_id = p_series_id;
END;
$$;

/*class subscription*/

CREATE OR REPLACE PROCEDURE createSubscriptionElement(
  IN p_subscription_id integer,
  IN p_description VARCHAR,
  IN p_price real
)
LANGUAGE plpgsql
AS $$
BEGIN
  INSERT INTO subscription (subscription_id, description, subscription_price)
  VALUES (p_subscription_id, p_description, p_price);
END;
$$;

CREATE VIEW selectSubscription AS
SELECT * FROM subscription;

CREATE OR REPLACE PROCEDURE updateUbscriptionElement(
  IN p_subscription_id integer,
  IN p_description VARCHAR,
  IN p_price real
)
LANGUAGE plpgsql
AS $$
BEGIN
  UPDATE subscription
  SET subscription_id = p_subscription_id, description = p_description, subscription_price = p_price
  WHERE subscription_id = p_subscription_id;
END;
$$;

CREATE OR REPLACE PROCEDURE deleteSubscriptionElement(
  IN p_subscription_id integer
)
LANGUAGE plpgsql
AS $$
BEGIN
  DELETE FROM subscription WHERE subscription_id = p_subscription_id;
END;
$$;

/*class movies*/

CREATE OR REPLACE PROCEDURE createMovieElement(
  IN p_movie_id integer,
  IN p_title VARCHAR,
  IN p_duration interval,
  IN p_views integer
)
LANGUAGE plpgsql
AS $$
BEGIN
  INSERT INTO movie (movie_id, title, duration, views)
  VALUES (p_movie_id, p_title, p_duration, p_views);
END;
$$;

CREATE VIEW selectMovie AS
SELECT * FROM movie;

CREATE OR REPLACE PROCEDURE updateMovieElement(
  IN p_movie_id integer,
  IN p_title VARCHAR,
  IN p_duration interval,
  IN p_views integer
)
LANGUAGE plpgsql
AS $$
BEGIN
  UPDATE movie
  SET title = p_title, duration = p_duration, views = p_views
  WHERE movie_id = p_movie_id;
END;
$$;

CREATE OR REPLACE PROCEDURE deleteMovieElement(
  IN p_movie_id integer
)
LANGUAGE plpgsql
AS $$
BEGIN
  DELETE FROM movie WHERE movie_id = p_movie_id;
END;
$$;

/*class series*/

CREATE OR REPLACE PROCEDURE createSeriesElement(
  IN p_series_id integer,
  IN p_title VARCHAR,
  IN p_views integer
)
LANGUAGE plpgsql
AS $$
BEGIN
  INSERT INTO series (series_id, title, views)
  VALUES (p_series_id, p_title, p_views);
END;
$$;

CREATE VIEW selectSeries AS
SELECT * FROM series;

CREATE OR REPLACE PROCEDURE updateSeriesElement(
  IN p_series_id integer,
  IN p_title VARCHAR,
  IN p_views integer
)
LANGUAGE plpgsql
AS $$
BEGIN
  UPDATE series
  SET title = p_title, views = p_views
  WHERE series_id = p_series_id;
END;
$$;

CREATE OR REPLACE PROCEDURE deleteSeriesElement(
  IN p_series_id integer
)
LANGUAGE plpgsql
AS $$
BEGIN
  DELETE FROM series WHERE series_id = p_series_id;
END;
$$;

/*class profile*/

CREATE OR REPLACE PROCEDURE createSeriesElement(
  IN p_profile_id integer,
  IN p_account_id integer,
  IN p_profile_image VARCHAR,
  IN p_profile_child boolean,
  IN p_age integer,
  IN p_language VARCHAR,
  IN p_watchlist_id integer,
  IN p_history_id integer,
  IN p_country VARCHAR
  IN p_is_trial boolean,
  IN p_is_discount boolean
)
LANGUAGE plpgsql
AS $$
BEGIN
  INSERT INTO profile (profile_id, account_id, profile_image, profile_child, age, language, watchlist_id, history_id, country, is_trial, is_discount)
  VALUES (p_profile_id, p_account_id, p_profile_image, p_profile_child, p_age,  p_language, p_watchlist_id, p_history_id, p_country, p_is_discount, p_is_discount);
END;
$$;

CREATE VIEW selectProfile AS
SELECT * FROM profile;

CREATE OR REPLACE PROCEDURE updateProfileElement(
  IN p_profile_id integer,
  IN p_profile_image VARCHAR,
  IN p_profile_child boolean,
  IN p_age integer,
  IN p_language VARCHAR,
  IN p_country VARCHAR,
  IN p_is_trial boolean,
  IN p_is_discount boolean
)
LANGUAGE plpgsql
AS $$
BEGIN
  UPDATE profile
  SET profile_image = p_profile_image, profile_child = p_profile_child, age = p_age, language = p_language, country = p_country, is_trial = p_is_trial, is_discount = p_is_discount
  WHERE profile_id = p_profile_id;
END;
$$;

CREATE OR REPLACE PROCEDURE deleteProfileElement(
  IN p_profile_id integer
)
LANGUAGE plpgsql
AS $$
BEGIN
  DELETE FROM profile WHERE profile_id = p_profile_id;
END;
$$;

/*class account*/

CREATE OR REPLACE PROCEDURE createAccountElement(
  IN p_account_id integer,
  IN p_email VARCHAR,
  IN p_password VARCHAR,
  IN p_payment_method VARCHAR,
  IN p_blocked boolean,
  IN p_login_attempts integer,
  IN p_last_login date,
  IN p_subscription_id integer
)
LANGUAGE plpgsql
AS $$
BEGIN
  INSERT INTO account (account_id, email, password, payment_method, blocked, login_attempts, last_login, subscription_id)
  VALUES (p_account_id, p_email, p_password, p_payment_method, p_blocked, p_login_attempts, p_last_login, p_subscription_id);
END;
$$;

CREATE VIEW selectAccount AS
SELECT * FROM account;

CREATE OR REPLACE PROCEDURE updateAccountElement(
IN p_account_id integer,
IN p_email VARCHAR,
  IN p_password VARCHAR,
  IN p_payment_method VARCHAR,
  IN p_blocked boolean,
  IN p_login_attempts integer,
  IN p_last_login date,
  IN p_subscription_id integer
)
LANGUAGE plpgsql
AS $$
BEGIN
  UPDATE account
  SET email = p_email, password = p_password, payment_method = p_payment_method, blocked = p_blocked, login_attempts = p_login_attempts, subscription_id = p_subscription_id
  WHERE account_id = p_account_id;
END;
$$;

CREATE OR REPLACE PROCEDURE deleteAccountElement(
  IN p_account_id integer
)
LANGUAGE plpgsql
AS $$
BEGIN
  DELETE FROM account WHERE account_id = p_account_id;
END;
$$;
