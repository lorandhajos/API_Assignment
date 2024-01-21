CREATE TABLE IF NOT EXISTS `Account`(
    account_id int(11) AUTO_INCREMENT PRIMARY KEY,
    email varchar(255) not null,
    `password` varchar(255) not null,
    payment_method varchar(255) not null,
    blocked bit default 0
    );
CREATE TABLE IF NOT EXISTS `Profile`(
    profile_id int(11) AUTO_INCREMENT PRIMARY KEY,
    account_id int(11) not null,
    profile_image varchar(255) not null default 'placeholder.jpeg',
    profile_child bit default 0
    );
CREATE TABLE IF NOT EXISTS `Subscription`(
    subscription_id int(11) AUTO_INCREMENT PRIMARY KEY,
    description varchar(255) not null,
    subscription_price float not null default 7.99    
    );
CREATE TABLE IF NOT EXISTS `Movie`(
    movie_id int(11) AUTO_INCREMENT PRIMARY KEY,
    title varchar(255) not null,
    duration timestamp not null default '00:00:00', 
    genre_id int(11) not null
    );
CREATE TABLE IF NOT EXISTS `Episode`(
    episode_id int(11) AUTO_INCREMENT PRIMARY KEY,
    title varchar(255) not null,
    duration timestamp not null default '00:00:00',
    season_id int(11) not null
    );
CREATE TABLE IF NOT EXISTS `Subtitle`(
    subtitle_id int(11) AUTO_INCREMENT PRIMARY KEY,
    language varchar(255) not null,
	movie_id int(11) null,
    episode_id int(11) null,
    subtitle_location varchar(255) not null    
    );