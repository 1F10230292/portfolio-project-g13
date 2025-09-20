// login.js - UX改良版
document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    const usernameInput = form.querySelector("input[name='username']");
    const passwordInput = form.querySelector("input[name='password']");

    form.addEventListener("submit", (e) => {
        let valid = true;

        // 空欄チェック
        [usernameInput, passwordInput].forEach(input => {
            if (input.value.trim() === "") {
                valid = false;
                input.classList.add("error");
            } else {
                input.classList.remove("error");
            }
        });

        if (!valid) {
            e.preventDefault();
            // エラーアラートをスムーズに表示
            alert("ユーザー名とパスワードを入力してください。");
        }
    });

    // Enter押下でも赤枠が消えるように
    [usernameInput, passwordInput].forEach(input => {
        input.addEventListener("input", () => {
            input.classList.remove("error");
        });
    });
});
