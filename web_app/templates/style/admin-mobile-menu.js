/**
 * Script para manejar los submenús móviles en el panel de administración
 * Este archivo implementa la función toggleMobileSubmenu para el dashboard de administración
 */

document.addEventListener('DOMContentLoaded', function() {
    initAdminMobileMenu();
});

/**
 * Inicializa las funcionalidades de menú móvil para el panel de administración
 */
function initAdminMobileMenu() {
    // Asegurarse de que la función toggleMobileSubmenu esté disponible globalmente
    if (typeof window.toggleMobileSubmenu !== 'function') {
        /**
         * Función para manejar los submenús en la versión móvil del panel de administración
         * @param {string} submenuId - El ID del submenú a mostrar/ocultar
         */
        window.toggleMobileSubmenu = function(submenuId) {
            const submenu = document.getElementById(submenuId);
            const iconId = submenuId.split('-')[0] + '-icon';
            const icon = document.getElementById(iconId);
            
            if (submenu) {
                if (submenu.classList.contains('hidden')) {
                    // Cerrar todos los submenús primero
                    document.querySelectorAll('[id$="-submenu"]').forEach(menu => {
                        if (menu.id !== submenuId && !menu.classList.contains('hidden')) {
                            menu.classList.add('hidden');
                            const otherIconId = menu.id.split('-')[0] + '-icon';
                            const otherIcon = document.getElementById(otherIconId);
                            if (otherIcon) otherIcon.classList.remove('rotate-180');
                        }
                    });
                    
                    // Abrir el submenú seleccionado
                    submenu.classList.remove('hidden');
                    if (icon) icon.classList.add('rotate-180');
                } else {
                    // Cerrar el submenú
                    submenu.classList.add('hidden');
                    if (icon) icon.classList.remove('rotate-180');
                }
            }
        };
    }
    
    // Inicializar los eventos para los botones de submenú si existen
    const submenuButtons = document.querySelectorAll('[id$="-submenu-btn"]');
    submenuButtons.forEach(button => {
        const submenuId = button.getAttribute('data-target');
        if (submenuId) {
            button.addEventListener('click', function() {
                toggleMobileSubmenu(submenuId);
            });
        }
    });
}