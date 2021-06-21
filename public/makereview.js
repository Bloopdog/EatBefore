var user_id = sessionStorage.getItem("user_id");
var user_name = sessionStorage.getItem("user_name");
var error_place = true;
var error_rating = true;
var error_title = true;
var error_reviewContent = true;
var error_img = true;

function showError(message) {
    var errorMsg = `
        <div class="alert alert-danger mt-3" role="alert" id="error-div">
            <h4 class="alert-heading">${message}</h4>
            <p class="mb-0">Please try again!</p>
        </div>
    `;
  $('#error-div').replaceWith(errorMsg);
};

//Google Autocorrect
let autocomplete;
function initAutocomplete() {
    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById('input'),
        {
            types: ['establishment'],
            componentRestrictions : {'country': ['SG']},
            fields: ['all']
        }
    );

    autocomplete.addListener('place_changed', function() {
        var place = autocomplete.getPlace();
        if (!place.place_id) {
            $('#input').addClass("is-invalid");
            document.getElementById('validity').innerText = 'Invalid Location';
            error_place = true;
            validate_errors();
        }
        
        else {
            $('#input').addClass("is-valid");
            document.getElementById('validity').innerText = 'Location is valid';
            document.getElementById('placeID').value = autocomplete.getPlace().place_id;
            document.getElementById('placeName').value = autocomplete.getPlace().name;
            error_place = false;
            validate_errors();
        }
    })

}

document.getElementById('rating').addEventListener("change", function() {
    //console.log("Rating validation");
    input = document.getElementById('rating').value;
    if (input != ' -- Select an option -- ') {
    error_rating = false;
    validate_errors();
    }
})

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

document.getElementById('img').addEventListener("change", function() {
    //console.log("Image validation");
    input = document.getElementById('img').value;
    if (input != "") {
        error_img = false;
        validate_errors();
    }
    else {
        error_img = true;
        validate_errors();
    }
})

function validate_errors() {
    if (error_place == false & error_rating == false & error_title == false & error_reviewContent == false & error_img == false) 
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
            sendReview();
            return y
          }
      })
      .catch(error => console.log('error', error))
  }

// Convert image to base64
document.querySelector('#img').addEventListener("change", function () {
    // console.log(this.files);
    const reader = new FileReader();

    reader.addEventListener("load", () => {
        image64inner = reader.result;
        image64inner = image64inner.replace(/^data:image\/[a-z]+;base64,/, "");
    })
    
    reader.readAsDataURL(this.files[0]);
});

async function sendReview() {
    var placeName = $('#placeName').val();
    var placeID = $('#placeID').val();
    var rating = $('#rating').val();
    var title = $('#title').val();
    var reviewContent = $('#reviewContent').val();
    var serviceURL = "http://127.0.0.1:5203/storereview";
    try {
        const response = await fetch(serviceURL, {
            method: 'POST',
            headers: {"Content-Type": "application/json"},
            body : JSON.stringify({
                user_id: user_id,
                user_name: user_name,
                place_id: placeID,
                place_name: placeName,
                rating: rating,
                review_title: title,
                review_text: reviewContent,
                likes: 0,
                views:0,
                imageurl: image64inner
            })
        });
        const result = await response.json();
        if(response.status === 201) {
            window.location.href = "index.html";
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
  
$('#addReviewForm').submit(function(event) {
    event.preventDefault();
    var title = $('#title').val();
    var reviewContent = $('#reviewContent').val();
    var combinedString = title + " " + reviewContent;
    words(combinedString);
})