
/*
CREATE TABLE posts (

    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    post_author bigint(20) UNSIGNED NOT NULL DEFAULT '0',
    post_date datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    post_title text NOT NULL,
    post_content longtext NOT NULL,
    post_modified datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,

);


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
*/

CREATE TABLE users (
  user_id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_login TEXT UNIQUE NOT NULL,
  user_password TEXT NOT NULL,
  user_firstname TEXT NOT NULL,
  user_lastname TEXT NOT NULL, 
  user_email TEXT NOT NULL, 
  user_registered TEXT NOT NULL,
  user_last_login TEXTNOT NULL, 
  user_status TEXT NOT NULL
);


CREATE TABLE groups (
  group_id INTEGER PRIMARY KEY AUTOINCREMENT,
  group_name TEXT UNIQUE NOT NULL
);


CREATE TABLE user_groups (
  user_id INTEGER, 
  group_id INTEGER,
  PRIMARY KEY (user_id, group_id),  
  FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE ON UPDATE NO ACTION,
  FOREIGN KEY (group_id) REFERENCES groups (group_id) ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE TABLE posts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES users (user_id)
);