/**
 * Script para manejar el menú responsive del panel de administración
 * Este archivo se encarga de la interacción con el menú hamburguesa y el sidebar
 */

document.addEventListener('DOMContentLoaded', function() {
    initAdminResponsiveMenu();
});

/**
 * Inicializa el menú responsive con animaciones mejoradas para el panel de administración
 */
function initAdminResponsiveMenu() {
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const sidebar = document.getElementById('sidebar');
    const menuOverlay = document.createElement('div');
    
    // Si no existen los elementos necesarios, salir
    if (!sidebarToggle || !sidebar) return;
    
    // Crear overlay para dispositivos móviles
    menuOverlay.id = 'admin-menu-overlay';
    menuOverlay.className = 'fixed inset-0 bg-black/50 backdrop-blur-sm z-30 hidden md:hidden transition-opacity duration-300 opacity-0';
    document.body.appendChild(menuOverlay);
    
    // Función para mostrar el sidebar
    function showSidebar() {
        sidebar.classList.remove('-translate-x-full');
        sidebar.classList.add('translate-x-0');
        
        // Mostrar overlay con animación
        menuOverlay.classList.remove('hidden');
        setTimeout(() => {
            menuOverlay.classList.remove('opacity-0');
            menuOverlay.classList.add('opacity-100');
        }, 50);
        
        // Animar icono del toggle
        sidebarToggle.classList.add('rotate-90');
        
        // Bloquear scroll en dispositivos móviles
        if (window.innerWidth < 768) {
            document.body.classList.add('overflow-hidden');
        }
    }
    
    // Función para ocultar el sidebar
    function hideSidebar() {
        sidebar.classList.remove('translate-x-0');
        sidebar.classList.add('-translate-x-full');
        
        // Ocultar overlay con animación
        menuOverlay.classList.remove('opacity-100');
        menuOverlay.classList.add('opacity-0');
        setTimeout(() => {
            menuOverlay.classList.add('hidden');
        }, 300);
        
        // Restaurar icono del toggle
        sidebarToggle.classList.remove('rotate-90');
        
        // Restaurar scroll
        document.body.classList.remove('overflow-hidden');
    }
    
    // Toggle del sidebar
    sidebarToggle.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        
        if (sidebar.classList.contains('-translate-x-full')) {
            showSidebar();
        } else {
            hideSidebar();
        }
    });
    
    // Cerrar sidebar al hacer clic en el overlay
    menuOverlay.addEventListener('click', function() {
        hideSidebar();
    });
    
    // Cerrar sidebar al hacer clic en un elemento del menú en dispositivos móviles
    const menuItems = document.querySelectorAll('.menu-item');
    menuItems.forEach(item => {
        item.addEventListener('click', function() {
            if (window.innerWidth < 768) {
                hideSidebar();
            }
        });
    });
    
    // Cerrar sidebar al redimensionar la ventana a desktop
    window.addEventListener('resize', function() {
        if (window.innerWidth >= 768) {
            // En desktop, mostrar siempre el sidebar
            sidebar.classList.remove('-translate-x-full');
            sidebar.classList.add('translate-x-0');
            menuOverlay.classList.add('hidden');
            document.body.classList.remove('overflow-hidden');
        } else {
            // En móvil, ocultar el sidebar por defecto
            if (!sidebar.classList.contains('translate-x-0')) {
                sidebar.classList.add('-translate-x-full');
            }
        }
    });
    
    // Manejar navegación entre secciones
    setupSectionNavigation();
}

/**
 * Configura la navegación entre secciones del panel de administración
 */
function setupSectionNavigation() {
    const menuItems = document.querySelectorAll('.menu-item');
    const contentSections = document.querySelectorAll('.content-section');
    
    menuItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Obtener la sección a mostrar
            const targetSection = item.getAttribute('data-section');
            
            // Desactivar todos los items del menú
            menuItems.forEach(mi => {
                mi.classList.remove('active');
                const link = mi.querySelector('a');
                if (link) {
                    link.classList.remove('bg-secondary', 'text-white');
                    link.classList.add('hover:bg-white/10');
                }
            });
            
            // Activar el item seleccionado
            item.classList.add('active');
            const activeLink = item.querySelector('a');
            if (activeLink) {
                activeLink.classList.add('bg-secondary', 'text-white');
                activeLink.classList.remove('hover:bg-white/10');
            }
            
            // Ocultar todas las secciones
            contentSections.forEach(section => {
                section.classList.remove('active');
            });
            
            // Mostrar la sección seleccionada
            const sectionToShow = document.getElementById(targetSection);
            if (sectionToShow) {
                sectionToShow.classList.add('active');
            }
        });
    });
}