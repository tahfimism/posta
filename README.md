# **Posta**  
**A sleek social media platform for sharing, connecting, and vibing.**

![Posta Preview](https://github.com/user-attachments/assets/68dd1a11-bd38-4000-92e9-8678bddb7f76)

---

## **Core Vibe**  
Posta lets users drop **short text posts**, follow others, and engage with content in a slick, dynamic interface. Create, edit, and like posts without clunky page reloads.

---

## **Features**  

### **1. Auth Game Strong**  
- 🟢 **Register**: New users join the party.  
- 🔐 **Login/Logout**: Secure sign-in and sign-out.

### **2. Post Power**  
- ✍️ **Create**: Authenticated users post from the main or profile page.  
- 📜 **View All**: Paginated feed of everyone's posts.  
- ✏️ **Edit**: Tweak your posts dynamically with JS.  
- ❤️ **Like/Unlike**: Like or unlike posts with real-time count updates.

### **3. Social Sparks**  
- 👤 **Profiles**: Show off your posts, followers, and following stats.  
- 🤝 **Follow/Unfollow**: Connect or disconnect from user profiles.  
- 📰 **Following Feed**: Chronological posts from those you follow.

### **4. Smooth Frontend**  
- ⚡ **Dynamic AF**: JavaScript + Fetch API for seamless post creation, editing, liking, and following.  
- No page refreshes, just pure flow.

---

## **Tech Breakdown**  

### **Backend (Django)**  
- **Models**:  
  - 🧑 `User`: Extends `AbstractUser` with a followers/following system.  
  - 📝 `Post`: Tracks content, author, timestamp, likes, and likers.  
- **Views & URLs**:  
  - Function-based views for HTML rendering (`index`, `profile`, `login`).  
  - API endpoints (`edit_post`, `like_post`, `follow_user`) return `JsonResponse`.  
- **Security**:  
  - 🔒 `@login_required` locks down sensitive views.  
  - 🛡️ `@csrf_exempt` for API endpoints, secured by session checks.  
  - Post edits verify ownership.  
- **Pagination**:  
  - 📄 10 posts per page for "All Posts", "Following", and profiles.

### **Frontend**  
- 🎨 **Templates**: Django Templating with `layout.html` for consistency.  
- 💅 **Styling**: Bootstrap for a clean, responsive look.  
- 🚀 **JavaScript** (`network/static/network/index.js`):  
  - Handles dynamic actions (edit, like, follow) with `fetch` API.  
  - Updates DOM for instant feedback.

---

## **API Endpoints**  
Powering the dynamic frontend with REST-like vibes:  
- `POST /new_post/`: Drop a new post.  
- `PUT /edit_post/<int:post_id>`: Update your post.  
- `PUT /like
