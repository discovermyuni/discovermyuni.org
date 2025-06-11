console.log("wooo raw js")

let page = 1;
let sort = "newest";
let tags = [];
let authors = [];
let search = "";

// add loading spinner while fetching posts??? may take a while depending on lag
function refreshPosts() {
    fetch(`/api/posts/render-cards/?t=dog`)
        .then(response => response.text())
        .then(html => {
            document.getElementById('posts-list').innerHTML = html;
        })
        .catch(error => console.error('Error loading post:', error));
}
