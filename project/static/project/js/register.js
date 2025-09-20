document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    const inputs = form.querySelectorAll("input");

    form.addEventListener("submit", (e) => {
        let valid = true;

        inputs.forEach(input => {
            if (input.value.trim() === "") {
                valid = false;
                input.classList.add("error");
            } else {
                input.classList.remove("error");
            }
        });

        if (!valid) {
            e.preventDefault();
            alert("すべての項目を入力してください。");
        }
    });

    // 入力中に赤枠が消える
    inputs.forEach(input => {
        input.addEventListener("input", () => {
            input.classList.remove("error");
        });
    });
});
