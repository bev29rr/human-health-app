document.getElementById("loginForm").addEventListener("submit", function(event) {
    event.preventDefault();
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    
    fetch('/api/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(
            {
                username: username,
                password: password
            }
        ),
    })
    .then(response => response.json())
    .then(data => {
        if (data.response === true) {
            alert("Logged in successfully");
        } else {
            alert("Incorrect credentials");
        }
    })
    .catch((e) => alert("Failed to login"));
});