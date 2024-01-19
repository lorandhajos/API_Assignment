CREATE USER api_user ENCRYPTED PASSWORD 'yqa*!ny31fgH1'

REVOKE ALL PRIVILEGES ON TABLE account FROM api_user;

REVOKE ALL PRIVILEGES ON TABLE episode FROM api_user;

REVOKE ALL PRIVILEGES ON TABLE genre FROM api_user;

REVOKE ALL PRIVILEGES ON TABLE history FROM api_user;

REVOKE ALL PRIVILEGES ON TABLE history_movies FROM api_user;

REVOKE ALL PRIVILEGES ON TABLE interests FROM api_user;

REVOKE ALL PRIVILEGES ON TABLE movie FROM api_user;

REVOKE ALL PRIVILEGES ON TABLE movie_genre FROM api_user;

REVOKE ALL PRIVILEGES ON TABLE profile FROM api_user;

REVOKE ALL PRIVILEGES ON TABLE series FROM api_user;

REVOKE ALL PRIVILEGES ON TABLE series_genre FROM api_user;

REVOKE ALL PRIVILEGES ON TABLE subscription FROM api_user;

REVOKE ALL PRIVILEGES ON TABLE watchlist FROM api_user;

REVOKE ALL PRIVILEGES ON TABLE watchlist_movies FROM api_user;

REVOKE ALL PRIVILEGES ON TABLE watchlist_series FROM api_user;


GRANT EXECUTE ON FUNCTION getWatchlistFilmsForID TO api_user;

GRANT EXECUTE ON FUNCTION getWatchlistSeriesForID TO api_user;

GRANT EXECUTE ON FUNCTION getHistoryMoviesForID TO api_user;

GRANT EXECUTE ON FUNCTION getHistorySeriesForID TO api_user;

GRANT EXECUTE ON FUNCTION getAgeRestrictorFilms TO api_user;

GRANT EXECUTE ON FUNCTION getAgeRestrictorSeries TO api_user;

GRANT EXECUTE ON FUNCTION login TO api_user;

GRANT EXECUTE ON FUNCTION getMovieViews TO api_user;

GRANT EXECUTE ON FUNCTION getSeriesViews TO api_user;

GRANT EXECUTE ON FUNCTION getProfileCountry TO api_user;
