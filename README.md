# Posta - Comprehensive Technical Documentation

## 1. Project Overview
**Posta** is a full-featured, sleek social media platform designed for seamless user interaction, real-time updates, and community building. Built with a robust Django backend and a dynamic JavaScript frontend, Posta allows users to share short-form text content, engage with others through follows and likes, and manage their social presence without the friction of constant page reloads.

The platform solves the problem of "static" web experiences by leveraging the Fetch API to perform background data synchronization, ensuring that actions like liking a post or editing content feel instantaneous and modern.

---

## 2. Project Structure & Breakdown

The repository follows a standard Django project structure but is organized to separate the core application logic from project-wide configurations.

### **`project4/` (Main Project Directory)**
This directory serves as the root of the Django environment.
*   **`project4/` (Internal Folder):** Contains project-wide settings, URL routing (`urls.py`), and WSGI/ASGI configurations.
*   **`network/` (Primary Application):** The heart of the platform. It houses all social media logic, including:
    *   **Models:** Data structures for Users and Posts.
    *   **Views:** Controller logic for rendering templates and handling API requests.
    *   **Templates:** HTML structure using Django's templating engine.
    *   **Static Files:** Custom CSS for the "dark mode" aesthetic and JavaScript for dynamic interactions.
*   **`db.sqlite3`:** The local development database.
*   **`manage.py`:** Django's command-line utility for administrative tasks.
*   **`requirements.txt`:** List of Python dependencies (Django 3.0.2).

### **Inter-module Interaction**
The `project4` configuration routes all traffic to the `network` application via `include("network.urls")`. Static files are served via Django's `staticfiles` app, with a centralized `layout.html` providing a consistent navigation bar and styling across all views.

---

## 3. Exhaustive Feature List

### **User Management & Authentication**
*   **User Registration:** New users can create accounts with a username, email, and password.
*   **Secure Authentication:** Standard login/logout flow powered by Django's `auth` framework.
*   **Custom User Profiles:** Every user has a dedicated profile page (`/profile/<username>`) displaying their stats and post history.

### **Social Interaction System**
*   **Follow/Unfollow:** Users can follow other users from their profile pages. This relationship is non-symmetrical (User A follows User B, but User B doesn't necessarily follow User A).
*   **Follower/Following Counts:** Real-time (on-refresh) display of social reach on profile pages.
*   **Following Feed:** A personalized "Following" view that aggregates posts only from users the current user follows.

### **Content Engine**
*   **Post Creation:** Authenticated users can drop new posts from the "All Posts" or "Profile" pages.
*   **Feed Pagination:** Both the global feed and the personal/following feeds are paginated (10 posts per page) to ensure optimal performance and readability.
*   **Global "All Posts" Feed:** A chronological stream of all public posts from every user.

### **Dynamic UI Features (JavaScript Power)**
*   **In-Place Editing:** Users can edit their own posts directly on the page. Clicking "Edit" replaces the text with a textarea, allowing updates without a page reload.
*   **Asynchronous Liking:** A "Like" system where clicking the heart/like button updates the count and state instantly via the Fetch API.
*   **No-Reload Post Creation:** Submitting the new post form updates the database via API, though the current implementation triggers a reload to refresh the feed (can be further optimized).

---

## 4. Technical Architecture & Tech Stack

### **Backend Architecture**
*   **Framework:** Django 3.0.2 (Python-based).
*   **Pattern:** Model-Template-View (MTV).
*   **Database:** SQLite3 (Relational).
*   **Security:**
    *   `@login_required` decorators for protected routes.
    *   CSRF tokens for form submissions.
    *   `@csrf_exempt` on API endpoints with internal session-based authentication checks.

### **Frontend Architecture**
*   **Styling:** Bootstrap 4.4.1 for responsive layout and UI components.
*   **Vanilla JavaScript:** Custom logic in `index.js` handles all Fetch API calls and DOM manipulation.
*   **Custom CSS:** A deep-dark theme implemented in `styles.css` with responsive media queries for mobile and desktop optimization.

### **Data Schema**
*   **`User` (extends `AbstractUser`):**
    *   `followers`: Many-to-Many relationship with `self` (non-symmetrical).
*   **`Post`:**
    *   `user`: ForeignKey to `User`.
    *   `content`: TextField for post body.
    *   `timestamp`: DateTimeField (auto-populated).
    *   `like_count`: PositiveIntegerField.
    *   `liked_by`: Many-to-Many relationship with `User`.

---

## 5. Under-the-Hood Optimizations

*   **Efficient Querying:** Uses `.order_by("-timestamp")` and `Paginator` to handle large volumes of posts efficiently.
*   **Frontend State Management:** JavaScript maintains an `isEditing` state to prevent multiple concurrent edits and ensure UI consistency.
*   **Dynamic DOM Injection:** Post editing transforms static text into editable fields and back, preserving the original styling.
*   **Mobile-First Design:** CSS includes breakpoints at 700px and 1000px to adjust content width for different screen sizes.
*   **API Design:** Internal "pseudo-REST" endpoints return JSON for easy consumption by the frontend.

---

## 6. Setup & Installation Instructions

### **Prerequisites**
*   Python 3.8 or higher.
*   `pip` (Python package installer).

### **Step-by-Step Installation**

1.  **Clone the Repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r project4/requirements.txt
    ```

3.  **Apply Database Migrations:**
    ```bash
    cd project4
    python manage.py makemigrations network
    python manage.py migrate
    ```

4.  **Create a Superuser (Optional - for Admin Access):**
    ```bash
    python manage.py createsuperuser
    ```

5.  **Run the Development Server:**
    ```bash
    python manage.py runserver
    ```

6.  **Access the App:**
    Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## 7. Usage Examples

### **API Endpoints**

#### **Create a New Post**
*   **URL:** `/new_post/`
*   **Method:** `POST`
*   **Body:** `{"content": "Hello World!"}`
*   **Success Response:** `201 Created` - `{"message": "Post created successfully!", "id": 1}`

#### **Edit a Post**
*   **URL:** `/edit_post/<post_id>`
*   **Method:** `PUT`
*   **Body:** `{"content": "Updated content"}`
*   **Success Response:** `200 OK` - `{"message": "Post updated successfully!", "id": 1}`

#### **Toggle Like**
*   **URL:** `/like_post/<post_id>`
*   **Method:** `PUT`
*   **Success Response:** `200 OK` - `{"message": "Like status updated.", "like_count": 5}`

### **Frontend Interactions**
*   **Following a User:** Navigate to any profile page (e.g., `/profile/johndoe`) and click the **Follow** button. The button will dynamically toggle to **Unfollow**.
*   **Viewing Following Feed:** Click **Following** in the navigation bar to see a curated feed of posts from people you know.
