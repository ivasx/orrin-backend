class Menu {
    constructor(toggleSelector, sidebarSelector) {
        this.toggle = document.querySelector(toggleSelector);
        this.sidebar = document.querySelector(sidebarSelector);

        this.toggle.addEventListener('click', () => this.handleToggle());
    }

    handleToggle() {
        this.toggle.classList.toggle('active');
        this.sidebar.classList.toggle('open'); // наприклад
    }
}

// Використання
const menu = new Menu('.menu-toggle', '.sidebar');
