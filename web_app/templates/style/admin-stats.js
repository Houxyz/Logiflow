/**
 * Script para cargar estadísticas en el dashboard de administración
 * Este archivo maneja la obtención y visualización de datos estadísticos
 */

// Ejecutar cuando el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function() {
    // Cargar estadísticas si el usuario está autenticado
    checkAuthentication().then(isAuth => {
        if (isAuth) {
            loadAdminStats();
        }
    });
});

/**
 * Carga las estadísticas del panel de administración
 */
async function loadAdminStats() {
    try {
        const token = localStorage.getItem('access_token');
        if (!token) return;
        
        // Obtener estadísticas desde la API
        const response = await fetch('/api/admin/stats', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) {
            throw new Error('Error al cargar estadísticas');
        }
        
        const data = await response.json();
        
        // Actualizar la interfaz con las estadísticas
        updateStatsUI(data);
        
    } catch (error) {
        console.error('Error al cargar estadísticas:', error);
    }
}

/**
 * Actualiza la interfaz con las estadísticas obtenidas
 */
function updateStatsUI(stats) {
    // Actualizar estadísticas de usuarios con animación
    const userStatsElement = document.querySelector('.user-stats');
    if (userStatsElement) {
        userStatsElement.innerHTML = `
            <div class="stat-card animated">
                <div class="stat-icon"><i class="fas fa-users"></i></div>
                <div class="stat-info">
                    <h3 class="counter" data-target="${stats.usuarios.total}">0</h3>
                    <p>Usuarios Totales</p>
                </div>
                <div class="stat-progress">
                    <div class="progress-bar" style="width: 100%"></div>
                </div>
            </div>
            <div class="stat-card animated">
                <div class="stat-icon"><i class="fas fa-user-check"></i></div>
                <div class="stat-info">
                    <h3 class="counter" data-target="${stats.usuarios.activos}">0</h3>
                    <p>Usuarios Activos</p>
                </div>
                <div class="stat-progress">
                    <div class="progress-bar" style="width: ${stats.usuarios.activos > 0 ? (stats.usuarios.activos / stats.usuarios.total * 100) : 0}%"></div>
                </div>
            </div>
        `;
    }
    
    // Actualizar estadísticas de documentos con animación
    const docStatsElement = document.querySelector('.doc-stats');
    if (docStatsElement) {
        docStatsElement.innerHTML = `
            <div class="stat-card animated">
                <div class="stat-icon"><i class="fas fa-file-alt"></i></div>
                <div class="stat-info">
                    <h3 class="counter" data-target="${stats.documentos.total}">0</h3>
                    <p>Documentos Totales</p>
                </div>
                <div class="stat-progress">
                    <div class="progress-bar" style="width: 100%"></div>
                </div>
            </div>
        `;
        
        // Agregar estadísticas por categoría con animación
        stats.documentos.por_categoria.forEach(cat => {
            const percentage = stats.documentos.total > 0 ? (cat.count / stats.documentos.total * 100) : 0;
            docStatsElement.innerHTML += `
                <div class="stat-card animated">
                    <div class="stat-icon"><i class="fas fa-folder"></i></div>
                    <div class="stat-info">
                        <h3 class="counter" data-target="${cat.count}">0</h3>
                        <p>${cat.categoria}</p>
                    </div>
                    <div class="stat-progress">
                        <div class="progress-bar" style="width: ${percentage}%"></div>
                    </div>
                </div>
            `;
        });
    }
    
    // Iniciar animación de contadores
    animateCounters();
}

/**
 * Anima los contadores de estadísticas
 */
function animateCounters() {
    const counters = document.querySelectorAll('.counter');
    const speed = 200; // Velocidad de la animación (ms)
    
    counters.forEach(counter => {
        const target = +counter.getAttribute('data-target');
        const increment = target / speed;
        
        const updateCount = () => {
            const count = +counter.innerText;
            if (count < target) {
                counter.innerText = Math.ceil(count + increment);
                setTimeout(updateCount, 1);
            } else {
                counter.innerText = target;
            }
        };
        
        updateCount();
    });
}

/**
 * Carga la lista de usuarios registrados
 */
async function loadUsersList() {
    try {
        const token = localStorage.getItem('access_token');
        if (!token) return;
        
        // Obtener lista de usuarios desde la API
        const response = await fetch('/api/admin/usuarios', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) {
            throw new Error('Error al cargar usuarios');
        }
        
        const data = await response.json();
        
        // Actualizar la interfaz con la lista de usuarios
        updateUsersListUI(data.usuarios);
        
    } catch (error) {
        console.error('Error al cargar usuarios:', error);
    }
}

/**
 * Actualiza la interfaz con la lista de usuarios
 */
function updateUsersListUI(usuarios) {
    const usersListElement = document.querySelector('.users-list');
    if (!usersListElement) return;
    
    // Limpiar lista actual
    usersListElement.innerHTML = '';
    
    // Agregar cada usuario a la lista
    usuarios.forEach(usuario => {
        const lastLogin = usuario.ultimo_ingreso ? new Date(usuario.ultimo_ingreso).toLocaleDateString() : 'Nunca';
        
        usersListElement.innerHTML += `
            <div class="user-card ${!usuario.activo ? 'inactive' : ''}">
                <div class="user-avatar">
                    <i class="fas fa-user"></i>
                </div>
                <div class="user-info">
                    <h4>${usuario.nombre_usuario || 'Sin nombre'}</h4>
                    <p>${usuario.correo}</p>
                    <span class="user-role ${usuario.rol}">${usuario.rol}</span>
                </div>
                <div class="user-details">
                    <p><i class="fas fa-calendar"></i> Registro: ${new Date(usuario.fecha_creacion).toLocaleDateString()}</p>
                    <p><i class="fas fa-sign-in-alt"></i> Último ingreso: ${lastLogin}</p>
                </div>
                <div class="user-actions">
                    <button class="action-btn" onclick="toggleUserStatus(${usuario.id}, ${!usuario.activo})">
                        <i class="fas ${usuario.activo ? 'fa-user-slash' : 'fa-user-check'}"></i>
                    </button>
                    <button class="action-btn">
                        <i class="fas fa-edit"></i>
                    </button>
                </div>
            </div>
        `;
    });
}

/**
 * Cambia el estado de un usuario (activo/inactivo)
 */
async function toggleUserStatus(userId, newStatus) {
    try {
        const token = localStorage.getItem('access_token');
        if (!token) return;
        
        // Actualizar estado del usuario mediante la API
        const response = await fetch(`/api/admin/usuarios/${userId}/estado?activo=${newStatus}`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) {
            throw new Error('Error al actualizar estado del usuario');
        }
        
        // Recargar lista de usuarios
        loadUsersList();
        
    } catch (error) {
        console.error('Error al cambiar estado de usuario:', error);
        alert('Error al cambiar el estado del usuario. Por favor, intente nuevamente.');
    }
}