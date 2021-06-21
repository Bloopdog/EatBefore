var user_id = sessionStorage.getItem("user_id");

function showError(message) {
    $('#main-container').append('<label>' + message + '</label>');
};

function loadReviews(user_id) {    
    var serviceURL = "http://127.0.0.1:5001/review/user/" + user_id;
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var response = JSON.parse(this.responseText);
            var reviews = response.data.reviews;
            if (reviews.length != 0) {
                $('#reviewHeader').text("Reviews made by you");

                var tableHead = `
                    <thead>
                        <tr>
                        <th scope="col">#</th>
                        <th scope="col">Place</th>
                        <th scope="col">Review Title</th>
                        <th scope="col">Rating</th>
                        <th scope="col"></th>
                        <th scope="col"></th>
                        </tr>
                    </thead>
                    <tbody id="review_rows">
                        <tr>
                        </tr>
                    </tbody>
                `;
                $('#reviewTable').html(tableHead);

                var rows = "";
                var rowNo = 0;
                for (const review of reviews) {
                    rowNo = rowNo + 1;
                    eachRow = `
                        <tr>
                            <th scope="row">${rowNo}</th>
                            <td>${review.place_name}</td>
                            <td>${review.review_title}</td>
                            <td>${review.rating}</td>
                            <td>
                                <a class="btn btn-primary" href="editreview.html?review_id=${review.review_id}" role="button">Edit</a>
                            </td>
                            <td>
                                <button type="button" class="btn btn-danger" onclick="deleteReview(${review.review_id})" id="deleteBtn">Delete</button>
                            </td>  
                        </tr>
                    `;
                    rows += eachRow;
                }
                $('#review_rows').append(rows);
            } else {
                $('#reviewHeader').text("No reviews made by you");
                $('#reviewTable').html("");
            }
      }
    };
    xhttp.open("GET", serviceURL, true);
    xhttp.send();
}

async function deleteReview(review_id) {
    var serviceURL = "http://127.0.0.1:5001/review/" + review_id;
    try {
        const response = 
            await fetch(
                serviceURL, {method: 'DELETE'}
        );
        const result = await response.json();
        if(response.status === 200) {
            loadReviews(user_id);
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
    var serviceURL = "http://127.0.0.1:5002/user/" + user_id;

    try {
        const response = 
            await fetch(
                serviceURL, {method: 'GET'}
            );
        const result = await response.json();
        if (response.status === 200) {
            var user = result.data;
            $('#username').text(user.user_name);
            $('#email').text(user.email);
            $('#wallet').text('$' + user.wallet_balance);
            $('#views').text(user.total_views);

            if (user.wallet_balance == 0) {
                $("#cashOut").addClass("disabled");
            }
        } else if (response.status == 404) {
            showError(result.message);
        } else {
            throw response.status;
        }
    } catch(error) {
        showError('There is a problem retrieving user data, please try again later.<br />' + error);
    }

    loadReviews(user_id);
});