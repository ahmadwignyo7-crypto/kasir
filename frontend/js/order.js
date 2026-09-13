// Order functionality
let currentOrder = null;

const STATUS_LABELS = {
    'pending': '⏳ Menunggu',
    'processing': '🔥 Diproses',
    'completed': '🍽️ Siap Diambil',
    'paid': '✅ Selesai'
};

function loadOrderStatus(orderId) {
    getOrder(orderId)
        .then(order => {
            currentOrder = order;
            displayOrderStatus(order);
        })
        .catch(error => {
            console.error('Error loading order:', error);
            const el = document.getElementById('order-status');
            if (el) el.innerHTML = '<p>❌ Gagal memuat pesanan</p>';
        });
}

function loadOrderForPayment(orderId) {
    getOrder(orderId)
        .then(order => {
            currentOrder = order;
            displayOrderSummary(order);
        })
        .catch(error => {
            console.error('Error loading order:', error);
            const el = document.getElementById('order-summary');
            if (el) el.innerHTML = '<p>❌ Gagal memuat pesanan</p>';
        });
}

function displayOrderStatus(order) {
    const orderStatus = document.getElementById('order-status');
    if (!orderStatus) return;

    orderStatus.innerHTML = `
        <div class="queue-number">
            <h2>📋 Nomor Antrian</h2>
            <div class="number">${order.order_number}</div>
        </div>
        <div class="order-details">
            <p><strong>📊 Status:</strong> <span class="status-${order.status}">${STATUS_LABELS[order.status] || order.status}</span></p>
            <p><strong>💰 Total:</strong> Rp ${order.total.toLocaleString()}</p>
            ${order.table_id ? `<p><strong>🪑 Meja:</strong> ${order.table_id}</p>` : ''}
        </div>
        <div class="order-items">
            <h3>🍽️ Item:</h3>
            <ul>
                ${order.items.map(item => `
                    <li>• ${item.name} x${item.qty} - Rp ${(item.price * item.qty).toLocaleString()}</li>
                `).join('')}
            </ul>
        </div>
    `;
}

function displayOrderSummary(order) {
    const summary = document.getElementById('order-summary');
    if (!summary) return;

    summary.innerHTML = `
        <div class="order-card">
            <h2>🧾 Pesanan #${order.order_number}</h2>
            <div class="order-items">
                <ul>
                    ${order.items.map(item => `
                        <li>• ${item.name} x${item.qty} - Rp ${(item.price * item.qty).toLocaleString()}</li>
                    `).join('')}
                </ul>
            </div>
            <div class="order-total">
                <h3>💰 Total: Rp ${order.total.toLocaleString()}</h3>
            </div>
        </div>
    `;
}

function selectPayment(method) {
    const cashPayment = document.getElementById('cash-payment');
    const qrisPayment = document.getElementById('qris-payment');

    if (method === 'cash') {
        cashPayment.style.display = 'block';
        qrisPayment.style.display = 'none';
    } else if (method === 'qris') {
        cashPayment.style.display = 'none';
        qrisPayment.style.display = 'block';
        document.getElementById('qris-image').src =
            'https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=https://example.com/payment';
    }
}

function handleCashPayment() {
    if (!currentOrder) {
        alert('❌ Tidak ada pesanan');
        return;
    }

    const amountPaid = parseInt(document.getElementById('amount-paid').value);
    if (isNaN(amountPaid) || amountPaid <= 0) {
        alert('⚠️ Masukkan jumlah yang valid');
        return;
    }

    if (amountPaid < currentOrder.total) {
        alert('❌ Uang tidak cukup');
        return;
    }

    const paymentData = {
        order_id: currentOrder.id,
        method: 'cash',
        amount_paid: amountPaid
    };

    processPaymentAPI(paymentData)
        .then(payment => {
            if (payment.error) {
                alert('❌ ' + payment.error);
            } else {
                const change = payment.change || 0;
                alert(`✅ Pembayaran berhasil!\n💵 Kembalian: Rp ${change.toLocaleString()}`);
                const mejaParam = getMejaParam();
                window.location.href = `order-status.html?order_id=${currentOrder.id}` + (mejaParam ? '&' + mejaParam.substring(1) : '');
            }
        })
        .catch(error => {
            alert('❌ Gagal memproses pembayaran: ' + error.message);
        });
}

function simulateQRIS() {
    if (!currentOrder) {
        alert('❌ Tidak ada pesanan');
        return;
    }

    const paymentData = {
        order_id: currentOrder.id,
        method: 'qris',
        amount_paid: currentOrder.total
    };

    processPaymentAPI(paymentData)
        .then(payment => {
            if (payment.error) {
                alert('❌ ' + payment.error);
            } else {
                alert('✅ Pembayaran QRIS berhasil!');
                const mejaParam = getMejaParam();
                window.location.href = `order-status.html?order_id=${currentOrder.id}` + (mejaParam ? '&' + mejaParam.substring(1) : '');
            }
        })
        .catch(error => {
            alert('❌ Gagal memproses QRIS: ' + error.message);
        });
}
