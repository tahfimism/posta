console.log("index.js loaded");


document.addEventListener('DOMContentLoaded', function() {

    
    // follow and unfollow buttons
    const follow_button = document.querySelector('#follow-button');
    if (follow_button) {
        follow_button.onclick = function() {
            const userId = follow_button.dataset.userid; // Get the user ID from the button's data attribute
            fetch(`/follow/${userId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(result => {
                // Update button text and state
                console.log(result);
                if (result.error) {
                    alert(result.error);
                } else {
                    follow_button.textContent = result.following ? 'Unfollow' : 'Follow';
                    follow_button.classList.toggle('btn-primary');
                    follow_button.classList.toggle('btn-secondary');
                }
            });
        }
    }


    // toggle between "All Posts" and "Following" posts
    const allPostsButton = document.querySelector('#all-posts');
    const followingPostsButton = document.querySelector('#following-posts');
    const index_title = document.querySelector('#index_title');
    
  


    // new post submission
    const newPostForm = document.querySelector('#new_post_form');
    if (newPostForm) {
       newPostForm.onsubmit = function(event) {

            event.preventDefault();
            const postContent = document.querySelector('#post-content').value;

            fetch('/new_post/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    content: postContent
                })
            })
            .then(response => response.json())
            .then(result => {
                // Print result
                console.log(result);
                const message = document.querySelector('#message');
                if (result.error) {
                    alert(result.error);
                } 
                else if (result.message) {
                    document.querySelector('#post-content').value = ''
                    location.reload();
                }
            }); 

        }
    }



// button event listeners

    // is editing post ?
    let isEditing = false;

    document.addEventListener('click', function(event) {
        const event_element = event.target;

        // edit post event
        if (event_element.classList.contains('post_edit_button')) {
            event.preventDefault();

            // is already editing a post ?
            if (isEditing) {
                alert("Finish editing the current post before editing another.");
                return;
            }
            isEditing = true;

            // definign some values
            const postId = event_element.dataset.postid;
            const postContent = event_element.closest('.post').querySelector('.post-content');
            const post_content_text = postContent.textContent.trim();
            
            postContent.innerHTML = `
                <textarea id="edit-post-content" rows="3" class="form-control">${post_content_text}</textarea>
                <button class="btn btn-primary mt-2" id="save-post-button">Save</button>
            `
            // Store the edit button
            const originalEditButton = event_element;
            const floatEndSpan = event_element.closest('.post').querySelector('.float-end');

            // remove the edit button temporarily
            event_element.remove();

            saveButton = document.querySelector('#save-post-button');
            saveButton.onclick = function() {
                const editedContent = document.querySelector('#edit-post-content').value;
                if (editedContent === '') {
                    alert("Post content cannot be empty.");
                    return;
                }
                // Send the edited content to the server
                fetch(`/edit_post/${postId}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        content: editedContent
                    })
                })
                .then(response => response.json())
                .then(result => {
                    console.log(result);
                    if (result.error) {
                        alert(result.error);
                    } else {
                        postContent.innerHTML = `${editedContent}`;
                        
                    }

                    // restore the edit button
                    
                    floatEndSpan.insertBefore(originalEditButton, floatEndSpan.firstChild);

                });
            }

    
        }

        // like button event
        if (event_element.classList.contains('like_button')) {
            event.preventDefault();
            
            const postId = event_element.dataset.postid; 
            fetch(`/like_post/${postId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(result => {
                // Update like count
                console.log(result);
                if (result.error) {
                    alert(result.error);
                } else {
                    document.querySelector(`#like_count_${postId}`).textContent = ` ${result.like_count} likes`;
                }
            });
        }
    });
})
