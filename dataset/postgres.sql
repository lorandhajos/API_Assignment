-- Adminer 4.8.1 PostgreSQL 16.1 (Debian 16.1-1.pgdg120+1) dump

\connect "postgres";

DROP TABLE IF EXISTS "account";
DROP SEQUENCE IF EXISTS account_account_id_seq;
CREATE SEQUENCE account_account_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."account" (
    "account_id" integer DEFAULT nextval('account_account_id_seq') NOT NULL,
    "email" character varying(255) NOT NULL,
    "password" character varying(255) NOT NULL,
    "payment_method" character varying(255) NOT NULL,
    "blocked" boolean DEFAULT false,
    "login_attempts" integer DEFAULT '0',
    "last_login" date,
    "subscription_id" integer,
    CONSTRAINT "account_pkey" PRIMARY KEY ("account_id")
) WITH (oids = false);

INSERT INTO "account" ("account_id", "email", "password", "payment_method", "blocked", "login_attempts", "last_login", "subscription_id") VALUES
(2,	'test.eamil@tetst.com',	'7c4a8d09ca3762af61e59520943dc26494f8941b',	'MasterCard',	'f',	0,	'2023-12-11',	2),
(3,	'email@test.com',	'20eabe5d64b0e216796e834f52d61fd0b70332fc',	'iDeal',	'f',	0,	'2023-12-11',	3),
(1,	'email.email@test.com',	'8cb2237d0679ca88db6464eac60da96345513964',	'Visa',	'f',	0,	'2023-12-11',	1);

DROP TABLE IF EXISTS "episode";
DROP SEQUENCE IF EXISTS episode_episode_id_seq;
CREATE SEQUENCE episode_episode_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."episode" (
    "episode_id" integer DEFAULT nextval('episode_episode_id_seq') NOT NULL,
    "title" character varying(255) NOT NULL,
    "duration" interval DEFAULT '00:00:00' NOT NULL,
    "season_number" integer NOT NULL,
    "series_id" integer NOT NULL,
    CONSTRAINT "episode_pkey" PRIMARY KEY ("episode_id")
) WITH (oids = false);

INSERT INTO "episode" ("episode_id", "title", "duration", "season_number", "series_id") VALUES
(6,	'pokjhbv',	'01:00:00',	2,	3),
(5,	'fghjkjhgfgbn',	'00:10:00',	1,	3),
(4,	'sdfsdfs',	'00:00:40',	1,	2),
(3,	'Title3',	'00:50:00',	2,	1),
(2,	'Title2',	'00:07:00',	1,	1),
(1,	'Title1',	'20:00:00',	1,	1);

DROP TABLE IF EXISTS "genre";
DROP SEQUENCE IF EXISTS genre_genre_id_seq;
CREATE SEQUENCE genre_genre_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."genre" (
    "genre_id" integer DEFAULT nextval('genre_genre_id_seq') NOT NULL,
    "name" character varying(255) NOT NULL,
    "age_restriction" integer NOT NULL,
    CONSTRAINT "genre_pkey" PRIMARY KEY ("genre_id")
) WITH (oids = false);

INSERT INTO "genre" ("genre_id", "name", "age_restriction") VALUES
(1,	'Horror',	18),
(2,	'Comedy',	0),
(3,	'Action',	13),
(4,	'Adventure',	8),
(5,	'Soap opera',	16),
(6,	'Documentary',	12);

DROP TABLE IF EXISTS "history";
DROP SEQUENCE IF EXISTS history_history_id_seq;
CREATE SEQUENCE history_history_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."history" (
    "history_id" integer DEFAULT nextval('history_history_id_seq') NOT NULL,
    CONSTRAINT "history_pkey" PRIMARY KEY ("history_id")
) WITH (oids = false);

INSERT INTO "history" ("history_id") VALUES
(1),
(2),
(3);

