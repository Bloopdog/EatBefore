var user_id = sessionStorage.getItem("user_id");
var email = sessionStorage.getItem("email");

function showError(message) {
    $('#message').html("<p>" + message + "</p>");
};

$('#formSubmit').click(async() => {
    var loading = `
        <div class="text-center">
            <image src="images/loading.gif" style="width: 100px; height: 100px;">
            <p>Cashing out in progress...</p>
        </div>
    `;
    $('#message').html(loading);

    var amount = parseFloat($('#amount').val());
    var serviceURL = "http://127.0.0.1:5202/redemption";

    try {
        const response = await fetch(serviceURL, {
            method: 'POST',
            headers: {"Content-Type": "application/json"},
            body : JSON.stringify({
                user_id: user_id,
                amount: amount,
                email: email
            })
        });
        const result = await response.json();

        if(response.status === 200) {
            $('#message').html("<p>You have successfully cashed out $" + amount + "!</p>");
            $('#modal').append(`
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <a class="btn btn-primary" href="user.html" role="button">Done</a>
                </div>
            `);
        } else if(response.status == 400 || response.status == 500) {
            showError(result.message);
            $('#modal').append(`
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                </div>
            `);
        } else {
            throw response.status;
        }
    } catch(error) {
        showError('There is a problem retrieving review data, please try again.<br />' + error);
    }   
})