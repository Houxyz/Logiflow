/**
 * Script para manejar el menú móvil y los submenús en el dashboard de usuario
 * Versión mejorada que soluciona problemas de espacio y navegación
 */

document.addEventListener('DOMContentLoaded', function() {
    initMobileMenu();
});

/**
 * Inicializa las funcionalidades del menú móvil con mejor organización
 */
function initMobileMenu() {
    // Referencias principales
    const mobileMenu = document.getElementById('mobile-menu');
    const logoutContainer = mobileMenu ? mobileMenu.querySelector('.absolute.bottom-0') : null;
    const menuContent = mobileMenu ? mobileMenu.querySelector('.p-4.space-y-3') : null;
    
    if (!mobileMenu || !menuContent) return;
    
    // Configurar el contenedor del menú para mejor scroll
    mobileMenu.classList.add('flex', 'flex-col');
    menuContent.classList.add('flex-grow', 'overflow-y-auto', 'custom-scrollbar');
    
    // Añadir estilos para la barra de desplazamiento personalizada
    addCustomScrollbarStyles();
    
    // Función mejorada para manejar los submenús en la versión móvil
    window.toggleMobileSubmenu = function(submenuId) {
        const submenu = document.getElementById(submenuId);
        const iconId = submenuId.split('-')[0] + '-icon';
        const icon = document.getElementById(iconId);
        const parentButton = submenu ? submenu.previousElementSibling : null;
        
        if (submenu) {
            if (submenu.classList.contains('hidden')) {
                // Cerrar todos los submenús primero
                document.querySelectorAll('[id$="-submenu"]').forEach(menu => {
                    if (menu.id !== submenuId && !menu.classList.contains('hidden')) {
                        menu.classList.add('hidden');
                        const otherIconId = menu.id.split('-')[0] + '-icon';
                        const otherIcon = document.getElementById(otherIconId);
                        const otherParent = menu.previousElementSibling;
                        
                        if (otherIcon) otherIcon.classList.remove('rotate-180');
                        if (otherParent) otherParent.classList.remove('bg-blue-50', 'text-primary');
                    }
                });
                
                // Abrir el submenú seleccionado con animación
                submenu.classList.remove('hidden');
                submenu.classList.add('animate-fade-in-up');
                
                // Destacar el botón padre activo
                if (parentButton) {
                    parentButton.classList.add('bg-blue-50', 'text-primary');
                }
                
                if (icon) icon.classList.add('rotate-180');
                
                // Hacer scroll suave al submenú
                setTimeout(() => {
                    if (parentButton) {
                        parentButton.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    }
                }, 100);
            } else {
                // Cerrar el submenú
                submenu.classList.add('hidden');
                submenu.classList.remove('animate-fade-in-up');
                
                // Restaurar el botón padre
                if (parentButton) {
                    parentButton.classList.remove('bg-blue-50', 'text-primary');
                }
                
                if (icon) icon.classList.remove('rotate-180');
            }
            
            // Reorganizar el espacio del menú
            optimizeMenuLayout();
        }
    };
    
    /**
     * Optimiza la distribución del menú móvil para aprovechar el espacio
     */
    function optimizeMenuLayout() {
        if (!mobileMenu || !menuContent) return;
        
        // Asegurar que el contenedor de menú tenga altura adecuada
        menuContent.style.maxHeight = 'calc(100vh - 180px)';
        
        // Ajustar el botón de cerrar sesión
        if (logoutContainer) {
            logoutContainer.classList.remove('absolute');
            logoutContainer.classList.add('relative', 'mt-4', 'mb-2');
        }
        
        // Añadir espacio después del último elemento para mejor scroll
        const lastSubmenu = Array.from(document.querySelectorAll('[id$="-submenu"]:not(.hidden)')).pop();
        if (lastSubmenu) {
            lastSubmenu.classList.add('pb-4');
        }
    }
    
    /**
     * Añade estilos para una barra de desplazamiento personalizada
     */
    function addCustomScrollbarStyles() {
        // Crear elemento de estilo si no existe
        if (!document.getElementById('custom-scrollbar-styles')) {
            const styleEl = document.createElement('style');
            styleEl.id = 'custom-scrollbar-styles';
            styleEl.textContent = `
                .custom-scrollbar::-webkit-scrollbar {
                    width: 4px;
                }
                .custom-scrollbar::-webkit-scrollbar-track {
                    background: #f1f1f1;
                    border-radius: 10px;
                }
                .custom-scrollbar::-webkit-scrollbar-thumb {
                    background: #3498db;
                    border-radius: 10px;
                }
                .custom-scrollbar::-webkit-scrollbar-thumb:hover {
                    background: #2c3e50;
                }
                .custom-scrollbar {
                    scrollbar-width: thin;
                    scrollbar-color: #3498db #f1f1f1;
                }
            `;
            document.head.appendChild(styleEl);
        }
    }
    
    // Inicializar la distribución del menú
    optimizeMenuLayout();
    
    // Observar cambios en el tamaño de la ventana
    window.addEventListener('resize', optimizeMenuLayout);
}