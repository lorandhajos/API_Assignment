CREATE USER api_user ENCRYPTED PASSWORD 'yqa*!ny31fgH1';

REVOKE ALL PRIVILEGES ON TABLE account FROM api_user;

REVOKE ALL PRIVILEGES ON TABLE episode FROM api_user;

REVOKE ALL PRIVILEGES ON TABLE genre FROM api_user;

REVOKE ALL PRIVILEGES ON TABLE history_movies FROM api_user;

REVOKE ALL PRIVILEGES ON TABLE interests FROM api_user;

REVOKE ALL PRIVILEGES ON TABLE movie FROM api_user;

REVOKE ALL PRIVILEGES ON TABLE movie_genre FROM api_user;

REVOKE ALL PRIVILEGES ON TABLE profile FROM api_user;

REVOKE ALL PRIVILEGES ON TABLE series FROM api_user;

REVOKE ALL PRIVILEGES ON TABLE series_genre FROM api_user;

REVOKE ALL PRIVILEGES ON TABLE subscription FROM api_user;

REVOKE ALL PRIVILEGES ON TABLE watchlist_movies FROM api_user;

REVOKE ALL PRIVILEGES ON TABLE watchlist_series FROM api_user;

GRANT EXECUTE ON FUNCTION getWatchlistFilmsForID TO api_user;

GRANT EXECUTE ON FUNCTION getWatchlistSeriesForID TO api_user;

GRANT EXECUTE ON FUNCTION getHistoryMoviesForID TO api_user;

GRANT EXECUTE ON FUNCTION getHistorySeriesForID TO api_user;

GRANT EXECUTE ON FUNCTION getAgeRestrictorFilms TO api_user;

GRANT EXECUTE ON FUNCTION getAgeRestrictorSeries TO api_user;

GRANT EXECUTE ON FUNCTION login TO api_user;

GRANT EXECUTE ON FUNCTION getMovieNames TO api_user;

GRANT EXECUTE ON FUNCTION getMovieViews TO api_user;

GRANT EXECUTE ON FUNCTION getSeriesTitle TO api_user;

GRANT EXECUTE ON FUNCTION getSeriesViews TO api_user;

GRANT EXECUTE ON FUNCTION getNOfUsersPerCountry TO api_user;

GRANT EXECUTE ON FUNCTION getUsersCountry TO api_user;

/*Revoking privileges from the CRUD part, so that api user gets no acces*/

REVOKE ALL PRIVILEGES ON PROCEDURE createWatchlistMoviesElement(p_watchlist_movies_id integer, p_watchlist_id integer, p_movie_id integer) FROM api_user;

REVOKE ALL PRIVILEGES ON PROCEDURE createWatchlistMoviesElement(p_watchlist_movies_id integer, p_watchlist_id integer, p_movie_id integer) FROM api_user;

REVOKE ALL PRIVILEGES ON PROCEDURE updateWatchlistMoviesElement(p_watchlist_movies_id integer, p_watchlist_id integer, p_movie_id integer) FROM api_user;

REVOKE ALL PRIVILEGES ON PROCEDURE deleteWatchlistMoviesElement(p_watchlist_movies_id integer) FROM api_user;

REVOKE ALL PRIVILEGES ON PROCEDURE createWatchlistSeriesElement(p_watchlist_series_id integer, p_watchlist_id integer, p_series_id integer) FROM api_user;

REVOKE ALL PRIVILEGES ON PROCEDURE updateWatchlistSeriesElement(p_watchlist_series_id integer, p_watchlist_id integer, p_series_id integer) FROM api_user;

REVOKE ALL PRIVILEGES ON PROCEDURE deleteWatchlistSeriesElement(p_watchlist_series_id integer) FROM api_user;

REVOKE ALL PRIVILEGES ON PROCEDURE deleteWatchlistSeriesElement(p_watchlist_series_id integer) FROM api_user;

REVOKE ALL PRIVILEGES ON PROCEDURE createHistoryMoviesElement(p_history_movies_id integer, p_history_id integer, p_movie_id integer, p_status_finished boolean, p_status_time interval) FROM api_user;

REVOKE ALL PRIVILEGES ON PROCEDURE updateHistoryMoviesElement(p_history_movies_id integer, p_history_id integer, p_movie_id integer, p_status_finished boolean, p_status_time interval) FROM api_user;

REVOKE ALL PRIVILEGES ON PROCEDURE deleteHistoryMoviesElement(p_history_movies_id integer) FROM api_user;

REVOKE ALL PRIVILEGES ON PROCEDURE createHistorySeriesElement(p_history_series_id integer, p_history_id integer, p_series_id integer) FROM api_user;

REVOKE ALL PRIVILEGES ON PROCEDURE updateHistorySeriesElement(p_history_series_id integer, p_history_id integer, p_series_id integer) FROM api_user;

REVOKE ALL PRIVILEGES ON PROCEDURE deleteHistorySeriesElement(p_history_series_id integer) FROM api_user;

REVOKE ALL PRIVILEGES ON PROCEDURE createInterestElement(p_profile_id integer, p_genre_id integer) FROM api_user;

REVOKE ALL PRIVILEGES ON PROCEDURE updateInterestElement(p_profile_id integer, p_genre_id integer, p_desired_genre_id integer) FROM api_user;

REVOKE ALL PRIVILEGES ON PROCEDURE deleteInterestElement(p_profile_id integer, p_genre_id integer) FROM api_user;

