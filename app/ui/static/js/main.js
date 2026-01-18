// static/js/main.js
function logout() {
    localStorage.removeItem('access_token');
    window.location.href = '/';
}

/**
 * Función auxiliar para mostrar mensajes tipo "Flash" con Bulma
 */
function showNotification(message, colorClass) {
    const container = document.getElementById('notification-area');
    container.innerHTML = `
        <div class="notification ${colorClass}">
            <button class="delete" onclick="this.parentElement.remove()"></button>
            ${message}
        </div>
    `;
}

/**
 * Función auxiliar para manejar el menú de hamburguesa de Bulma
 */
document.addEventListener('DOMContentLoaded', () => {
  const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);
  if ($navbarBurgers.length > 0) {
    $navbarBurgers.forEach( el => {
      el.addEventListener('click', () => {
        const target = el.dataset.target;
        const $target = document.getElementById(target);
        el.classList.toggle('is-active');
        $target.classList.toggle('is-active');
      });
    });
  }
});
