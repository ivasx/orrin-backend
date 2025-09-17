document.addEventListener('DOMContentLoaded', function() {
    const searchInputs = document.querySelectorAll('.search-input');

    searchInputs.forEach(input => {
        const clearBtn = input.parentElement.querySelector('.search-clear-btn');

        if (!clearBtn) return;

        // Показувати кнопку тільки коли є текст
        input.addEventListener('input', () => {
            clearBtn.style.display = input.value ? 'flex' : 'none';
        });

        // Клік по кнопці очищує поле
        clearBtn.addEventListener('click', () => {
            input.value = '';
            clearBtn.style.display = 'none';
            input.focus();
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const burger = document.querySelector('.menu-toggle'); // твій бургер
    const sidebar = document.getElementById('sidebar'); // бічне меню має id="sidebar"

    if (burger && sidebar) {
        burger.addEventListener('click', () => {
            sidebar.classList.toggle('collapsed'); // додаємо/забираємо клас collapsed
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
            const searchToggle = document.querySelector('.search-toggle');
            const mobileSearch = document.getElementById('mobileSearch');
            const searchBackBtn = document.querySelector('.search-back-btn');
            const mobileSearchInput = document.querySelector('.mobile-search .search-input');

            // Відкрити мобільний пошук
            searchToggle.addEventListener('click', function() {
                mobileSearch.classList.add('open');
                // Фокус на поле після анімації
                setTimeout(() => {
                    mobileSearchInput.focus();
                }, 100);
            });

            // Закрити мобільний пошук
            searchBackBtn.addEventListener('click', function() {
                mobileSearch.classList.remove('open');
            });

            // Закрити на ESC
            document.addEventListener('keydown', function(e) {
                if (e.key === 'Escape' && mobileSearch.classList.contains('open')) {
                    mobileSearch.classList.remove('open');
                }
            });
        });
