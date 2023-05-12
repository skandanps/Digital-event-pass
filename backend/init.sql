CREATE TABLE department (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) UNIQUE NOT NULL,
    description VARCHAR(250),
    created_on DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_updated_on DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE event (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    venue VARCHAR(50) NOT NULL,
    date TIMESTAMP NOT NULL,
    description TEXT,
    image_url VARCHAR(100)
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    email VARCHAR(120) NOT NULL,
    address VARCHAR(250) NOT NULL,
    barcode VARCHAR(50) NOT NULL,
    created_on DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_updated_on DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (username),
    UNIQUE (phone_number),
    UNIQUE (email),
    UNIQUE (barcode)
);

CREATE TABLE user_event (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    event_id INTEGER NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    event_time TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    notified BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (event_id) REFERENCES event (id)
);
