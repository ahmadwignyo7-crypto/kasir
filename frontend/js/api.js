// API Helper functions
const API_BASE_URL = '/api';

function getToken() {
    return localStorage.getItem('token');
}

function setToken(token) {
    localStorage.setItem('token', token);
}

function removeToken() {
    localStorage.removeItem('token');
}

function getUserRole() {
    return localStorage.getItem('role');
}

function setUserRole(role) {
    localStorage.setItem('role', role);
}

async function apiRequest(endpoint, method = 'GET', data = null) {
    const url = `${API_BASE_URL}${endpoint}`;
    const headers = {
        'Content-Type': 'application/json',
    };

    const token = getToken();
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const options = { method, headers };

    if (data) {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(url, options);
        const result = await response.json();
        if (!response.ok) {
            throw new Error(result.error || `HTTP error! status: ${response.status}`);
        }
        return result;
    } catch (error) {
        console.error('API request failed:', error);
        throw error;
    }
}

// Authentication
async function login(email, password) {
    const result = await apiRequest('/auth/login', 'POST', { email, password });
    if (result.token) {
        setToken(result.token);
        setUserRole(result.role);
    }
    return result;
}

function logout() {
    removeToken();
    localStorage.removeItem('role');
    window.location.href = '/';
}

function isLoggedIn() {
    return !!getToken();
}

// Menu
async function getMenus() {
    return apiRequest('/menu/');
}

async function getMenu(menuId) {
    return apiRequest(`/menu/${menuId}`);
}

async function createMenu(data) {
    return apiRequest('/menu/', 'POST', data);
}

async function updateMenu(menuId, data) {
    return apiRequest(`/menu/${menuId}`, 'PUT', data);
}

async function deleteMenu(menuId) {
    return apiRequest(`/menu/${menuId}`, 'DELETE');
}

// Categories (via menu routes)
async function getCategories() {
    return apiRequest('/menu/categories');
}

async function createCategory(data) {
    return apiRequest('/menu/categories', 'POST', data);
}

async function deleteCategory(catId) {
    return apiRequest(`/menu/categories/${catId}`, 'DELETE');
}

// Orders
async function getOrders() {
    return apiRequest('/order/');
}

async function getOrder(orderId) {
    return apiRequest(`/order/${orderId}`);
}

async function createOrder(data) {
    return apiRequest('/order/', 'POST', data);
}

async function updateOrderStatus(orderId, status) {
    return apiRequest(`/order/${orderId}/status`, 'PUT', { status });
}

// Payments
async function processPaymentAPI(data) {
    return apiRequest('/payment/', 'POST', data);
}

async function getPayment(paymentId) {
    return apiRequest(`/payment/${paymentId}`);
}

// Tables
async function getTables() {
    return apiRequest('/table/');
}

async function createTable(data) {
    return apiRequest('/table/', 'POST', data);
}

async function updateTable(tableId, data) {
    return apiRequest(`/table/${tableId}`, 'PUT', data);
}

async function deleteTable(tableId) {
    return apiRequest(`/table/${tableId}`, 'DELETE');
}

async function generateTableQR(tableId) {
    return apiRequest(`/table/${tableId}/qr`);
}
