DROP TABLE IF EXISTS users;

-- Create the 'users' table with the specified structure
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,          -- Unique user ID
    username TEXT NOT NULL UNIQUE,                 -- Unique username
    hashed_password TEXT NOT NULL,                 -- Hashed password (bcrypt hash)
    salt TEXT NOT NULL,                            -- Salt used for hashing
    location TEXT NOT NULL,                        -- User's location
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP  -- Timestamp of account creation
);
