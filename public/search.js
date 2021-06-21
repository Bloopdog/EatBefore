function showError(message) {
    var errorMsg = `
        <div class="alert alert-danger mt-3" role="alert" id="error-div">
            <h4 class="alert-heading">${message}</h4>
            <p class="mb-0">Please try again!</p>
        </div>
    `;
    $('#main-container').append(errorMsg);
};

$(async() => {
    var urlParams = window.location.search;
    var pos = urlParams.indexOf('=') + 1;
    var length = urlParams.substr(pos).length;

    if (length != 0) {
        var place_name = decodeURI(urlParams.substr(pos));
        var serviceURL = "http://127.0.0.1:5001/review" + "/" + place_name ;

        try {
            const response = 
                await fetch(
                    serviceURL, {method: 'GET'}
                );
            const result = await response.json();
            if (response.status === 200) {
                var search_results = result.data.reviews;
                var amount = search_results.length;
                if (amount != 0) {
                    var rows = "";
                    for (const search_result of search_results) {
                        eachRow = `
                            <a href="review.html?review_id=${search_result.review_id}" class="list-group-item list-group-item-action">
                                <div class="d-flex">
                                    <div class="flex-shrink-0">
                                        <img src="${search_result.imageurl}" alt="thumbnail" style="width:100px;height: auto;">
                                    </div>
                                    <div class="flex-grow-1 ms-3">
                                        <div class="d-flex w-100 justify-content-between">
                                            <h5 class="mb-1">${search_result.review_title}</h5>
                                        </div>
                                        <p class="mb-1">Rating: ${search_result.rating}/5</p>
                                        <p class="mb-1"><i class="far fa-eye"></i> ${search_result.views} views</p>
                                        <small>${search_result.user_name} | Created on  ${search_result.created}</small>
                                    </div>
                                </div>
                            </a>
                        `;
                        rows += eachRow;
                    }
                    $('#search_heading').text(amount + " search results for " + "'" + place_name + "'");
                    $('#result_list').append(rows);
                } else {
                    var result_message = `
                    <div class="text-center mt-5">
                        <img src="images/search.png" style="width: 100px; height: 100px;">
                        <h2 class="mt-4">No results found for '${place_name}'</h2>
                    </div>
                    `;
                    $('#main-container').html(result_message);
                }
            } else if (response.status == 404) {
                var result_message = `
                    <div class="text-center">
                        <img src="images/search.png">
                        <p>No results found for '${place_name}'</p>
                    </div>
                `;
                $('#main-container').html(result_message);
                showError(result.message);
            } else {
                throw response.status;
            }
        } catch(error) {
            showError('There is a problem retrieving reviews data, please try again later.<br />' + error);
        }
    } else {
        var result_message = `
            <div class="text-center mt-5">
                <img src="images/search.png" style="width: 100px; height: 100px;">
                <h2 class="mt-4">No results found</h2>
            </div>
        `;
        $('#main-container').html(result_message);
    }
});