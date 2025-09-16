document.addEventListener('DOMContentLoaded', function () {
    const toggleBtn = document.querySelector('.search-toggle'); // іконка в хедері (праворуч)
    const mobileSearch = document.querySelector('.mobile-search');
    if (!toggleBtn || !mobileSearch) return;

    const backBtn = mobileSearch.querySelector('.search-back-btn'); // кнопка назад
    const searchInput = mobileSearch.querySelector('.search-input');

    function openMobileSearch() {
        mobileSearch.style.display = 'block';
        setTimeout(() => mobileSearch.classList.add('open'), 10);
        toggleBtn.classList.add('active'); // змінюємо іконку на стрілку
        if (searchInput) searchInput.focus();
    }

    function closeMobileSearch() {
        mobileSearch.classList.remove('open');
        toggleBtn.classList.remove('active');
        setTimeout(() => {
            if (!mobileSearch.classList.contains('open')) {
                mobileSearch.style.display = 'none';
            }
        }, 150);
    }

    toggleBtn.addEventListener('click', function (e) {
        e.preventDefault();
        const isVisible = getComputedStyle(mobileSearch).display !== 'none' && mobileSearch.classList.contains('open');
        if (isVisible) closeMobileSearch(); else openMobileSearch();
    });

    if (backBtn) {
        backBtn.addEventListener('click', function (e) {
            e.preventDefault();
            closeMobileSearch();
        });
    }

    document.addEventListener('click', function (e) {
        if (getComputedStyle(mobileSearch).display !== 'none' &&
            !mobileSearch.contains(e.target) &&
            !toggleBtn.contains(e.target)) {
            closeMobileSearch();
        }
    });

    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') closeMobileSearch();
    });

    window.addEventListener('resize', function () {
        if (window.innerWidth >= 768) closeMobileSearch();
    });
});

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
