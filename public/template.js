var user_id = sessionStorage.getItem("user_id");

// this function calls all the individual component display functions
function display_all() {
    if (user_id) {
        display_user_navbar();
    } else {
        display_navbar();
    }
};

function display_navbar() {
    // Navbar for all pages
    let id = 'navbar';

    document.getElementById(id).innerHTML = `
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container-fluid">
            <a class="navbar-brand" href="index.html"><img style="max-height: 100%; height: 100%; width: auto; margin: 0 auto; -o-object-fit: contain; object-fit: contain;" src="images/medium_logo.png" alt="logo"></a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                        <a class="nav-link" href="login.html">Login</a>
                    </li>
                </ul>
                <form class="d-flex">
                <input class="form-control me-2" id="search" type="search" placeholder="Search" aria-label="Search">
                <a class="btn btn-outline-success" href="" onclick="this.href='search.html?place='+document.getElementById('search').value" role="button">Search</a>
                </form>
            </div>
        </div>
    </nav>
    `;
};

function display_user_navbar() {
    // Navbar for all pages
    let id = 'navbar';

    document.getElementById(id).innerHTML = `
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container-fluid">
        <a class="navbar-brand" href="index.html"><img style="max-height: 100%; height: 100%; width: auto; margin: 0 auto; -o-object-fit: contain; object-fit: contain;" src="images/medium_logo.png" alt="logo"></a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                        <a class="nav-link" href="makereview.html">Make A Review</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="user.html">Profile</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="index.html" onclick="clearSession()">Log Out</a>
                    </li>
                </ul>
                <form class="d-flex">
                <input class="form-control me-2" id="search" type="search" placeholder="Search" aria-label="Search">
                <a class="btn btn-outline-success" href="" onclick="this.href='search.html?place='+document.getElementById('search').value" role="button">Search</a>
                </form>
            </div>
        </div>
    </nav>
    `;
};

function clearSession() {
    sessionStorage.clear();
}