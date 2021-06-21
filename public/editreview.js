var error_title = false;
var error_reviewContent = false;
var urlParams = window.location.search;
var pos = urlParams.indexOf('=') + 1;
var review_id = parseInt(urlParams.substr(pos));

function showError(message) {
    var errorMsg = `
        <div class="alert alert-danger mt-3" role="alert" id="error-div">
            <h4 class="alert-heading">${message}</h4>
            <p class="mb-0">Please try again!</p>
        </div>
    `;
    $('#error-div').replaceWith(errorMsg);
};

document.getElementById('title').addEventListener("change", function() {
    //console.log("Title validation");
    input = document.getElementById('title').value;
    if (input != "") {
        error_title = false;
        validate_errors();
    }
    else {
        error_title = true;
        validate_errors();
    }
})

document.getElementById('reviewContent').addEventListener("change", function() {
    //console.log("Content validation");
    input = document.getElementById('reviewContent').value;
    if (input != "") {
        error_reviewContent = false;
        validate_errors();
    }
    else {
        error_reviewContent = true;
        validate_errors();
    }
})

function validate_errors() {
    if (error_title == false & error_reviewContent == false) 
    {
        //console.log("Validation success");
        document.getElementById("submit").setAttribute("class", "btn btn-primary");
    }
    else {
        //console.log("Validation failed")
        document.getElementById("submit").setAttribute("class", "btn btn-primary disabled");
    }
}

function words(combinedString) {
    var myHeaders = new Headers();
    myHeaders.append("apikey", "JkeTyo27pt8NCbZ2NlQei3XORis6Iit7");
  
    var raw = combinedString;
    // Bad words API doesn't accept newline in string input, therefore I had to add the following line
    raw = raw.replace(/(\r\n|\n|\r|&)/gm," ");
    var wordArr = combinedString.split(' ');
  
    var requestOptions = {
        method: 'POST',
        redirect: 'follow',
        headers: myHeaders,
        body: raw
    };

    // Our own defined list of badwords
    local_bad_words_list = ['cb','knnb','pukimak','ccb','lanjiao','lan jiao','knn','knnccb', 'wtf', 'buto', 'anjing', 'kys', 'babi', 'fook', 'fak', 'cunt', 'sh1t', 'useless'];
  
    // Initialise no_bad_words
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
                    <p>Please do not include vulgarities in your review! Keep it civil!</p>
                </div>
            `);
            return x
          }
        else {
            // console.log("No bad words detected");
            var y = false;
            updateReview();
            return y
          }
      })
      .catch(error => console.log('error', error))
  }

async function updateReview() {
    var rating = $('#rating').val();
    var title = $('#title').val();
    var reviewContent = $('#reviewContent').val();
    var serviceURL = "http://127.0.0.1:5001/review/" + review_id;
    try {
        const response = await fetch(serviceURL, {
            method: 'PUT',
            headers: {"Content-Type": "application/json"},
            body : JSON.stringify({
                rating: rating,
                review_title: title,
                review_text: reviewContent
            })
        });
        const result = await response.json();
        if(response.status === 200) {
            window.location.href = "user.html";
        }
        else if(response.status == 500) {
            showError(result.message);
        } else {
            throw response.status;
        }
    } catch(error) {
        showError('There is a problem retrieving review data, please try again.<br />' + error);
    } 
}

$(async() => {
    var serviceURL = "http://127.0.0.1:5001/review/" + review_id;
    
    try {
        const response = 
            await fetch(
                serviceURL, {method: 'GET'}
            );
        const result = await response.json();
        if (response.status === 200) {
            var review = result.data.review;
            $('#placeName').val(review.place_name);
            $('#rating').val(review.rating);
            $('#title').val(review.review_title);
            $('#reviewContent').text(review.review_text);
        } else if (response.status == 404) {
            showError(result.message);
        } else {
            throw response.status;
        }
    } catch(error) {
        showError('There is a problem retrieving reviews data, please try again later.<br />' + error);
    }

    $('#editReviewForm').submit(function(event) {
        event.preventDefault();
        var title = $('#title').val();
        var reviewContent = $('#reviewContent').val();
        var combinedString = title + " " + reviewContent;
        words(combinedString);
    })
});