# Blogify

Blogify is a full-stack blogging platform built with Django (backend) and React (frontend). It allows users to share stories, connect with others, and explore a world of ideas. The platform supports user authentication, post creation, commenting, category management, and more, providing a modern and interactive blogging experience.

---

## Key Features

- **User Authentication:**
  - Register and log in with secure authentication.
  - Persistent login using tokens.
  - Admin users have access to a management dashboard.

- **Blog Posts:**
  - View a list of the latest blog posts.
  - View detailed post pages with content, author, date, and category.
  - Pagination for browsing posts.

- **Categories:**
  - Browse posts by category.
  - Subscribe or unsubscribe to categories to personalize your feed.

- **Comments & Replies:**
  - Authenticated users can comment on posts.
  - Reply to comments (one reply per comment).
  - View threaded comment discussions.

- **Likes/Dislikes:**
  - React to posts with likes or dislikes (for authenticated users).

- **Admin Management:**
  - Admin users can access the Django admin panel to manage posts, users, categories, and comments.

- **Responsive UI:**
  - Modern, responsive design with a sidebar for categories and a navbar for navigation.
  - User-friendly error handling and loading states.

---

## Tech Stack

- **Frontend:** React, Vite, CSS
- **Backend:** Django, Django REST Framework, SQLite
- **Authentication:** JWT (JSON Web Tokens)
- **Other:** CORS, Django Filters

---

## How to Run

### Backend
1. Install dependencies: `pip install -r requirements.txt`
2. Run migrations: `python manage.py migrate`
3. Start server: `python manage.py runserver`

### Frontend
1. Install dependencies: `npm install`
2. Start development server: `npm run dev`

---

## Contribution

Feel free to fork the repository and submit pull requests for new features, bug fixes, or improvements!
