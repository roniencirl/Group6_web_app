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