DROP TABLE IF EXISTS "history_movies";
DROP SEQUENCE IF EXISTS history_movies_history_movies_id_seq;
CREATE SEQUENCE history_movies_history_movies_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."history_movies" (
    "history_movies_id" integer DEFAULT nextval('history_movies_history_movies_id_seq') NOT NULL,
    "history_id" integer NOT NULL,
    "movie_id" integer NOT NULL,
    CONSTRAINT "history_movies_pkey" PRIMARY KEY ("history_movies_id")
) WITH (oids = false);

INSERT INTO "history_movies" ("history_movies_id", "history_id", "movie_id") VALUES
(1,	1,	1),
(2,	2,	2),
(3,	3,	1);

DROP TABLE IF EXISTS "history_series";
DROP SEQUENCE IF EXISTS history_series_history_series_id_seq;
CREATE SEQUENCE history_series_history_series_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."history_series" (
    "history_series_id" integer DEFAULT nextval('history_series_history_series_id_seq') NOT NULL,
    "history_id" integer NOT NULL,
    "series_id" integer NOT NULL,
    CONSTRAINT "history_series_pkey" PRIMARY KEY ("history_series_id")
) WITH (oids = false);

INSERT INTO "history_series" ("history_series_id", "history_id", "series_id") VALUES
(1,	1,	2),
(2,	3,	1),
(3,	2,	2);

DROP TABLE IF EXISTS "interests";
CREATE TABLE "public"."interests" (
    "profile_id" integer NOT NULL,
    "genre_id" integer NOT NULL
) WITH (oids = false);

INSERT INTO "interests" ("profile_id", "genre_id") VALUES
(1,	1),
(1,	2),
(2,	3),
(2,	1),
(3,	3),
(3,	2),
(3,	1);

DROP TABLE IF EXISTS "movie";
DROP SEQUENCE IF EXISTS movie_movie_id_seq;
CREATE SEQUENCE movie_movie_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."movie" (
    "movie_id" integer DEFAULT nextval('movie_movie_id_seq') NOT NULL,
    "title" character varying(255) NOT NULL,
    "duration" interval DEFAULT '00:00:00' NOT NULL,
    "views" integer NOT NULL,
    CONSTRAINT "movie_pkey" PRIMARY KEY ("movie_id")
) WITH (oids = false);

INSERT INTO "movie" ("movie_id", "title", "duration", "views") VALUES
(1,	'The movie',	'02:30:00',	612),
(3,	'A third movie',	'03:01:09',	57),
(2,	'A diffrent movie',	'01:00:00',	230);

DROP TABLE IF EXISTS "movie_genre";
CREATE TABLE "public"."movie_genre" (
    "movie_id" integer NOT NULL,
    "genre_id" integer NOT NULL
) WITH (oids = false);

INSERT INTO "movie_genre" ("movie_id", "genre_id") VALUES
(1,	2),
(2,	1),
(3,	3);

DROP TABLE IF EXISTS "profile";
DROP SEQUENCE IF EXISTS profile_profile_id_seq;
CREATE SEQUENCE profile_profile_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."profile" (
    "profile_id" integer DEFAULT nextval('profile_profile_id_seq') NOT NULL,
    "account_id" integer NOT NULL,
    "profile_image" character varying(255) DEFAULT 'placeholder.jpeg' NOT NULL,
    "profile_child" boolean DEFAULT false,
    "age" integer NOT NULL,
    "language" character varying(255) DEFAULT 'English' NOT NULL,
    "watchlist_id" integer NOT NULL,
    "history_id" integer NOT NULL,
    "country" character varying(255) NOT NULL,
    CONSTRAINT "profile_pkey" PRIMARY KEY ("profile_id")
) WITH (oids = false);

INSERT INTO "profile" ("profile_id", "account_id", "profile_image", "profile_child", "age", "language", "watchlist_id", "history_id", "country") VALUES
(1,	1,	'placeholder.jpeg',	't',	12,	'English',	1,	1,	'Brazil'),
(2,	2,	'placeholder.jpeg',	'f',	20,	'English',	2,	2,	'Netherlands'),
(3,	3,	'placeholder.jpeg',	'f',	18,	'English',	3,	3,	'Brazil');

