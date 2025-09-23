/**
 * Funciones de autenticación para LogiXport
 * Este archivo maneja la interacción con los endpoints de autenticación
 */

// URL base para las peticiones de autenticación
const AUTH_BASE_URL = '/auth';

// Función para iniciar sesión
async function login(email, password, rememberMe = false) {
    try {
        const response = await fetch(`${AUTH_BASE_URL}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email,
                password: password,
                remember_me: rememberMe
            })
        });

        // Verificar si la respuesta es exitosa
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Error al iniciar sesión');
        }

        // Procesar respuesta exitosa
        const data = await response.json();
        
        // Guardar token y datos de usuario en localStorage
        localStorage.setItem('access_token', data.access_token);
        localStorage.setItem('token_type', data.token_type);
        localStorage.setItem('expires_in', data.expires_in);
        localStorage.setItem('user', JSON.stringify(data.user));
        localStorage.setItem('isLoggedIn', 'true');
        
        // Determinar redirección basada en el rol del usuario
        if (data.user.rol === 'admin') {
            window.location.href = '/admin';
        } else {
            window.location.href = '/dashboard';
        }
        
        return data;
    } catch (error) {
        console.error('Error de inicio de sesión:', error);
        throw error;
    }
}

// Función para verificar si el usuario está autenticado
async function isAuthenticated() {
    const token = localStorage.getItem('access_token');
    if (!token) {
        return false;
    }
    
    try {
        // Verificar validez del token con el servidor
        const response = await fetch(`${AUTH_BASE_URL}/verify`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        return response.ok;
    } catch (error) {
        console.error('Error al verificar autenticación:', error);
        return false;
    }
}

// Función para obtener información del usuario actual
async function getCurrentUser() {
    const userJson = localStorage.getItem('user');
    if (userJson) {
        return JSON.parse(userJson);
    }
    
    const token = localStorage.getItem('access_token');
    if (!token) {
        return null;
    }
    
    try {
        // Obtener información actualizada del usuario desde el servidor
        const response = await fetch(`${AUTH_BASE_URL}/me`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) {
            throw new Error('No se pudo obtener información del usuario');
        }
        
        const userData = await response.json();
        localStorage.setItem('user', JSON.stringify(userData));
        return userData;
    } catch (error) {
        console.error('Error al obtener usuario:', error);
        return null;
    }
}

// Función para cerrar sesión
function logout() {
    // Eliminar datos de sesión del localStorage
    localStorage.removeItem('access_token');
    localStorage.removeItem('token_type');
    localStorage.removeItem('expires_in');
    localStorage.removeItem('user');
    localStorage.removeItem('isLoggedIn');
    
    // Redireccionar a la página de login
    window.location.href = '/login';
}

// Función para proteger rutas que requieren autenticación
async function requireAuth() {
    const isLoggedIn = await isAuthenticated();
    if (!isLoggedIn) {
        // Guardar la URL actual para redireccionar después del login
        localStorage.setItem('redirect_after_login', window.location.pathname);
        window.location.href = '/login';
        return false;
    }
    return true;
}

// Función para redireccionar después del login si hay una URL guardada
function redirectAfterLogin() {
    const redirectUrl = localStorage.getItem('redirect_after_login');
    if (redirectUrl) {
        localStorage.removeItem('redirect_after_login');
        window.location.href = redirectUrl;
    }
}