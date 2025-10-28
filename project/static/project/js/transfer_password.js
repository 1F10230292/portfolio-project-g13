document.addEventListener('DOMContentLoaded', () => {
    const copyBtn = document.getElementById('copyBtn');
    const transferPassword = document.getElementById('transferPassword');

    copyBtn.addEventListener('click', () => {
        if (transferPassword) {
            // パスワードをコピー
            navigator.clipboard.writeText(transferPassword.textContent)
                .then(() => {
                    alert('パスワードをコピーしました');
                })
                .catch(err => {
                    alert('コピーに失敗しました: ' + err);
                });
        }
    });
});