DROP VIEW IF EXISTS "selectaccount";
CREATE TABLE "selectaccount" ("account_id" integer, "email" character varying(255), "password" character varying(255), "payment_method" character varying(255), "blocked" boolean, "login_attempts" integer, "last_login" date, "subscription_id" integer);


DROP VIEW IF EXISTS "selecthistorymovies";
CREATE TABLE "selecthistorymovies" ("history_movies_id" integer, "history_id" integer, "movie_id" integer);


DROP VIEW IF EXISTS "selecthistoryseries";
CREATE TABLE "selecthistoryseries" ("history_series_id" integer, "history_id" integer, "series_id" integer);


DROP VIEW IF EXISTS "selectinterests";
CREATE TABLE "selectinterests" ("profile_id" integer, "genre_id" integer);


DROP VIEW IF EXISTS "selectmovie";
CREATE TABLE "selectmovie" ("movie_id" integer, "title" character varying(255), "duration" interval, "views" integer);


DROP VIEW IF EXISTS "selectmoviesgenre";
CREATE TABLE "selectmoviesgenre" ("movie_id" integer, "genre_id" integer);


DROP VIEW IF EXISTS "selectprofile";
CREATE TABLE "selectprofile" ("profile_id" integer, "account_id" integer, "profile_image" character varying(255), "profile_child" boolean, "age" integer, "language" character varying(255), "watchlist_id" integer, "history_id" integer, "country" character varying(255));


DROP VIEW IF EXISTS "selectseries";
CREATE TABLE "selectseries" ("series_id" integer, "title" character varying(255), "views" integer);


DROP VIEW IF EXISTS "selectseriesgenre";
CREATE TABLE "selectseriesgenre" ("series_id" integer, "genre_id" integer);


DROP VIEW IF EXISTS "selectsubscription";
CREATE TABLE "selectsubscription" ("subscription_id" integer, "description" character varying(255), "subscription_price" real);


DROP VIEW IF EXISTS "selectwatchlistmovies";
CREATE TABLE "selectwatchlistmovies" ("watchlist_movies_id" integer, "watchlist_id" integer, "movie_id" integer);


DROP VIEW IF EXISTS "selectwatchlistseries";
CREATE TABLE "selectwatchlistseries" ("watchlist_series_id" integer, "watchlist_id" integer, "series_id" integer);


DROP TABLE IF EXISTS "series";
DROP SEQUENCE IF EXISTS series_series_id_seq;
CREATE SEQUENCE series_series_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."series" (
    "series_id" integer DEFAULT nextval('series_series_id_seq') NOT NULL,
    "title" character varying(255) NOT NULL,
    "views" integer NOT NULL,
    CONSTRAINT "series_pkey" PRIMARY KEY ("series_id")
) WITH (oids = false);

INSERT INTO "series" ("series_id", "title", "views") VALUES
(1,	'Title of a series',	56),
(3,	'Third title of the series',	870),
(2,	'Second title of the series',	76);

DROP TABLE IF EXISTS "series_genre";
CREATE TABLE "public"."series_genre" (
    "series_id" integer NOT NULL,
    "genre_id" integer NOT NULL
) WITH (oids = false);

INSERT INTO "series_genre" ("series_id", "genre_id") VALUES
(1,	2),
(2,	3),
(3,	1);

DROP TABLE IF EXISTS "subscription";
DROP SEQUENCE IF EXISTS subscription_subscription_id_seq;
CREATE SEQUENCE subscription_subscription_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."subscription" (
    "subscription_id" integer DEFAULT nextval('subscription_subscription_id_seq') NOT NULL,
    "description" character varying(255) NOT NULL,
    "subscription_price" real DEFAULT '7.99' NOT NULL,
    CONSTRAINT "subscription_pkey" PRIMARY KEY ("subscription_id")
) WITH (oids = false);

INSERT INTO "subscription" ("subscription_id", "description", "subscription_price") VALUES
(1,	'Ubscription for 1 person',	7.99),
(2,	'Subscription for up to 5 people',	11.99),
(3,	'Student subscription',	5.99);

