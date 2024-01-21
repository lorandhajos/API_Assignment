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
  SET NOCOUNT ON;
  INSERT INTO interests (profile_id, genre_id)
  VALUES (p_profileID, p_genre_id);
END;
$$;