REVOKE ALL PRIVILEGES ON PROCEDURE createGenreMoviesElement(p_genre_id integer, p_movie_id integer) FROM api_user;

REVOKE ALL PRIVILEGES ON PROCEDURE updateMovieGenreElement(p_genre_id integer, p_movie_id integer, p_desired_genre_id integer) FROM api_user;

REVOKE ALL PRIVILEGES ON PROCEDURE deleteMoviesGenreElement(p_genre_id integer, p_movie_id integer) FROM api_user;

REVOKE ALL PRIVILEGES ON PROCEDURE createGenreSeriesElement(p_genre_id integer, p_series_id integer) FROM api_user;

REVOKE ALL PRIVILEGES ON PROCEDURE updateSeriesGenreElement(p_genre_id integer, p_series_id integer, p_desired_genre_id integer) FROM api_user;

REVOKE ALL PRIVILEGES ON PROCEDURE deleteSeriesGenreElement(p_genre_id integer, p_series_id integer) FROM api_user;

REVOKE ALL PRIVILEGES ON PROCEDURE createSubscriptionElement(p_subscription_id integer, p_description VARCHAR, p_price real) FROM api_user;

REVOKE ALL PRIVILEGES ON PROCEDURE updateUbscriptionElement(p_subscription_id integer, p_description VARCHAR, p_price real) FROM api_user;

REVOKE ALL PRIVILEGES ON PROCEDURE deleteSubscriptionElement(p_subscription_id integer) FROM api_user;

REVOKE ALL PRIVILEGES ON PROCEDURE createMovieElement(p_movie_id integer, p_title VARCHAR, p_duration interval, p_views integer) FROM api_user;

REVOKE ALL PRIVILEGES ON PROCEDURE updateMovieElement(p_movie_id integer, p_title VARCHAR, p_duration interval, p_views integer) FROM api_user;

REVOKE ALL PRIVILEGES ON PROCEDURE deleteMovieElement(p_movie_id integer) FROM api_user;

REVOKE ALL PRIVILEGES ON PROCEDURE createSeriesElement(p_series_id integer, p_title VARCHAR, p_views integer) FROM api_user;

REVOKE ALL PRIVILEGES ON PROCEDURE updateSeriesElement(p_series_id integer, p_title VARCHAR, p_views integer) FROM api_user;

REVOKE ALL PRIVILEGES ON PROCEDURE deleteSeriesElement(p_series_id integer) FROM api_user;

REVOKE ALL PRIVILEGES ON PROCEDURE createProfileElement(p_profile_id integer, p_account_id integer, p_profile_image VARCHAR, p_profile_child boolean, p_age integer, p_language VARCHAR, p_watchlist_id integer, p_history_id integer, p_country VARCHAR, p_is_trial boolean, p_is_discount boolean) FROM api_user;

REVOKE ALL PRIVILEGES ON PROCEDURE updateProfileElement(p_profile_id integer, p_account_id integer, p_profile_image VARCHAR, p_profile_child boolean, p_age integer, p_language VARCHAR, p_country VARCHAR, p_is_trial boolean, p_is_discount boolean) FROM api_user;

REVOKE ALL PRIVILEGES ON PROCEDURE deleteProfileElement(p_profile_id integer) FROM api_user;

REVOKE ALL PRIVILEGES ON PROCEDURE createAccountElement(p_account_id integer, p_email VARCHAR, p_password VARCHAR, p_payment_method VARCHAR, p_blocked boolean, p_login_attempts integer, p_last_login date, p_subscription_id integer) FROM api_user;

REVOKE ALL PRIVILEGES ON PROCEDURE updateAccountElement(p_account_id integer, p_email VARCHAR, p_password VARCHAR, p_payment_method VARCHAR, p_blocked boolean, p_login_attempts integer, p_last_login date, p_subscription_id integer) FROM api_user;

REVOKE ALL PRIVILEGES ON PROCEDURE deleteAccountElement(p_account_id integer) FROM api_user;

CREATE USER authorisedDBUser ENCRYPTED PASSWORD 'yn5j1masd!';

CREATE ROLE junior;

/*Junior gets to change only films and series*/

REVOKE ALL PRIVILEGES ON TABLE account FROM junior;

REVOKE ALL PRIVILEGES ON TABLE genre FROM junior;

REVOKE ALL PRIVILEGES ON TABLE history_movies FROM junior;

REVOKE ALL PRIVILEGES ON TABLE interests FROM junior;

REVOKE ALL PRIVILEGES ON TABLE movie_genre FROM junior;

REVOKE ALL PRIVILEGES ON TABLE profile FROM junior;

REVOKE ALL PRIVILEGES ON TABLE series_genre FROM junior;

REVOKE ALL PRIVILEGES ON TABLE subscription FROM junior;

REVOKE ALL PRIVILEGES ON TABLE watchlist_movies FROM junior;

REVOKE ALL PRIVILEGES ON TABLE watchlist_series FROM junior;

CREATE ROLE medior;

/*Medior gets to do more, but does not get to see personla data*/

REVOKE ALL PRIVILEGES ON TABLE account FROM medior;

REVOKE ALL PRIVILEGES ON TABLE profile FROM medior;

CREATE ROLE senior;

/*senior gets to keep the default acces rights*/

GRANT senior TO authorisedDBUser WITH INHERIT TRUE;