DROP TABLE IF EXISTS "watchlist";
DROP SEQUENCE IF EXISTS watchlist_watchlist_id_seq;
CREATE SEQUENCE watchlist_watchlist_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."watchlist" (
    "watchlist_id" integer DEFAULT nextval('watchlist_watchlist_id_seq') NOT NULL,
    CONSTRAINT "watchlist_pkey" PRIMARY KEY ("watchlist_id")
) WITH (oids = false);

INSERT INTO "watchlist" ("watchlist_id") VALUES
(1),
(2),
(3),
(4);

DROP TABLE IF EXISTS "watchlist_movies";
DROP SEQUENCE IF EXISTS watchlist_movies_watchlist_movies_id_seq;
CREATE SEQUENCE watchlist_movies_watchlist_movies_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."watchlist_movies" (
    "watchlist_movies_id" integer DEFAULT nextval('watchlist_movies_watchlist_movies_id_seq') NOT NULL,
    "watchlist_id" integer NOT NULL,
    "movie_id" integer NOT NULL,
    CONSTRAINT "watchlist_movies_pkey" PRIMARY KEY ("watchlist_movies_id")
) WITH (oids = false);

INSERT INTO "watchlist_movies" ("watchlist_movies_id", "watchlist_id", "movie_id") VALUES
(1,	1,	2),
(2,	2,	1),
(3,	3,	1);

DROP TABLE IF EXISTS "watchlist_series";
DROP SEQUENCE IF EXISTS watchlist_series_watchlist_series_id_seq;
CREATE SEQUENCE watchlist_series_watchlist_series_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."watchlist_series" (
    "watchlist_series_id" integer DEFAULT nextval('watchlist_series_watchlist_series_id_seq') NOT NULL,
    "watchlist_id" integer NOT NULL,
    "series_id" integer NOT NULL,
    CONSTRAINT "watchlist_series_pkey" PRIMARY KEY ("watchlist_series_id")
) WITH (oids = false);

INSERT INTO "watchlist_series" ("watchlist_series_id", "watchlist_id", "series_id") VALUES
(1,	2,	1),
(2,	3,	1);

ALTER TABLE ONLY "public"."account" ADD CONSTRAINT "fk_subscription" FOREIGN KEY (subscription_id) REFERENCES subscription(subscription_id) NOT DEFERRABLE;

ALTER TABLE ONLY "public"."episode" ADD CONSTRAINT "fk_series" FOREIGN KEY (series_id) REFERENCES series(series_id) NOT DEFERRABLE;

ALTER TABLE ONLY "public"."history_movies" ADD CONSTRAINT "history_movies_history_id_fkey" FOREIGN KEY (history_id) REFERENCES history(history_id) ON UPDATE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "public"."history_movies" ADD CONSTRAINT "history_movies_movie_id_fkey" FOREIGN KEY (movie_id) REFERENCES movie(movie_id) ON UPDATE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."history_series" ADD CONSTRAINT "fk_history" FOREIGN KEY (history_id) REFERENCES history(history_id) NOT DEFERRABLE;
ALTER TABLE ONLY "public"."history_series" ADD CONSTRAINT "fk_series" FOREIGN KEY (series_id) REFERENCES series(series_id) NOT DEFERRABLE;

ALTER TABLE ONLY "public"."interests" ADD CONSTRAINT "fk_genre" FOREIGN KEY (genre_id) REFERENCES genre(genre_id) NOT DEFERRABLE;
ALTER TABLE ONLY "public"."interests" ADD CONSTRAINT "fk_profile" FOREIGN KEY (profile_id) REFERENCES profile(profile_id) NOT DEFERRABLE;

ALTER TABLE ONLY "public"."movie_genre" ADD CONSTRAINT "fk_genre" FOREIGN KEY (genre_id) REFERENCES genre(genre_id) NOT DEFERRABLE;
ALTER TABLE ONLY "public"."movie_genre" ADD CONSTRAINT "fk_movie" FOREIGN KEY (movie_id) REFERENCES movie(movie_id) NOT DEFERRABLE;

