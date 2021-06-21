function showError(message) {
    var errorMsg = `
        <div class="alert alert-danger mt-3" role="alert" id="error-div">
            <h4 class="alert-heading">${message}</h4>
            <p class="mb-0">Please try again!</p>
        </div>
    `;
    $('#main-container').append(errorMsg);
}

$('#login').click(async() => {
    var email = $('#email').val();
    var password = $('#password').val();
    var serviceURL = "http://127.0.0.1:5002/user/login";

    try {
        const response = await fetch(serviceURL, {
            method: 'POST',
            headers: {"Content-Type": "application/json"},
            body : JSON.stringify({
                email: email,
                password: password
            })
        });
        const result = await response.json();
        if(response.status === 200) {
            var user = result.data;
            sessionStorage.setItem("user_id", parseInt(user.user_id));
            sessionStorage.setItem("user_name", user.user_name);
            sessionStorage.setItem("email", user.email);
            window.location.href = "index.html";
        } else if(response.status == 404 || response.status == 500) {
            showError(result.message);
        } else {
            throw response.status;
        }
    } catch(error) {
        showError('There is a problem retrieving user data, please try again.<br />' + error);
    }   
})