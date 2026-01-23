/**
 * static/js/dashboard.js
 */

document.addEventListener('DOMContentLoaded', async () => {
    // Manejo de tabs
    const tabs = document.querySelectorAll('.tabs li');
    const tabContents = document.querySelectorAll('.tab-pane');

    tabs.forEach(tab => {
        tab.addEventListener('click', async () => {
            tabs.forEach(item => item.classList.remove('is-active'));
            tab.classList.add('is-active');

            const target = tab.dataset.tab;
            tabContents.forEach(content => {
                content.id === target 
                    ? content.classList.remove('is-hidden') 
                    : content.classList.add('is-hidden');
            });

            // Cargamos datos según el tab seleccionado
            if (target === 'users-tab') await loadUsers();
            if (target === 'rates-tab') await loadRates();
        });
    });

    // Carga inicial
    await loadUsers();
});

// Carga de usuarios
async function loadUsers() {
    const token = localStorage.getItem('access_token');
    if (!token) {
        window.location.href = '/';
        return;
    }

    try {
        const response = await fetch('/api/v1/admin/all_users', {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (response.status === 401 || response.status === 403) {
            logout();
            return;
        }

        const data = await response.json(); // 'data' es el diccionario {count: 3, users: [...]}
        const tableBody = document.getElementById('users-table-body');
        
        // Accedemos a la lista dentro del diccionario
        const usersList = data.users; 

        if (usersList && usersList.length > 0) {
            // Dentro de loadUsers, al mapear los usuarios:
            tableBody.innerHTML = usersList.map(user => {
                // Escapamos el objeto para que sea seguro pasarlo como argumento
                const userJson = JSON.stringify(user).replace(/"/g, '&quot;');
                
                return `
                <tr>
                    <td>${user.id}</td>
                    <td>${user.email}</td>
                    <td>${user.username}</td>
                    <td><span class="tag ${user.role === 'ADMIN' ? 'is-warning' : 'is-info'}">${user.role}</span></td>
                    <td>${user.is_active ? '<span class="tag is-success">Activo</span>' : '<span class="tag is-danger">Inactivo</span>'}</td>
                    <td>
                        <div class="buttons are-small">
                            <button class="button is-warning is-light" title="Editar" onclick="openEditModal(${userJson})">
                                <span class="icon is-small">
                                    <i class="fas fa-edit"></i>
                                </span>
                            </button>
                            <button class="button is-danger is-light" title="Eliminar" onclick="deleteUser(${user.id})">
                                <span class="icon is-small">
                                    <i class="fas fa-trash"></i>
                                </span>
                            </button>
                        </div>
                    </td>
                </tr>
            `;}).join('');
        } else {
            tableBody.innerHTML = '<tr><td colspan="5" class="has-text-centered">No hay usuarios registrados</td></tr>';
        }

    } catch (error) {
        console.error('Error cargando usuarios:', error);
    }
}

// Carga de tasas
async function loadRates() {
    const token = localStorage.getItem('access_token');
    try {
        const response = await fetch('/api/v1/rates/all', {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (response.status === 401 || response.status === 403) {
            logout();
            return;
        }

        const data = await response.json(); // { count: 4, rates: [...] }
        const tableBody = document.getElementById('rates-table-body');
        
        // Accedemos a la lista 'rates'
        const ratesList = data.rates.sort((a, b) => b.id - a.id);

        if (ratesList && ratesList.length > 0) {
            tableBody.innerHTML = ratesList.map(rate => {
                // Formateamos la fecha para que sea legible (formalismo matemático/técnico)
                const rateJson = JSON.stringify(rate).replace(/"/g, '&quot;');
                const date = new Date(rate.timestamp).toLocaleString();

                return `
                    <tr>
                        <td>${rate.id}</td>
                        <td><span class="tag is-light">${rate.from_currency}</span></td>
                        <td><span class="tag is-light">${rate.to_currency}</span></td>
                        <td class="has-text-weight-bold">${rate.rate.toFixed(2)}</td>
                        <td><small>${date}</small></td>
                        <td>
                            <div class="buttons are-small">
                                <button class="button is-warning is-light" onclick="openEditRateModal(${rateJson})">
                                    <span class="icon is-small"><i class="fas fa-edit"></i></span>
                                </button>
                            </div>
                        </td>
                    </tr>
                `;
            }).join('');
        } else {
            tableBody.innerHTML = '<tr><td colspan="5" class="has-text-centered">No hay tasas registradas</td></tr>';
        }
    } catch (error) {
        console.error('Error cargando tasas:', error);
    }
}

/**
 * Funciones para el manejo del Modal de Tasas
 */

function showRateModal() {
    document.getElementById('rate-modal').classList.add('is-active');
}

function closeRateModal() {
    document.getElementById('rate-modal').classList.remove('is-active');
    document.getElementById('rate-form').reset();
}

async function saveRate(event) {
    event.preventDefault();
    const btn = document.getElementById('save-rate-btn');
    const form = event.target;
    const token = localStorage.getItem('access_token');

    // Extraemos datos y convertimos 'rate' a float (importante para Pydantic)
    const formData = new FormData(form);
    const payload = Object.fromEntries(formData.entries());
    payload.rate = parseFloat(payload.rate);

    btn.classList.add('is-loading');

    try {
        const response = await fetch('/api/v1/admin/register_rate', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            closeRateModal();
            await loadRates(); // Recargamos la tabla automáticamente
            // Opcional: mostrar notificación de éxito
        } else {
            const error = await response.json();
            alert('Error al guardar: ' + JSON.stringify(error.detail));
        }
    } catch (err) {
        console.error('Error post rate:', err);
    } finally {
        btn.classList.remove('is-loading');
    }
}

/**
 * Funciones para el manejo de operaciones CRUD en las tablas
 */

// 1. Registro Manual
async function registerUser(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const payload = Object.fromEntries(formData.entries());
    
    const response = await fetch('/api/v1/admin/register_user', {
        method: 'POST',
        headers: { 
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            'Content-Type': 'application/json' 
        },
        body: JSON.stringify(payload)
    });

    if (response.ok) {
        alert("Usuario creado con éxito");
        event.target.reset();
        // Opcional: saltar al tab de usuarios para ver el resultado
    }
}

// 2. Edición
function openEditModal(user) {
    document.getElementById('edit-user-id').value = user.id;
    document.getElementById('edit-username').value = user.username;
    document.getElementById('edit-is-active').checked = user.is_active;
    document.getElementById('edit-user-modal').classList.add('is-active');
}

async function updateUser(event) {
    event.preventDefault();
    const userId = document.getElementById('edit-user-id').value;
    const payload = {
        username: document.getElementById('edit-username').value,
        is_active: document.getElementById('edit-is-active').checked
    };

    const response = await fetch(`/api/v1/admin/update_user/${userId}`, {
        method: 'PATCH',
        headers: { 
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            'Content-Type': 'application/json' 
        },
        body: JSON.stringify(payload)
    });

    if (response.ok) {
        closeEditModal();
        loadUsers();
    }
}

// 3. Eliminación (Llamaría a un endpoint DELETE que deberíamos tener)
async function deleteUser(userId) {
    if (!confirm(`¿Estás seguro de eliminar al usuario con ID: ${userId}? Esta acción es irreversible.`)) return;

    try {
        const response = await fetch(`/api/v1/admin/delete_user/${userId}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
        });

        if (response.ok) {
            await loadUsers(); // Refrescamos la lista
        } else {
            alert("No se pudo eliminar el usuario.");
        }
    } catch (err) {
        console.error("Error deleting user:", err);
    }
}

function closeEditModal() {
    document.getElementById('edit-user-modal').classList.remove('is-active');
}

/** * Gestión de Edición de Tasas 
 */
function openEditRateModal(rate) {
    document.getElementById('edit-rate-id').value = rate.id;
    document.getElementById('edit-rate-value').value = rate.rate;
    document.getElementById('edit-rate-modal').classList.add('is-active');
}

function closeEditRateModal() {
    document.getElementById('edit-rate-modal').classList.remove('is-active');
}

async function updateRate(event) {
    event.preventDefault();
    const rateId = document.getElementById('edit-rate-id').value;
    const newValue = parseFloat(document.getElementById('edit-rate-value').value);
    const token = localStorage.getItem('access_token');

    try {
        const response = await fetch(`/api/v1/admin/update_rate/${rateId}`, {
            method: 'PATCH',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ rate: newValue })
        });

        if (response.ok) {
            closeEditRateModal();
            await loadRates(); // Recarga la tabla
        } else {
            alert("Error al actualizar la tasa.");
        }
    } catch (err) {
        console.error("Error patching rate:", err);
    }
}