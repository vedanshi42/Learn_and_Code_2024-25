-- USERS TABLE
CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(100),
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(10) CHECK (role IN ('admin', 'user')) DEFAULT 'user'
);

-- CATEGORIES TABLE
CREATE TABLE IF NOT EXISTS categories (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

-- ARTICLES TABLE
CREATE TABLE IF NOT EXISTS articles (
    article_id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT,
    category_id INTEGER REFERENCES categories(category_id),
    source_url TEXT,
    date_published TIMESTAMP
);

-- USER SAVED ARTICLES
CREATE TABLE IF NOT EXISTS user_saved_articles (
    saved_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    article_id INTEGER REFERENCES articles(article_id) ON DELETE CASCADE,
    saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, article_id)
);

-- USER KEYWORDS
CREATE TABLE IF NOT EXISTS keywords (
    keyword_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    keyword TEXT NOT NULL,
    UNIQUE(user_id, keyword)
);

-- USER CATEGORIES (subscriptions)
CREATE TABLE IF NOT EXISTS user_categories (
    user_category_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    category_id INTEGER REFERENCES categories(category_id),
    UNIQUE(user_id, category_id)
);

-- NOTIFICATIONS TABLE
CREATE TABLE IF NOT EXISTS user_notifications (
    notification_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    article_id INTEGER REFERENCES articles(article_id),
    notified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, article_id)
);

-- EXTERNAL API SERVERS
CREATE TABLE IF NOT EXISTS external_api_servers (
    api_id SERIAL PRIMARY KEY,
    api_name TEXT UNIQUE NOT NULL,
    api_key TEXT NOT NULL,
    status VARCHAR(10) CHECK (status IN ('Active', 'Inactive')) DEFAULT 'Active',
    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
