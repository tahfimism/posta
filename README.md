# posta
Social media site

![Screenshot_4-7-2025_223953_127 0 0 1](https://github.com/user-attachments/assets/68dd1a11-bd38-4000-92e9-8678bddb7f76)


## Core Functionality

The app provides a platform for users to share short text-based posts, follow other users, and interact with content. It features a dynamic frontend that allows for actions like creating posts, editing, and liking without requiring a full page reload.

## Features

### 1. User Authentication
-   **Register:** New users can create an account.
-   **Login/Logout:** Registered users can sign in and out of their accounts.

### 2. Post Management
-   **Create Posts:** Authenticated users can create new posts from the main page and their profile page.
-   **View All Posts:** The main index page displays a paginated list of all posts from all users.
-   **Edit Posts:** Users can edit their own posts directly from the post view. This is handled dynamically using JavaScript.
-   **Like/Unlike Posts:** Authenticated users can like or unlike any post. The like count updates in real-time.

### 3. Social Interaction
-   **User Profiles:** Each user has a public profile page that displays their posts, follower count, and following count.
-   **Follow/Unfollow:** Users can follow or unfollow other users from their profile pages.
-   **"Following" Feed:** A dedicated page shows a chronological feed of posts exclusively from users that the current user follows.

### 4. Dynamic Frontend
-   The application uses JavaScript and the Fetch API to handle key user interactions asynchronously.
-   Actions like creating a new post, editing a post, liking a post, and following a user are performed without a page refresh, providing a smoother user experience.

## Technical Analysis

### Backend (Django)
-   **Models:**
    -   `User`: Extends Django's `AbstractUser` and adds a many-to-many relationship to itself to manage followers and following.
    -   `Post`: Stores the post content, a reference to the author (`User`), a timestamp, a `like_count`, and a `liked_by` many-to-many field to track which users have liked the post.
-   **Views & URLs:**
    -   The app uses function-based views to handle requests.
    -   Standard views render HTML templates for initial page loads (e.g., `index`, `profile`, `login`).
    -   Several views act as API endpoints, receiving `PUT` or `POST` requests from the frontend JavaScript to handle state changes (e.g., `edit_post`, `like_post`, `follow_user`). These views return `JsonResponse` objects.
-   **Security:**
    -   Views requiring authentication are protected with the `@login_required` decorator.
    -   API-like endpoints that modify data are marked with `@csrf_exempt` but are protected by requiring a logged-in session.
    -   Logic for editing posts correctly verifies that the request user is the owner of the post.
-   **Pagination:**
    -   The main "All Posts", "Following", and profile feeds are paginated to efficiently handle a large number of posts, displaying 10 posts per page.

### Frontend
-   **Templates:** Uses the Django Templating Language with a `layout.html` base template for consistent structure.
-   **Styling:** Styled with Bootstrap for a clean and responsive layout.
-   **JavaScript (`network/static/network/index.js`):**
    -   Contains all the client-side logic for dynamic features.
    -   Uses `document.addEventListener` to attach event listeners for clicks on edit, like, and follow buttons.
    -   Employs the `fetch` API to communicate with the Django backend, sending JSON data and updating the DOM based on the response.

## API Endpoints

The application exposes several URL endpoints that behave like a REST API to support the dynamic frontend:

-   `POST /new_post/`: Creates a new post.
-   `PUT /edit_post/<int:post_id>`: Updates an existing post.
-   `PUT /like_post/<int:post_id>`: Toggles the like status for a post.
-   `PUT /follow/<int:user_id>`: Toggles the follow status for a user.
-   `GET /load_posts/<str:filter>`: An endpoint to fetch posts (though not currently used by the primary JS logic).
