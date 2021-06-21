var user_id = sessionStorage.getItem("user_id");
var user_name = sessionStorage.getItem("user_name");
var error_comment = true;

function showError(message) {
    var errorMsg = `
        <div class="alert alert-danger mt-3" role="alert" id="error-div">
            <h4 class="alert-heading">${message}</h4>
            <p class="mb-0">Please try again!</p>
        </div>
    `;
    $('#error-div').replaceWith(errorMsg);
};

function words(comment) {
    var myHeaders = new Headers();
    myHeaders.append("apikey", "JkeTyo27pt8NCbZ2NlQei3XORis6Iit7");
  
    var raw = comment;
    //bad words API doesn't accept newline in string input, therefore I had to add the following line
    raw = raw.replace(/(\r\n|\n|\r|&)/gm," ");
    var wordArr = comment.split(' ');
  
    var requestOptions = {
      method: 'POST',
      redirect: 'follow',
      headers: myHeaders,
      body: raw
    };

    // Our own defined list of badwords:
    local_bad_words_list = ['cb','knnb','pukimak','ccb','lanjiao','lan jiao','knn','knnccb', 'wtf', 'buto', 'anjing', 'kys', 'babi', 'fook', 'fak', 'cunt', 'sh1t', 'useless'];
  
    //initialise no_bad_words
    var no_bad_words = 0;

    fetch("https://api.promptapi.com/bad_words?censor_character=*", requestOptions)
      .then(response => response.text())
      .then(result => {
        no_bad_words = JSON.parse(result).bad_words_total
        //check through with our own defined list of bad words too
        var wordLength = wordArr.length;
        for (var i = 0; i < wordLength; i++) {
          if (local_bad_words_list.includes(wordArr[i])) {
            // console.log('Local bad words detected')
            no_bad_words += 1;
          }
        }
        if (no_bad_words > 0) {
            // console.log("Bad words detected");
            var x = true;
            $('#error-div').replaceWith(`
                <div class="alert alert-danger" role="alert" id="error-div">
                    <h4 class="alert-heading">Vulgarities Detected!</h4>
                    <p>Please do not include vulgarities in your comment! Keep it civil!</p>
                </div>`);
            return x
          }
        else {
            // console.log("No bad words detected")
            var y = false;
            $('#error-div').replaceWith(`<div id="error-div"></div>`);
            sendComment();
            return y
          }
      })
      .catch(error => console.log('error', error))
  }

  function loadLikes(review_id) {    
    var serviceURL = "http://127.0.0.1:5001/review/" + review_id;
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var response = JSON.parse(this.responseText);
            var likes = response.data.review.likes;
            $('#likesSection').html(`
                <button class="btn btn-primary" type="button" id="like">
                    <i class="fas fa-thumbs-up"></i> Like
                </button>
                ${likes} likes
            `);
      }
    };
    xhttp.open("GET", serviceURL, true);
    xhttp.send();
}

function loadComments(review_id) {    
    var serviceURL = "http://127.0.0.1:5001/review/" + review_id;
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var response = JSON.parse(this.responseText);
            var comments = response.data.comments;
            var rows = "";
            
            for (const comment of comments) {
                eachRow = 
                    `<li class="list-group-item" aria-disabled="true">
                        <div class="d-flex w-100 justify-content-between">
                            <h5 class="mb-1" id="user_name">${comment.user_name}</h5>
                            <small id="date">${comment.comment_created}</small>
                        </div>
                        <p class="mb-1" id="comment_text">${comment.comment_text}</p>
                    </li>`
                rows += eachRow;
            }
            if (user_id) {
                rows += 
                `<li class="list-group-item" aria-disabled="true" id="comment_input">
                    <form id="addCommentForm">
                        <div class="form-floating mb-2">
                            <textarea class="form-control" placeholder="Leave a comment here" id="comment" style="height: 100px"></textarea>
                            <label for="comment">Comments</label>
                        </div>
                        <button type="button" id="formSubmit" class="btn btn-primary">Submit</button>
                    </form>
                </li>`
            }
            $('#comment_section').html(rows);
            document.getElementById("formSubmit").setAttribute("class", "btn btn-primary disabled");
            document.getElementById('comment').addEventListener("change", function() {
                //console.log("comment validation");
                input = document.getElementById('comment').value;
                if (input != "" && input !="Comments") {
                    error_comment = false;
                    validate_errors();
                }
                else {
                    error_comment = true;
                    validate_errors();
                }
              })
            $('#formSubmit').click(async(event) => {
                event.preventDefault();
                var comment = $('#comment').val();
                words(comment);
            })
      }
    };
    xhttp.open("GET", serviceURL, true);
    xhttp.send();
}

