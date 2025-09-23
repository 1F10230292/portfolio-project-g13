document.addEventListener('DOMContentLoaded', () => {
    const heroSection = document.querySelector('.hero-section');
    if (heroSection) {
        heroSection.style.opacity = '0'; 
        heroSection.style.transform = 'translateY(20px)'; 
        heroSection.style.transition = 'opacity 1s ease-out, transform 1s ease-out'; // アニメーション設定

        setTimeout(() => {
            heroSection.style.opacity = '1';
            heroSection.style.transform = 'translateY(0)';
        }, 100); 
    }

    // 各要素を個別にフェードインさせたい場合（今回はheroSection全体に適用）
    // const heroTitle = document.querySelector('.hero-title');
    // const heroSubtitle = document.querySelector('.hero-subtitle');
    // const heroActions = document.querySelector('.hero-actions');

    // const elementsToAnimate = [heroTitle, heroSubtitle, heroActions];
    // elementsToAnimate.forEach((el, index) => {
    //     if (el) {
    //         el.style.opacity = '0';
    //         el.style.transform = 'translateY(20px)';
    //         el.style.transition = `opacity 0.8s ease-out ${index * 0.2}s, transform 0.8s ease-out ${index * 0.2}s`;
    //         setTimeout(() => {
    //             el.style.opacity = '1';
    //             el.style.transform = 'translateY(0)';
    //         }, 100);
    //     }
    // });


    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', (e) => {
            // スプラッシュエフェクトを追加
            const rect = button.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const splash = document.createElement('span');
            splash.classList.add('btn-splash');
            splash.style.left = `${x}px`;
            splash.style.top = `${y}px`;
            button.appendChild(splash);

            // アニメーション終了後に要素を削除
            splash.addEventListener('animationend', () => {
                splash.remove();
            });
        });
    });
});