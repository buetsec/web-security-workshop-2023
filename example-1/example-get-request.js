const fetch = require("node-fetch");
const url = 'https://example.com';

fetch(url)
.then((res) => {
    return res.text();
})
.then((data) => {
    console.log(data);
})
.finally(() => {
    console.log("fetch completed");
})
