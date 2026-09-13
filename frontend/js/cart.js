// Cart functionality
let cart = JSON.parse(localStorage.getItem('cart')) || [];

function addToCart(menuId, name, price) {
    const existingItem = cart.find(item => item.menuId === menuId);
    if (existingItem) {
        existingItem.qty += 1;
    } else {
        cart.push({ menuId, name, price, qty: 1 });
    }
    saveCart();
    alert(`${name} ditambahkan ke keranjang`);
}

function removeFromCart(menuId) {
    cart = cart.filter(item => item.menuId !== menuId);
    saveCart();
    displayCart();
}

function updateCartQuantity(menuId, qty) {
    const item = cart.find(item => item.menuId === menuId);
    if (item) {
        item.qty = qty;
        if (item.qty <= 0) {
            removeFromCart(menuId);
        } else {
            saveCart();
            displayCart();
        }
    }
}

function getCart() { return cart; }

function getCartCount() {
    return cart.reduce((total, item) => total + item.qty, 0);
}

function getCartTotal() {
    return cart.reduce((total, item) => total + (item.price * item.qty), 0);
}

function clearCart() {
    cart = [];
    saveCart();
}

function saveCart() {
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartBadge();
}

function updateCartBadge() {
    const badge = document.getElementById('cart-badge');
    if (badge) {
        const count = getCartCount();
        badge.textContent = count;
        badge.style.display = count > 0 ? 'inline' : 'none';
    }
}

function getTableFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('meja') || '';
}

function getMejaParam() {
    const urlParams = new URLSearchParams(window.location.search);
    const meja = urlParams.get('meja') || '';
    const orderType = urlParams.get('order_type') || '';
    const params = [];
    if (meja) params.push('meja=' + encodeURIComponent(meja));
    if (orderType) params.push('order_type=' + encodeURIComponent(orderType));
    return params.length > 0 ? '?' + params.join('&') : '';
}

function viewCart() {
    const params = getMejaParam();
    window.location.href = 'cart.html' + params;
}

function displayCart() {
    const cartItems = document.getElementById('cart-items');
    const cartTotal = document.getElementById('cart-total');
    const tableInfo = document.getElementById('table-info');

    if (!cartItems) return;

    // Show table info if present
    if (tableInfo) {
        const meja = getTableFromURL();
        if (meja) {
            tableInfo.textContent = 'Meja ' + meja;
            tableInfo.style.display = 'block';
        } else {
            tableInfo.style.display = 'none';
        }
    }

    if (cart.length === 0) {
        cartItems.innerHTML = '<p class="empty-cart">Keranjang kosong</p>';
        if (cartTotal) cartTotal.innerHTML = '';
        return;
    }

    cartItems.innerHTML = cart.map(item => `
        <div class="cart-item">
            <div class="cart-item-info">
                <h3>${item.name}</h3>
                <p>Rp ${item.price.toLocaleString()}</p>
            </div>
            <div class="cart-item-controls">
                <button class="btn-qty" onclick="updateCartQuantity('${item.menuId}', ${item.qty - 1})">-</button>
                <span>${item.qty}</span>
                <button class="btn-qty" onclick="updateCartQuantity('${item.menuId}', ${item.qty + 1})">+</button>
            </div>
            <div class="cart-item-subtotal">
                <p>Rp ${(item.price * item.qty).toLocaleString()}</p>
                <button class="btn-remove" onclick="removeFromCart('${item.menuId}')">Hapus</button>
            </div>
        </div>
    `).join('');

    if (cartTotal) {
        cartTotal.innerHTML = `
            <div class="cart-summary">
                <h3>Total: Rp ${getCartTotal().toLocaleString()}</h3>
                <button class="btn-checkout" onclick="checkout()">Checkout</button>
            </div>
        `;
    }
}

function checkout() {
    if (cart.length === 0) {
        alert('Keranjang kosong');
        return;
    }

    const tableId = getTableFromURL();
    const urlParams = new URLSearchParams(window.location.search);
    const orderType = urlParams.get('order_type') || (tableId ? 'qr' : 'kasir');

    if (orderType === 'dine_in' && !tableId) {
        var meja = prompt('Masukkan nomor meja (1-10):');
        if (!meja || isNaN(meja) || parseInt(meja) < 1 || parseInt(meja) > 10) {
            alert('Nomor meja harus antara 1 - 10');
            return;
        }
        doCheckout(String(meja), orderType);
        return;
    }

    doCheckout(tableId, orderType);
}

function doCheckout(tableId, orderType) {
    const orderData = {
        table_id: tableId || '',
        order_type: orderType,
        total: getCartTotal(),
        items: cart.map(item => ({
            menu_id: item.menuId,
            name: item.name,
            price: item.price,
            qty: item.qty,
            note: ''
        }))
    };

    createOrder(orderData)
        .then(order => {
            clearCart();
            window.location.href = `order-status.html?order_id=${order.id}` + getMejaParam();
        })
        .catch(error => {
            alert('Gagal membuat pesanan: ' + error.message);
        });
}
