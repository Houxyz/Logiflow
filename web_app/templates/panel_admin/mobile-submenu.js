/**
 * Script para implementar submenús móviles en el panel de administración
 * Este archivo agrega los botones de submenú necesarios para el dashboard de administración
 */

document.addEventListener('DOMContentLoaded', function() {
    initAdminMobileSubmenus();
});

/**
 * Inicializa los submenús móviles para el panel de administración
 */
function initAdminMobileSubmenus() {
    // Secciones que necesitan submenús
    const sections = [
        {
            title: 'Material Didáctico',
            id: 'material',
            items: [
                { name: 'Cargar Material', icon: 'fa-upload', section: 'upload-section' },
                { name: 'Gestionar Archivos', icon: 'fa-folder-open', section: 'files-section' },
                { name: 'Categorías', icon: 'fa-tags', section: 'categories-section' }
            ]
        },
        {
            title: 'Leyes y Normativas',
            id: 'leyes',
            items: [
                { name: 'Importación', icon: 'fa-balance-scale', section: 'import-section' },
                { name: 'Exportación', icon: 'fa-shipping-fast', section: 'export-section' },
                { name: 'Normativas', icon: 'fa-gavel', section: 'regulations-section' }
            ]
        },
        {
            title: 'Gestión',
            id: 'gestion',
            items: [
                { name: 'Usuarios', icon: 'fa-users', section: 'users-section' },
                { name: 'Suscripciones', icon: 'fa-crown', section: 'subscriptions-section' }
            ]
        }
    ];
    
    // Crear los botones de submenú móvil
    createMobileSubmenus(sections);
    
    // Inicializar los eventos para los botones de submenú
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

/**
 * Crea los botones y submenús móviles para las secciones especificadas
 * @param {Array} sections - Las secciones para las que crear submenús
 */
function createMobileSubmenus(sections) {
    // Solo crear los submenús en dispositivos móviles
    if (window.innerWidth >= 768) return;
    
    const sidebar = document.getElementById('sidebar');
    if (!sidebar) return;
    
    // Para cada sección, crear un botón de submenú y sus elementos
    sections.forEach(section => {
        // Buscar el encabezado de la sección
        const sectionHeader = Array.from(sidebar.querySelectorAll('h3')).find(h => 
            h.textContent.trim() === section.title
        );
        
        if (sectionHeader) {
            // Crear el botón de submenú
            const submenuBtn = document.createElement('button');
            submenuBtn.id = `${section.id}-submenu-btn`;
            submenuBtn.setAttribute('data-target', `${section.id}-submenu`);
            submenuBtn.className = 'flex items-center justify-between w-full p-3 rounded-lg hover:bg-white/10 transition-all duration-300';
            submenuBtn.innerHTML = `
                <div class="flex items-center">
                    <i class="fas fa-list-ul w-5 text-center mr-3 text-secondary"></i>
                    <span>${section.title}</span>
                </div>
                <i class="fas fa-chevron-down text-xs transition-transform" id="${section.id}-icon"></i>
            `;
            
            // Crear el contenedor del submenú
            const submenu = document.createElement('div');
            submenu.id = `${section.id}-submenu`;
            submenu.className = 'hidden ml-5 space-y-1 mt-1 mb-2';
            
            // Agregar los elementos del submenú
            section.items.forEach(item => {
                const menuItem = document.createElement('a');
                menuItem.href = '#';
                menuItem.className = 'flex items-center p-2 rounded-lg hover:bg-white/10 transition-all duration-300 pl-5';
                menuItem.setAttribute('data-section', item.section);
                menuItem.innerHTML = `
                    <i class="fas ${item.icon} w-5 text-center mr-3 text-secondary"></i>
                    <span>${item.name}</span>
                `;
                
                // Agregar evento para cambiar de sección
                menuItem.addEventListener('click', function(e) {
                    e.preventDefault();
                    const sectionId = this.getAttribute('data-section');
                    const menuItems = document.querySelectorAll('.menu-item');
                    
                    // Activar el elemento de menú correspondiente
                    menuItems.forEach(item => {
                        if (item.getAttribute('data-section') === sectionId) {
                            item.querySelector('a').click();
                        }
                    });
                });
                
                submenu.appendChild(menuItem);
            });
            
            // Reemplazar la lista existente con el botón y submenú
            const existingList = sectionHeader.nextElementSibling;
            if (existingList && existingList.tagName === 'UL') {
                // En dispositivos móviles, ocultar la lista original
                existingList.classList.add('hidden', 'md:block');
                
                // Insertar el botón y submenú después del encabezado
                sectionHeader.parentNode.insertBefore(submenuBtn, existingList);
                sectionHeader.parentNode.insertBefore(submenu, existingList.nextSibling);
            }
        }
    });
}

// Actualizar los submenús al cambiar el tamaño de la ventana
window.addEventListener('resize', function() {
    // Eliminar los submenús móviles en dispositivos de escritorio
    if (window.innerWidth >= 768) {
        document.querySelectorAll('[id$="-submenu-btn"]').forEach(btn => {
            btn.style.display = 'none';
        });
        document.querySelectorAll('[id$="-submenu"]').forEach(menu => {
            menu.style.display = 'none';
        });
        document.querySelectorAll('ul.hidden.md\\:block').forEach(list => {
            list.classList.remove('hidden');
        });
    } else {
        // Mostrar los submenús móviles en dispositivos móviles
        document.querySelectorAll('[id$="-submenu-btn"]').forEach(btn => {
            btn.style.display = 'flex';
        });
        document.querySelectorAll('ul.hidden.md\\:block').forEach(list => {
            list.classList.add('hidden');
        });
    }
});