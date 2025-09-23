/**
 * Script para manejar modales y la verificación de autenticación
 * Este archivo se encarga de la interacción con los modales y la pantalla de carga
 */

// Función para mostrar/ocultar secciones
function toggleSection(sectionId) {
    const section = document.getElementById(sectionId);
    const arrow = document.getElementById(sectionId.replace('section', 'arrow'));
    
    if (section && arrow) {
        if (section.style.display === 'none' || !section.style.display) {
            section.style.display = 'block';
            arrow.style.transform = 'rotate(180deg)';
        } else {
            section.style.display = 'none';
            arrow.style.transform = 'rotate(0)';
        }
    }
}

// Función para inicializar la verificación de autenticación
async function initAuthCheck() {
    const authCheck = document.getElementById('auth-check');
    const mainContent = document.getElementById('main-content');
    
    if (!authCheck || !mainContent) {
        console.error('Elementos de autenticación no encontrados');
        return;
    }
    
    try {
        // Verificar si el usuario está autenticado
        const isLoggedIn = await isAuthenticated();
        
        if (isLoggedIn) {
            // Si está autenticado, mostrar el contenido principal
            authCheck.style.display = 'none';
            mainContent.classList.remove('hidden');
            
            // Obtener información del usuario y actualizar elementos en la página
            const user = await getCurrentUser();
            if (user) {
                // Actualizar elementos con información del usuario
                const userNameElements = document.querySelectorAll('#user-name, #welcome-username');
                userNameElements.forEach(element => {
                    if (element) element.textContent = user.nombre_usuario || 'Usuario';
                });
                
                const userEmailElement = document.getElementById('welcome-email');
                if (userEmailElement && user.correo) {
                    userEmailElement.textContent = user.correo;
                }
            }
        } else {
            // Si no está autenticado, redirigir a la página de login
            window.location.href = '/login';
        }
    } catch (error) {
        console.error('Error al verificar autenticación:', error);
        // En caso de error, redirigir a la página de login
        window.location.href = '/login';
    }
}

// Ejecutar la verificación de autenticación cuando se carga la página
document.addEventListener('DOMContentLoaded', function() {
    // Iniciar verificación de autenticación
    initAuthCheck();
    
    // Inicializar secciones expandibles
    const sections = ['info-section', 'normativas-section'];
    sections.forEach(section => {
        const sectionElement = document.getElementById(section);
        if (sectionElement) {
            sectionElement.style.display = 'block';
        }
    });
});