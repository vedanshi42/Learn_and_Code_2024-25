# News Aggregator - Project Documentation (NewsViews)

## Overview
The News Aggregator project (NewsViews) is a modular, client-server system that periodically fetches news from multiple external APIs, stores it in a PostgreSQL database, and provides personalized notifications to users based on their keyword and category preferences. Users interact via a CLI, while an admin manages the system, categories, keywords, article-reports and external API configurations.

---

## Key Entities and Their Roles

### 1. **User**
- Attributes: `username`, `email (unique)`, `password`, `role` (admin/user)
- Admin is seeded once; all others sign up via CLI.
- Users log in, configure notification preferences, search, save, and receive article notifications.
- Can view, save, and delete articles; configure categories and keywords for notifications.

### 2. **Article**
- Fetched every 3–4 hours from multiple APIs (NewsAPI, TheNewsAPI, etc.).
- Categorized via ML model or admin-configured list.
- Duplicates are detected and discarded.
- Each article has: `article_id`, `title`, `content`, `category_id`, `source_url`, `date_published`.

### 3. **Category**
- Predefined and managed by admin.
- Used in both article classification and user preferences.
- Admin can add, disable, and manage categories via CLI.

### 4. **Keyword**
- Custom words defined per user for news matching.
- Admin can view and disable keywords globally.

### 5. **NotificationConfig**
- User-specific configuration.
- Holds enabled keywords and categories for each user.
- Referenced after every article refresh to match new articles to user interests.

### 6. **UserNotification**
- Holds only latest matched articles per user.
- Cleared and rewritten after each fetch cycle.
- Used for CLI "View Notifications" and for sending notification emails.

### 7. **SavedArticle**
- Maps user to saved articles (ID-based save/delete).
- Users can view, save, and delete articles from their saved list.

### 8. **ExternalAPIServer**
- Managed by admin.
- Stores API keys and server status (active/inactive).
- Tracks last accessed timestamp and health of each external API.

---

## Application Flow

### 1. Admin Setup
- Admin added via `seed_admin.py` (run once).
- Uses a dedicated noreply email account for notifications.
- Admin can manage external API keys, view server statuses, add/disable categories and keywords, and manage reported articles.

### 2. Signup/Login System
- Users sign up with unique email; duplicate emails are rejected.
- Role-based login: admin vs user.
- Passwords are hashed and checked securely.
- Admin and user have different CLI menus and permissions.

### 3. API News Fetching
- Triggered on schedule (`schedule` module in `server/utils/scheduler.py`).
- Calls multiple news APIs (e.g., NewsAPI, TheNewsAPI) using stored API keys.
- Checks duplicates and stores only new articles in the database.
- Articles are categorized using an ML model or defaulted to "All" if no match.
- Server status is updated to `Active` or `Inactive` based on fetch response.
- All fetches and errors are logged.

### 4. Notification Processing
- After each fetch, clears `user_notifications` table.
- For each user, compares newly fetched articles against their configured keywords and categories to identify relevant matches.
- Sends one combined email per user with all relevant articles.
- Stores latest notifications in DB for viewing via CLI.
- All notification events and errors are logged.

### 5. CLI Features (User)
- View headlines by date, category, or today.
- Also view personalized notifications based on likes, dislikes, reports, saved.
- Search by keyword or category.
- Save and delete articles from personal list.
- Configure notification preferences (categories and keywords).
- View latest notification matches (from DB and email).
- Each menu has `Back` and `Logout` options.
- Robust error handling and user feedback for all actions.

### 6. CLI Features (Admin)
- View/update external server configuration and API keys.
- View external API status and last accessed timestamp.
- Add, disable, and manage categories and keywords.
- View and delete reported articles (with threshold for deletion = 5)..
- Logout and return.
- All admin actions are logged and errors are reported.

---

## Tech Stack

| Layer         | Tool/Tech              
|---------------|-----------------------------
| Database      | PostgreSQL (psycopg)            
| Server        | Python + FastAPI + requests + uvicorn(for server)     
| Client        | Python CLI (terminal)
| Email         | Gmail SMTP + smtplib   
| Scheduling    | schedule               
| Password Hash | bcrypt                 
| Load .env     | python-dotenv        
| ML Model      | scikit-learn, joblib
| Payloads      | pydantic (create base models with parameters sent by clientS)   
| Tabulation    | tabulate (printing results as a table)
| Testing       | pytest + pytest-mock

---

## Security
- Admin seeded manually, role-controlled logic.
- Passwords are hashed (bcrypt).
- Email/password never stored or viewed in plaintext.
- `.env` file used for credentials and secrets.
- Unique constraint ensures duplicate users can’t register and email format is also checked.
- All sensitive actions and errors are logged.

---

## Setup Instructions

1. Create and activate virtual environment
2. Run `pip install -r requirements.txt`
3. Create PostgreSQL DB and run `schema.sql`
4. Add `.env` with DB and email credentials
5. Run `seed_admin.py` to insert admin
6. Start server via 'uvicorn server.server:app'
7. Run 'server/services/train_category_ml_model.py' to ready the ML model.
8. Start 'server/utils/scheduler.py' to fetch news every 3.5 hours and send notifications to users.
9. Run `client/main.py` in bash.

---

## Testing
- Unit tests exist under `/server/tests/`
- Use `pytest` to run all test modules
- All major services are covered by tests
