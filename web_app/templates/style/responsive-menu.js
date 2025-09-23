/**
 * Script para manejar el menú responsive
 * Este archivo se encarga de la interacción con el menú hamburguesa y la navegación responsive
 */

document.addEventListener('DOMContentLoaded', function() {
    initResponsiveMenu();
});

/**
 * Inicializa el menú responsive con animaciones mejoradas
 */
function initResponsiveMenu() {
    const hamburger = document.getElementById('hamburger-menu');
    const navLinks = document.getElementById('nav-links');
    const mobileMenu = document.getElementById('mobile-menu');
    const overlay = document.getElementById('menu-overlay');
    const closeButton = document.getElementById('close-mobile-menu');
    
    if (!hamburger || !navLinks) return;
    
    // Añadir clases de transición
    navLinks.classList.add('transition-all', 'duration-300', 'ease-in-out');
    
    // Función para alternar el estado del menú
    function toggleMenu() {
        const isOpen = hamburger.classList.contains('active');
        const spans = hamburger.querySelectorAll('span');
        
        // Alternar clase activa en el botón hamburguesa
        hamburger.classList.toggle('active');
        
        if (!isOpen) {
            // Abrir menú
            if (mobileMenu) {
                // Si existe el contenedor móvil específico
                mobileMenu.classList.remove('translate-x-full');
                mobileMenu.classList.add('translate-x-0');
                if (overlay) {
                    overlay.classList.remove('hidden');
                    // Añadir animación de fade-in al overlay
                    overlay.classList.add('opacity-0');
                    setTimeout(() => {
                        overlay.classList.remove('opacity-0');
                        overlay.classList.add('opacity-100');
                    }, 50);
                }
            } else {
                // Comportamiento alternativo si no existe el contenedor móvil
                navLinks.classList.remove('hidden');
                navLinks.classList.add('flex', 'flex-col', 'absolute', 'top-16', 'right-4', 'bg-white', 'shadow-lg', 'p-6', 'rounded-xl', 'z-50', 'w-64', 'border', 'border-gray-100');
            }
            
            // Animar a X
            if (spans.length >= 3) {
                spans[0].classList.add('rotate-45', 'translate-y-1.5', 'absolute');
                spans[1].classList.add('opacity-0');
                spans[2].classList.add('-rotate-45', '-translate-y-1.5', 'absolute');
            }
            
            // Animar aparición de enlaces con efecto cascada
            const links = (mobileMenu || navLinks).querySelectorAll('a');
            links.forEach((link, index) => {
                link.classList.add('transform', 'translate-x-0', 'opacity-100');
                link.style.transitionDelay = `${index * 0.05}s`;
            });
            
            // Bloquear scroll del body
            document.body.classList.add('overflow-hidden', 'lg:overflow-auto');
        } else {
            // Cerrar menú
            // Animar a hamburguesa
            if (spans.length >= 3) {
                spans[0].classList.remove('rotate-45', 'translate-y-1.5', 'absolute');
                spans[1].classList.remove('opacity-0');
                spans[2].classList.remove('-rotate-45', '-translate-y-1.5', 'absolute');
            }
            
            if (mobileMenu) {
                // Cerrar el menú móvil con animación
                mobileMenu.classList.remove('translate-x-0');
                mobileMenu.classList.add('translate-x-full');
                if (overlay) {
                    // Añadir animación de fade-out al overlay
                    overlay.classList.remove('opacity-100');
                    overlay.classList.add('opacity-0');
                    // Ocultar después de la animación
                    setTimeout(() => {
                        overlay.classList.add('hidden');
                    }, 300);
                }
            } else {
                // Ocultar después de la animación
                setTimeout(() => {
                    navLinks.classList.add('hidden');
                    navLinks.classList.remove('flex', 'flex-col', 'absolute', 'top-16', 'right-4', 'bg-white', 'shadow-lg', 'p-6', 'rounded-xl', 'z-50', 'w-64', 'border', 'border-gray-100');
                }, 300);
            }
            
            // Restaurar scroll
            document.body.classList.remove('overflow-hidden');
        }
    }
    
    /**
     * Función para manejar los submenús en la versión móvil
     * Esta función se expone globalmente para ser usada en los botones de submenú
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
    }
    
    // Evento para el botón hamburguesa
    hamburger.addEventListener('click', function(e) {
        e.stopPropagation();
        toggleMenu();
    });
    
    // Evento para el botón de cierre en el menú móvil
    if (closeButton) {
        closeButton.addEventListener('click', function(e) {
            e.stopPropagation();
            toggleMenu();
        });
    }
    
    // Cerrar menú al hacer clic en overlay
    if (overlay) {
        overlay.addEventListener('click', toggleMenu);
    }
    
    // Cerrar menú al hacer clic en enlaces
    const allLinks = (mobileMenu || navLinks).querySelectorAll('a');
    allLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (hamburger.classList.contains('active')) {
                toggleMenu();
            }
        });
    });
    
    // Cerrar menú al hacer clic fuera
    document.addEventListener('click', function(event) {
        if (hamburger.classList.contains('active') && 
            !hamburger.contains(event.target) && 
            !(mobileMenu ? mobileMenu.contains(event.target) : navLinks.contains(event.target))) {
            toggleMenu();
        }
    });
    
    // Cerrar menú al redimensionar a pantalla grande
    window.addEventListener('resize', function() {
        if (window.innerWidth >= 1024 && hamburger.classList.contains('active')) {
            toggleMenu();
        }
    });
}