/**
 * Script para el dashboard de administración de LogiXport
 * Este archivo maneja la interacción con el panel de administración
 */

// Ejecutar cuando el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function() {
    // Verificar autenticación
    checkAuthentication();
    
    // Configurar eventos
    setupLogoutButton();
    setupMenuNavigation();
    setupFileUpload();
    setupFormSubmission();
    setupSidebarToggle();
});

/**
 * Configura el botón para mostrar/ocultar el sidebar en dispositivos móviles
 */
function setupSidebarToggle() {
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const sidebar = document.querySelector('.admin-sidebar');
    
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('show');
        });
        
        // Cerrar sidebar al hacer clic en un elemento del menú en dispositivos móviles
        const menuItems = document.querySelectorAll('.menu-item');
        menuItems.forEach(item => {
            item.addEventListener('click', function() {
                if (window.innerWidth <= 768) {
                    sidebar.classList.remove('show');
                }
            });
        });
        
        // Cerrar sidebar al hacer clic fuera de él en dispositivos móviles
        document.addEventListener('click', function(event) {
            if (window.innerWidth <= 768 && 
                !sidebar.contains(event.target) && 
                !sidebarToggle.contains(event.target) &&
                sidebar.classList.contains('show')) {
                sidebar.classList.remove('show');
            }
        });
    }
}

/**
 * Verifica si el usuario está autenticado y es administrador
 */
async function checkAuthentication() {
    try {
        // Verificar si hay un token de acceso
        const token = localStorage.getItem('access_token');
        if (!token) {
            window.location.href = '/login';
            return;
        }
        
        // Obtener información del usuario
        const user = await getCurrentUser();
        if (!user) {
            window.location.href = '/login';
            return;
        }
        
        // Verificar si el usuario es administrador
        if (user.rol !== 'admin') {
            window.location.href = '/dashboard';
            return;
        }
        
        // Mostrar información del usuario en la interfaz
        updateUserInfo(user);
        
    } catch (error) {
        console.error('Error de autenticación:', error);
        window.location.href = '/login';
    }
}

/**
 * Actualiza la información del usuario en la interfaz
 */
function updateUserInfo(user) {
    // Actualizar nombre de usuario en la barra de navegación
    const userNameElement = document.getElementById('user-name');
    if (userNameElement) {
        userNameElement.textContent = user.nombre_usuario || 'Administrador';
    }
    
    // Actualizar correo de usuario en la barra de navegación
    const userEmailElement = document.getElementById('user-email');
    if (userEmailElement) {
        userEmailElement.textContent = user.correo || '';
    }
    
    // Actualizar mensaje de bienvenida personalizado
    const welcomeNameElement = document.getElementById('welcome-name');
    if (welcomeNameElement) {
        welcomeNameElement.textContent = user.nombre_usuario || 'Administrador';
    }
    
    const welcomeEmailElement = document.getElementById('welcome-email');
    if (welcomeEmailElement) {
        welcomeEmailElement.textContent = user.correo || 'correo@ejemplo.com';
    }
}

/**
 * Configura el botón de cierre de sesión
 */
function setupLogoutButton() {
    const logoutBtn = document.querySelector('.logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function() {
            logout(); // Función definida en auth.js
        });
    }
}

/**
 * Configura la navegación del menú lateral
 */
function setupMenuNavigation() {
    const menuItems = document.querySelectorAll('.menu-item');
    menuItems.forEach(item => {
        item.addEventListener('click', function() {
            // Remover clase activa de todos los elementos
            menuItems.forEach(i => i.classList.remove('active'));
            // Agregar clase activa al elemento clickeado
            this.classList.add('active');
            
            // Aquí se podría implementar la navegación entre secciones
            // Por ahora solo cambiamos la clase activa
        });
    });
}

/**
 * Configura la funcionalidad de carga de archivos
 */
function setupFileUpload() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    const fileInfoSection = document.getElementById('fileInfoSection');
    const uploadBtn = document.querySelector('.upload-btn');
    
    if (!uploadArea || !fileInput || !fileInfoSection || !uploadBtn) return;
    
    // Drag and drop functionality
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('drag-over');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('drag-over');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('drag-over');
        const files = e.dataTransfer.files;
        handleFiles(files);
    });

    uploadBtn.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', (e) => {
        handleFiles(e.target.files);
    });
}

/**
 * Maneja los archivos seleccionados
 */
function handleFiles(files) {
    if (files.length > 0) {
        const fileInfoSection = document.getElementById('fileInfoSection');
        if (fileInfoSection) {
            fileInfoSection.style.display = 'block';
            fileInfoSection.scrollIntoView({ behavior: 'smooth' });
            
            // Aquí se podría implementar la lógica para mostrar información de los archivos
            // Por ejemplo, llenar campos automáticamente basados en el nombre del archivo
        }
    }
}

/**
 * Configura el envío del formulario de material
 */
function setupFormSubmission() {
    const materialForm = document.getElementById('materialForm');
    const cancelBtn = document.getElementById('cancelBtn');
    
    if (!materialForm || !cancelBtn) return;
    
    materialForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        try {
            // Obtener datos del formulario
            const formData = new FormData(materialForm);
            const fileInput = document.getElementById('fileInput');
            
            // Agregar archivos al FormData
            if (fileInput && fileInput.files.length > 0) {
                for (let i = 0; i < fileInput.files.length; i++) {
                    formData.append('files', fileInput.files[i]);
                }
            }
            
            // Aquí se implementaría la lógica para enviar los datos al servidor
            // Por ahora solo mostramos un mensaje de éxito
            alert('Material publicado exitosamente!');
            
            // Limpiar formulario
            materialForm.reset();
            fileInput.value = '';
            document.getElementById('fileInfoSection').style.display = 'none';
            
            // Actualizar lista de materiales recientes
            // Esta función se implementaría para obtener los materiales del servidor
            // updateRecentMaterials();
            
        } catch (error) {
            console.error('Error al publicar material:', error);
            alert('Error al publicar material. Por favor, intente nuevamente.');
        }
    });
    
    cancelBtn.addEventListener('click', () => {
        const fileInfoSection = document.getElementById('fileInfoSection');
        const fileInput = document.getElementById('fileInput');
        
        if (fileInfoSection) fileInfoSection.style.display = 'none';
        if (fileInput) fileInput.value = '';
        materialForm.reset();
    });
}