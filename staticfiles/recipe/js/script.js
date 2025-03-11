"use-strict";

// elements
const btnContainer = document.querySelector(".btn-container");
const btnToken = document.querySelector(".btn-success");

// timeout function for setting time to fetch token
const timeout = function (s) {
  return new Promise(function (_, reject) {
    setTimeout(function () {
      reject(new Error(`Request took too long! Timeout after ${s} second`));
    }, s * 1000);
  });
};

// function to fetch csrf token from cookie data
const getCSRFToken = function () {
  const cookies = document.cookie.split(";");
  // looping over cookie data to find CSRF
  for (let i = 0; i < cookies.length; i++) {
    let cookie = cookies[i].trim();
    if (cookie.startsWith("csrftoken=")) {
      return cookie.split("=")[1];
    }
  }
  return "";
};

// function to display generated token
const displayToken = function (token) {
  const markup = `
  <div class="alert alert-success">
    ${token}
  </div>
  `;
  btnContainer.innerHTML = markup;
};

// handling the token generation button click event
btnToken.addEventListener("click", async function (e) {
  e.preventDefault();
  const response = await Promise.race([
    fetch("http://127.0.0.1:8000/forkify-user/generate-token/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCSRFToken(), // Include CSRF token
      },
    }),
    timeout(5),
  ]);

  const data = await response.json();
  displayToken(
    data.access_key ? data.access_key : "Too many request have been sent!"
  );
});
