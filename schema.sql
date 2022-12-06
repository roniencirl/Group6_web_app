DROP TABLE IF EXISTS posts;

CREATE TABLE posts (

    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    post_author bigint(20) UNSIGNED NOT NULL DEFAULT '0',
    post_date datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    post_title text NOT NULL,
    post_content longtext NOT NULL,
    post_modified datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,

);

DROP TABLE IF EXISTS users;

CREATE TABLE users (

  ID bigint(20) UNSIGNED NOT NULL,
  user_login varchar(60)  NOT NULL DEFAULT '',
  user_pass varchar(255) COLLATE  NOT NULL DEFAULT '',
  user_firstname varchar(50) COLLATE NOT NULL DEFAULT '',
  user_lastname varchar(50) COLLATE NOT NULL DEFAULT '',
  user_email varchar(100) COLLATE NOT NULL DEFAULT '',
  user_registered datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  user_status int(11) NOT NULL DEFAULT '0',

)