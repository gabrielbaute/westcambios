/**
 * Lógica de autenticación para WestCambios
 */

// Esta función se activará cuando el formulario de login haga "submit"
async function login(event) {
    // 1. Evitamos que el formulario recargue la página (comportamiento por defecto de HTML)
    event.preventDefault();
    
    // 2. Obtenemos los elementos del DOM (Bulma suele usar IDs o clases)
    const emailField = document.getElementById('email');
    const passwordField = document.getElementById('password');
    const loginButton = document.getElementById('login-button');

    // 3. Activamos el estado "loading" de Bulma en el botón para feedback visual
    loginButton.classList.add('is-loading');

    // 4. Preparamos el cuerpo de la petición (OAuth2PasswordRequestForm espera Form Data)
    const formData = new FormData();
    formData.append('username', emailField.value); // FastAPI usa 'username' por defecto en el form
    formData.append('password', passwordField.value);

    try {
        // 5. Llamada asíncrona a nuestra API
        const response = await fetch('/api/v1/auth/login', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            // 6. ¡Éxito! Guardamos el token en el almacenamiento persistente del navegador
            localStorage.setItem('access_token', data.access_token);
            
            // Redirigimos al dashboard
            window.location.href = '/admin-dashboard';
        } else {
            // 7. Error (401, 404, etc.). Mostramos el detalle al usuario.
            showNotification(data.detail || 'Error al iniciar sesión', 'is-danger');
        }
    } catch (error) {
        showNotification('Error de conexión con el servidor', 'is-danger');
    } finally {
        // Quitamos el estado de carga del botón
        loginButton.classList.remove('is-loading');
    }
}