function showError(message) {
    $('#body-content').append('<label>' + message + '</label>');
};

async function printList(serviceURL) {
    try {
        const response = 
            await fetch(
                serviceURL, {method: 'GET'}
            );
        const result = await response.json();
        if (response.status === 200) {
            var reviews = result.data.reviews;
            var rows = "";
            for (const review of reviews) {
                console.log(review.imageurl);
                eachRow = `
                    <a href="review.html?review_id=${review.review_id}" class="list-group-item text-decoration-none text-reset">
                        <div class="d-flex">
                            <div class="flex-shrink-0">
                                <img src="${review.imageurl}" alt="thumbnail" style="width:100px;height: auto;">
                            </div>
                            <div class="flex-grow-1 ms-3">
                                <div class="d-flex w-100 justify-content-between">
                                    <h5 class="mb-1">${review.place_name}</h5>
                                    <small id="date">${review.created}</small>
                                </div>
                                <p class="mb-1 fw-bold">${review.review_title}</p>
                                <p class="mb-1">Rating: ${review.rating}/5</p>
                                <p class="mb-1"><i class="far fa-eye"></i> ${review.views} views</p>
                                <small>By ${review.user_name}</small>
                            </div>
                        </div>
                    </a>
                `
                rows += eachRow;
            }

            for (var i = 0; i < 2; i++) {
                console.log(reviews[i].review_id);
                var name = '#img' + reviews[i].review_id;
                $(name).attr('src', reviews[i].imageurl);
            }
            $('#review_list').html(rows);
        } else if (response.status == 404) {
            showError(result.message);
        } else {
            throw response.status;
        }
    } catch(error) {
        showError('There is a problem retrieving reviews data, please try again later.<br />' + error);
    }
}

$(async() => {
    var serviceURL = "http://127.0.0.1:5001/review";
    printList(serviceURL);

    $('#all').click(async() => {
        $('#topViews').removeClass("active");
        $('#topRated').removeClass("active");
        $('#all').addClass("active");
        var serviceURL = "http://127.0.0.1:5001/review";
        printList(serviceURL);
    });

    $('#topRated').click(async() => {
        $('#all').removeClass("active");
        $('#topRated').addClass("active");
        var serviceURL = "http://127.0.0.1:5001/review/sorted/rating";
        printList(serviceURL);
    });

    $('#topViews').click(async() => {
        $('#topRated').removeClass("active");
        $('#topViews').addClass("active");
        var serviceURL = "http://127.0.0.1:5001/review/sorted/views";
        printList(serviceURL);
    });
});


