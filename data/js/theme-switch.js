document.addEventListener('DOMContentLoaded', () => {
    const body = document.body;
    const wrapper = document.getElementById('wrapper');
    const themeToggle = document.getElementById('theme-toggle');

    if (!wrapper || !themeToggle) {
        return;
    }

    // Carregar o tema salvo no localStorage
    const darkMode = sessionStorage.getItem('dark-mode') === 'enabled';

    // Aplica a classe 'dark-mode' com base na preferência armazenada
    if (darkMode) {
        wrapper.classList.add('dark-mode');
    } else {
        wrapper.classList.remove('dark-mode');
    }

    // Alterna o tema e salva a preferência
    themeToggle.addEventListener('click', () => {
        wrapper.classList.toggle('dark-mode');
        sessionStorage.setItem('dark-mode', wrapper.classList.contains('dark-mode') ? 'enabled' : 'disabled');
    });
});
