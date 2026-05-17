// Django Rest Framework用処理
// 検証用
console.log("signup.js loaded");

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

document.addEventListener("DOMContentLoaded", function () {
  const signupForm = document.getElementById("signup-form");
  const messageArea = document.getElementById("signup-message");

  console.log("signupForm:", signupForm);
  console.log("messageArea:", messageArea);

  if (!signupForm) {
    console.error("signup-form が見つかりません。");
    return;
  }

  signupForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    console.log("signup form submitted by fetch");

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const csrfToken = getCookie("csrftoken");

    console.log("送信 username:", username);
    console.log("csrfToken:", csrfToken);

    try {
      const response = await fetch("/api/users/signup/", {
        method: "POST",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({
          username: username,
          password: password,
        }),
      });

      const data = await response.json();

      console.log("response status:", response.status);
      console.log("response data:", data);

      if (response.ok) {
        if (messageArea) {
          messageArea.textContent = "新規登録が完了しました。";
        }

        window.location.href = "/login/";
      } else {
        const errorMessage =
          data.error ||
          data.username ||
          data.password ||
          data.non_field_errors ||
          "新規登録に失敗しました。";

        if (messageArea) {
          messageArea.textContent = errorMessage;
        }

        console.error("signup error:", data);
      }
    } catch (error) {
      console.error(error);

      if (messageArea) {
        messageArea.textContent = "通信エラーが発生しました。";
      }
    }
  });
});