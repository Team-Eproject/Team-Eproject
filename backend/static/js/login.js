// Django Rest Framework用処理

// CookieからCSRFトークンを取得する関数
function getCookie(name) {
  const cookies = document.cookie.split(";");

  for (let cookie of cookies) {
    cookie = cookie.trim();

    if (cookie.startsWith(name + "=")) {
      return decodeURIComponent(cookie.substring(name.length + 1));
    }
  }

  return null;
}

const loginForm = document.getElementById("login-form");
const messageArea = document.getElementById("login-message");

// API経由で送信するため、通常のHTMLのform送信を止める処理
loginForm.addEventListener("submit", async function (event) {
  event.preventDefault();

  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;
  const csrfToken = getCookie("csrftoken");

  try {
    const response = await fetch("/api/users/login/", {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
      // HTMLで入力された値をJSONに変換し返す
      body: JSON.stringify({
        username: username,
        password: password,
      }),
    });

    const data = await response.json();

    if (response.ok) {
      messageArea.textContent = "ログインしました。";

      // main.htmlのURLに合わせて変更
      window.location.href = "/main/";
    } else {
      messageArea.textContent = data.error || "ログインに失敗しました。";
    }
  } catch (error) {
    console.error(error);
    messageArea.textContent = "通信エラーが発生しました。";
  }
});