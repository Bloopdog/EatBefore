function showError(message) {
    $('#main-container').append('<label>' + message + '</label>');
};

$('#signUpForm').submit(async(event) => {
    event.preventDefault();
    var username = $('#username').val();
    var email = $('#email').val();
    var password = $('#password').val();
    var serviceURL = "http://127.0.0.1:5002/user/create";

    try {
        const response = await fetch(serviceURL, {
            method: 'POST',
            headers: {"Content-Type": "application/json"},
            body : JSON.stringify({
                user_name: username,
                password: password,
                email: email,
                wallet_balance: 0,
                total_views: 0,
            })
        });
        const result = await response.json();
        if(response.status === 201) {
            var user = result.data;
            sessionStorage.setItem("user_id", parseInt(user.user_id));
            sessionStorage.setItem("user_name", user.user_name);
            sessionStorage.setItem("email", user.email);
            window.location.href = "index.html";
        }
        else if(response.status == 400 || response.status == 500) {
            showError(result.message);
        } else {
            throw response.status;
        }
    } catch(error) {
        showError('There is a problem retrieving review data, please try again.<br />' + error);
    }   
})