let first = 1;
let second = 2;
let third = first + second;
console.log(third);

fetch('/api/status', { method: 'GET' })
.then(response => response.json())
.then(data => {
    console.log(data);
})
.catch(error => console.log("Not logged in"));