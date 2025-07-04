console.log("index.js loaded");




function load_posts(filter = 'all') {

        // Clear existing posts
        console.log(`Loading posts with filter: ${filter}`);
        
        // Select the posts container
        const postsContainer = document.querySelector('#posts-container');
        postsContainer.innerHTML = ''; // Clear existing posts


        // Fetch posts from the server
        fetch(`/load_posts/${filter}`)
            .then(response => response.json())
            .then(posts => {
                const postsContainer = document.querySelector('#posts-container');
                posts.forEach(post => {
                    const postElement = document.createElement('div');
                    postElement.className = 'post';
                    postElement.innerHTML = `
                    <div class="post-header">
                        <a href="/profile/${post.user}"> <strong>${post.user}</strong> </a>
                        <span class="text-muted float-end" style="font-size: small;">${post.timestamp}</span>
                    </div>
                    <hr class="my-2">
                    <div class="post-content">
                        ${post.content}
                    </div>
                    <div class="post-actions">
                        <button class="btn btn-link">Like</button> <span class="text-muted" id="like_count"> ${post.like_count} likes</span>
                    </div>
                    `;


                    // Add event listener for the like button
                    postElement.querySelector('.btn-link').addEventListener('click', function() {
                        fetch(`/like_post/${post.id}/`, {
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
                            }
                            else  {
                                postElement.querySelector('#like_count').textContent = ` ${result.like_count} likes`;
                            }
                        });
                    });


                    postsContainer.appendChild(postElement);
                });
            });
    }
    











document.addEventListener('DOMContentLoaded', function() {

    


    // toggle between "All Posts" and "Following" posts
    const allPostsButton = document.querySelector('#all-posts');
    const followingPostsButton = document.querySelector('#following-posts');
    const index_title = document.querySelector('#index_title');
    
  


    // new post submission
    document.querySelector('#new_post_form').onsubmit = function(event) {

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
                message.innerHTML = result.error;
            } 
            else if (result.message) {
                message.innerHTML = result.message;
                // Optionally, you can clear the form after submission
                document.querySelector('#post-content').value = '';
                // Reload the page to see the new post
                location.reload();
            }
        }); 

    }

});