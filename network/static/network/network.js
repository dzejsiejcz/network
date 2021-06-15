document.addEventListener('DOMContentLoaded', function() {
    
    document.querySelectorAll('#compose-view').forEach(div => {
        div.style.display = 'none'
    });

    // document.querySelectorAll('#posty').forEach(div => {
    //     div.style.display = 'block';
    // })


    //view newpost
    let newpost = document.querySelector('#new-post');
    if (newpost !== null) {
        newpost.addEventListener('click', () => new_post());
    }

    //edycja postu
    document.querySelectorAll(".edy").forEach(div => {
        div.style.display = 'none';
    });

    document.querySelectorAll('#edit').forEach(button => {
        
        button.onclick = function() {
            id = button.dataset.edit;

            document.querySelector(`#one_post-${id}`).style.display = 'none';
            document.querySelector(`#edit-${id}`).style.display = 'block';
            
        }; 
    });

    document.querySelectorAll('#edit-form').forEach(form => {
        form.onsubmit = function() {
            id = form.dataset.editform;
            text = document.querySelector(`#edit-body-${id}`).value
            fetch(`/post/edit/${id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    body: text
                })
            // })
            // .then(async(response) => {
            // document.querySelector(`#one_post-${id}`).style.display = 'block';
            // document.querySelector(`#edit-${id}`).style.display = 'none';
            // console.log(response);
            // // location.reload();
            // // return false;
            })
        };
    });

    document.querySelectorAll('#anuluj-button').forEach(button => {
        
        button.onclick = function() {
            id = button.dataset.anuluj;
 
            document.querySelector(`#one_post-${id}`).style.display = 'block';
            document.querySelector(`#edit-${id}`).style.display = 'none';
            
        }; 
    });
    
    // usuwanie postu

    document.querySelectorAll('#delete').forEach(button => {
        
        button.onclick = function() {
            id = button.dataset.delete;
            // console.log(id);
            document.querySelector(`#one_post-${id}`).style.display = 'none';
            fetch(`/post/delete/${id}`)
            .then();            
        }; 
    });
    
    
    // liczba lajków
    document.querySelectorAll('#liked').forEach(div => {
        // console.log(div.dataset.number);
        fetch(`/likes/${div.dataset.number}`)
        .then(response => response.json())
        .then(a => {
            if (a.a !== 0) {
                div.innerHTML = `Likes: ${a.a}`;
                // console.log(a.a);
            } else {
                div.innerHTML = ``;
                // console.log(a.a);
            }
        })
    });

    // like or unlike
    document.querySelectorAll("#like").forEach(button => {
        id = button.dataset.like
        fetch(`/liked/${id}`)
        .then(response => response.json())
        .then(liked => {
            if (liked.liked === true) {
                button.innerHTML = 'Nie lubię <img src="/static/network/unlike.jpg" alt="Unlike">';
                button.title = "Unlike";
            } else {
                button.innerHTML = 'Lubię to <img src="/static/network/like.jpg" alt="Like">';
                button.title = "Like";
            }
            button.onclick = function() {
                id = button.dataset.like
                fetch(`/liking/${id}`);
                setTimeout(function() {
                    fetch(`/likes/${id}`)
                    .then(response => response.json())
                    .then(a => {
                        if (a.a !== 0) {
                            document.querySelector(`div[data-number='${id}']`).innerHTML = `Likes: ${a.a}`;          
                        } else {
                            document.querySelector(`div[data-number='${id}']`).innerHTML = ``;
                        }
                    });
                }, 100);
                setTimeout(function() {
                    fetch(`/liked/${id}`)
                    .then(response => response.json())
                    .then(liked => {
                        if (liked.liked === true) {
                            button.innerHTML = 'Nie lubię <img src="/static/network/unlike.jpg" alt="Like">'
                        } else {
                            button.innerHTML = 'Lubię to <img src="/static/network/like.jpg" alt="Like">'
                        }
                    })
                }, 100);
            }
        })
    })


    // przycisk follow-unfollow

    const follow = document.querySelector('#follow-unfollow');
        if (follow !== null) {
            friend = follow.dataset.user;
            console.log(friend);
            fetch(`/following/checking/${friend}`)
            .then(response => response.json())
            .then(has_followed => {
                console.log(has_followed, "checking");
                if (has_followed.has_followed === true) {
                    follow.innerHTML = `<div id="unfollow" data-friend="${friend}"> Usuń z obserwowanych</div>`;    
                } if (has_followed.has_followed === false) {
                    follow.innerHTML = `<div id="follow" data-friend="${friend}"> Dodaj do obserwowanych</div>`;
                }
            })
            follow.addEventListener('click', event => {
                const action = event.target;
                friend = action.dataset.friend;
                console.log(friend);
                if (action.id === 'unfollow') {
                    fetch(`/following/unfollow/${friend}`)
                } else if (action.id === 'follow') {
                    fetch(`/following/follow/${friend}`)
                }
                location.reload();
            });
        }
});

// funkcja do obsługi view new-post
function new_post() {
    // history.pushState({}, "", "NewPost");
    document.querySelector('#new-post').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';
    document.querySelector('#compose-form').onsubmit = function() {
        text = document.querySelector('#compose-body').value
        if (text !== "") {
            fetch('posts', {
                method: 'POST',
                body: JSON.stringify({
                    body: text
                })
            })
            .then(async(response) => {
                if (response.status === 201) {
                    alert("Post created successfully.");  
                }
            })
        }
            
        }
    };