ALTER TABLE ONLY "public"."profile" ADD CONSTRAINT "fk_account" FOREIGN KEY (account_id) REFERENCES account(account_id) NOT DEFERRABLE;
ALTER TABLE ONLY "public"."profile" ADD CONSTRAINT "fk_watchlist" FOREIGN KEY (watchlist_id) REFERENCES watchlist(watchlist_id) NOT DEFERRABLE;

ALTER TABLE ONLY "public"."series_genre" ADD CONSTRAINT "fk_genre" FOREIGN KEY (genre_id) REFERENCES genre(genre_id) NOT DEFERRABLE;
ALTER TABLE ONLY "public"."series_genre" ADD CONSTRAINT "fk_movie" FOREIGN KEY (series_id) REFERENCES series(series_id) NOT DEFERRABLE;

ALTER TABLE ONLY "public"."watchlist_movies" ADD CONSTRAINT "fk_movie" FOREIGN KEY (movie_id) REFERENCES movie(movie_id) NOT DEFERRABLE;
ALTER TABLE ONLY "public"."watchlist_movies" ADD CONSTRAINT "fk_watchlist" FOREIGN KEY (watchlist_id) REFERENCES watchlist(watchlist_id) NOT DEFERRABLE;

ALTER TABLE ONLY "public"."watchlist_series" ADD CONSTRAINT "fk_series" FOREIGN KEY (series_id) REFERENCES series(series_id) NOT DEFERRABLE;
ALTER TABLE ONLY "public"."watchlist_series" ADD CONSTRAINT "fk_watchlist" FOREIGN KEY (watchlist_id) REFERENCES watchlist(watchlist_id) NOT DEFERRABLE;

DROP TABLE IF EXISTS "selectaccount";
CREATE VIEW "selectaccount" AS SELECT account_id,
    email,
    password,
    payment_method,
    blocked,
    login_attempts,
    last_login,
    subscription_id
   FROM account;

DROP TABLE IF EXISTS "selecthistorymovies";
CREATE VIEW "selecthistorymovies" AS SELECT history_movies_id,
    history_id,
    movie_id
   FROM history_movies;

DROP TABLE IF EXISTS "selecthistoryseries";
CREATE VIEW "selecthistoryseries" AS SELECT history_series_id,
    history_id,
    series_id
   FROM history_series;

DROP TABLE IF EXISTS "selectinterests";
CREATE VIEW "selectinterests" AS SELECT profile_id,
    genre_id
   FROM interests;

DROP TABLE IF EXISTS "selectmovie";
CREATE VIEW "selectmovie" AS SELECT movie_id,
    title,
    duration,
    views
   FROM movie;

DROP TABLE IF EXISTS "selectmoviesgenre";
CREATE VIEW "selectmoviesgenre" AS SELECT movie_id,
    genre_id
   FROM movie_genre;

DROP TABLE IF EXISTS "selectprofile";
CREATE VIEW "selectprofile" AS SELECT profile_id,
    account_id,
    profile_image,
    profile_child,
    age,
    language,
    watchlist_id,
    history_id,
    country
   FROM profile;

DROP TABLE IF EXISTS "selectseries";
CREATE VIEW "selectseries" AS SELECT series_id,
    title,
    views
   FROM series;

DROP TABLE IF EXISTS "selectseriesgenre";
CREATE VIEW "selectseriesgenre" AS SELECT series_id,
    genre_id
   FROM series_genre;

DROP TABLE IF EXISTS "selectsubscription";
CREATE VIEW "selectsubscription" AS SELECT subscription_id,
    description,
    subscription_price
   FROM subscription;

DROP TABLE IF EXISTS "selectwatchlistmovies";
CREATE VIEW "selectwatchlistmovies" AS SELECT watchlist_movies_id,
    watchlist_id,
    movie_id
   FROM watchlist_movies;

DROP TABLE IF EXISTS "selectwatchlistseries";
CREATE VIEW "selectwatchlistseries" AS SELECT watchlist_series_id,
    watchlist_id,
    series_id
   FROM watchlist_series;

-- 2024-01-21 21:38:26.532531+00