async function sendComment(){
    var comment = $('#comment').val();
    var urlParams = window.location.search;
    var pos = urlParams.indexOf('=') + 1;
    var review_id = parseInt(urlParams.substr(pos));
    var serviceURL = "http://127.0.0.1:5001/review/comment";


    try {
        const response = await fetch(serviceURL, {
            method: 'POST',
            headers: {"Content-Type": "application/json"},
            body : JSON.stringify({
                review_id: review_id,
                user_id: user_id,
                user_name: user_name,
                comment_text: comment,
                comment_likes: 0
            })
        });
        console.log(JSON.stringify({
            review_id: review_id,
            user_id: user_id,
            user_name: user_name,
            comment_text: comment,
            comment_likes: 0
        }));
        const result = await response.json();
        if(response.status === 201) {
            loadComments(review_id);
        } else if(response.status == 400 || response.status == 500) {
            showError(result.message);
        } else {
            throw response.status;
        }
    } catch(error) {
        showError('There is a problem retrieving comment data, please try again.<br />' + error);
    }   
}

$(async() => {
    var urlParams = window.location.search;
    var pos = urlParams.indexOf('=') + 1;
    var review_id = parseInt(urlParams.substr(pos));
    
    var serviceURL = "http://127.0.0.1:5201/view_review/" + review_id;
    
    try {
        const response = 
            await fetch(
                serviceURL, {method: 'GET'}
            );
        const result = await response.json();
        if (response.status === 200) {
            var review = result.data.review;
            $('#placeName').text(review.place_name);
            $('#reviewSubtext').text(review.user_name + " Eat Before on " + review.created);
            $('#reviewContent').html(`
                <h5>${review.review_title}</h5>
                <p>${review.review_text}</p>
                <p class="fw-bold">Rating: ${review.rating}/5</p>
                <div id="likesSection">
                    <button class="btn btn-primary" type="button" id="like">
                        <i class="far fa-thumbs-up"></i> Like
                    </button>
                    ${review.likes} likes
                </div>
            `);
            $("#reviewImg").attr("src", review.imageurl);
            loadComments(review.review_id);
        } else if (response.status == 404) {
            showError(result.message);
        } else {
            throw response.status;
        }
    } catch(error) {
        showError('There is a problem retrieving reviews data, please try again later.<br />' + error);
    }

    $('#like').click(async(event) => {
        event.preventDefault();
        var serviceURL = "http://127.0.0.1:5001/review/likes/" + review_id;
    
        try {
            const response = 
                await fetch(
                    serviceURL, {method: 'PUT'}
                );
            const result = await response.json();
            if (response.status === 200) {
                loadLikes(review_id);
            } else if (response.status == 404) {
                showError(result.message);
            } else {
                throw response.status;
            }
        } catch(error) {
            showError('There is a problem retrieving reviews data, please try again later.<br />' + error);
        }
    })

    $('#formSubmit').click(async(event) => {
        event.preventDefault();
        var comment = $('#comment').val();
        words(comment);
    })

});


function validate_errors() {
  if (error_comment == false) 
  {
    document.getElementById("formSubmit").setAttribute("class", "btn btn-primary");
  }
  else {
    document.getElementById("formSubmit").setAttribute("class", "btn btn-primary disabled");
  }
}

  