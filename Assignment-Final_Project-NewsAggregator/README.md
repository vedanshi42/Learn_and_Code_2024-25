# News Aggregator - Project Documentation

## Overview
The News Aggregator project is a modular, client-server system that periodically fetches news from external APIs, stores it in a database, and provides personalized notifications to users based on their keyword and category preferences. Users interact via a CLI, while an admin manages the system.

---

## Key Entities and Their Roles

### 1. **User**
- Attributes: `username`, `email (unique)`, `password`, `role`
- Admin is seeded once; all others sign up via CLI.
- Users log in, configure preferences, search, save, and receive article notifications.

### 2. **Article**
- Fetched every 3–4 hours.
- Categorized via logic or admin-configured list.
- Duplicates are detected and discarded.

### 3. **Category**
- Predefined and managed by admin.
- Used in both article classification and user preferences.

### 4. **Keyword**
- Custom words defined per user for news matching.

### 5. **NotificationConfig**
- User-specific.
- Holds keywords and categories.
- Referenced after every article refresh.

### 6. **UserNotification**
- Holds only latest matched articles per user.
- Cleared and rewritten after each fetch cycle.
- Used for CLI "View Notifications".

### 7. **SavedArticle**
- Maps user to saved articles (ID-based save/delete).

### 8. **ExternalAPIServer**
- Managed by admin.
- Stores API keys and server status (active/inactive).

---

## Application Flow

### 1. Admin Setup
- Admin added via `seed_admin.py`.
- Uses a dedicated noreply email account for notifications.

### 2. Signup/Login System
- Checks for **duplicate email** on sign-up.
- Has role-based login: admin vs user.
- Login uses hashed password check.

### 3. API News Fetching
- Triggered on schedule (`schedule` module).
- Calls NewsAPI and TheNewsAPI.
- De-duplicates and stores only new articles.
- Articles are categorized or defaulted to "All".
- Server marked `Active` or `Inactive` based on fetch response.

### 4. Notification Processing
- Clears `user_notifications` table.
- For each user, match new articles to keywords or categories.
- Send one combined email.
- Store latest notifications in DB for viewing via CLI.

### 5. CLI Features (User)
- View headlines by date, category, or today.
- Search by keyword/category.
- Save/Delete articles.
- Configure notification preferences.
- View latest notification matches.
- Each menu has `Back` and `Logout` options.

### 6. CLI Features (Admin)
- View/update external server config.
- View API status and last accessed timestamp.
- Add new categories.
- Logout and return.

---

## Tech Stack

| Layer         | Tool/Tech              |
|---------------|------------------------|
| Database      | PostgreSQL             |
| Server        | Python + FastAPI       |
| Client        | Python CLI             |
| Email         | Gmail SMTP + smtplib   |
| Scheduling    | schedule               |
| Password Hash | bcrypt                 |
| Config Mgmt   | python-dotenv          |

---

## Security
- Admin seeded manually, role-controlled logic
- Passwords are hashed (bcrypt)
- Email/password never stored in plaintext
- `.env` file used for credentials and secrets
- Unique constraint ensures duplicate users can’t register

---

## Setup Instructions

1. Create and activate virtual environment
2. Run `pip install -r requirements.txt`
3. Create PostgreSQL DB and run `schema.sql`
4. Add `.env` with DB and email credentials
5. Run `seed_admin.py` to insert admin
6. Start server via `server/app.py`
7. Start CLI via `client/main.py`

---

## Testing
- Unit tests exist under `/server/tests/`
- Use `pytest` to run all test modules
