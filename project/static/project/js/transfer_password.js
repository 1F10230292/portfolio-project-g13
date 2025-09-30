document.addEventListener("DOMContentLoaded", () => {
  const copyBtn = document.getElementById("copyBtn");
  const printBtn = document.getElementById("printBtn");
  const passwordElem = document.getElementById("transferPassword");

  if (copyBtn && passwordElem) {
    copyBtn.addEventListener("click", () => {
      navigator.clipboard.writeText(passwordElem.textContent)
        .then(() => alert("パスワードをコピーしました"))
        .catch(() => alert("コピーに失敗しました"));
    });
  }

  if (printBtn) {
    printBtn.addEventListener("click", () => {
      window.print();
    });
  }
});
