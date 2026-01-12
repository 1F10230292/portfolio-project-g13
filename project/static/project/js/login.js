document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    const usernameInput = form.querySelector("input[name='username']");
    const passwordInput = form.querySelector("input[name='password']");

    // 1. ブラウザの入力履歴（予測候補）を無効化する設定
    if (usernameInput) {
        usernameInput.setAttribute("autocomplete", "off");
    }
    if (passwordInput) {
        // passwordマネージャーの干渉を防ぐため new-password を推奨
        passwordInput.setAttribute("autocomplete", "new-password");
    }

    // 2. フォーム送信時のバリデーション
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
            // エラーアラートを表示
            alert("ユーザー名とパスワードを入力してください。");
        }
    });

    // 3. 入力中にエラー（赤枠）を消す処理
    [usernameInput, passwordInput].forEach(input => {
        input.addEventListener("input", () => {
            input.classList.remove("error");
        });
    });
});