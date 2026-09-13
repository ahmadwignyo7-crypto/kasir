"""
Phase 8 — Testing KAGO
Sistem Kasir & Pemesanan Berbasis Web
"""
import unittest
import json
import time
import threading
from app import create_app


class KagoTestCase(unittest.TestCase):
    """Base test case dengan Flask test client"""

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.admin_token = None
        self.kasir_token = None
        self.dapur_token = None

    def _login(self, email, password):
        """Helper: login dan return token"""
        resp = self.client.post('/api/auth/login',
                                data=json.dumps({'email': email, 'password': password}),
                                content_type='application/json')
        data = resp.get_json()
        return resp, data

    def _get_admin_token(self):
        if not self.admin_token:
            _, data = self._login('admin@kago.com', 'admin123')
            self.admin_token = data.get('token')
        return self.admin_token

    def _get_kasir_token(self):
        if not self.kasir_token:
            _, data = self._login('kasir@kago.com', 'kasir123')
            self.kasir_token = data.get('token')
        return self.kasir_token

    def _get_dapur_token(self):
        if not self.dapur_token:
            _, data = self._login('dapur@kago.com', 'dapur123')
            self.dapur_token = data.get('token')
        return self.dapur_token

    def _auth_header(self, token):
        return {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}


# ============================================================
# 1. LOGIN & ROLE ACCESS
# ============================================================
class TestAuth(KagoTestCase):

    def test_login_admin_success(self):
        resp, data = self._login('admin@kago.com', 'admin123')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('token', data)
        self.assertEqual(data['role'], 'admin')

    def test_login_kasir_success(self):
        resp, data = self._login('kasir@kago.com', 'kasir123')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('token', data)
        self.assertEqual(data['role'], 'kasir')

    def test_login_dapur_success(self):
        resp, data = self._login('dapur@kago.com', 'dapur123')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('token', data)
        self.assertEqual(data['role'], 'dapur')

    def test_login_wrong_password(self):
        resp, data = self._login('admin@kago.com', 'wrongpassword')
        self.assertEqual(resp.status_code, 401)
        self.assertIn('error', data)

    def test_login_nonexistent_user(self):
        resp, data = self._login('notexist@test.com', 'pass123')
        self.assertEqual(resp.status_code, 401)

    def test_login_missing_fields(self):
        resp = self.client.post('/api/auth/login',
                                data=json.dumps({}),
                                content_type='application/json')
        self.assertEqual(resp.status_code, 401)


# ============================================================
# 2. CRUD MENU
# ============================================================
class TestMenuCRUD(KagoTestCase):

    def setUp(self):
        super().setUp()
        self._created_menu_id = None

    def test_get_menus(self):
        resp = self.client.get('/api/menu/')
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIsInstance(data, list)

    def test_create_menu(self):
        menu_data = {
            'name': 'Test Nasi Goreng',
            'price': 25000,
            'category_id': '',
            'image_url': '',
            'is_available': True
        }
        resp = self.client.post('/api/menu/',
                                data=json.dumps(menu_data),
                                content_type='application/json')
        self.assertEqual(resp.status_code, 201)
        data = resp.get_json()
        self.assertIn('id', data)
        self._created_menu_id = data['id']

    def test_update_menu(self):
        # Create first
        menu_data = {'name': 'Test Update', 'price': 10000, 'is_available': True}
        resp = self.client.post('/api/menu/',
                                data=json.dumps(menu_data),
                                content_type='application/json')
        menu_id = resp.get_json()['id']

        # Update
        update_data = {'name': 'Test Updated', 'price': 15000}
        resp = self.client.put(f'/api/menu/{menu_id}',
                               data=json.dumps(update_data),
                               content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()['name'], 'Test Updated')

    def test_delete_menu(self):
        # Create first
        menu_data = {'name': 'Test Delete', 'price': 5000, 'is_available': True}
        resp = self.client.post('/api/menu/',
                                data=json.dumps(menu_data),
                                content_type='application/json')
        menu_id = resp.get_json()['id']

        # Delete
        resp = self.client.delete(f'/api/menu/{menu_id}')
        self.assertEqual(resp.status_code, 200)

    def test_create_menu_empty_data(self):
        resp = self.client.post('/api/menu/',
                                data=json.dumps({}),
                                content_type='application/json')
        self.assertEqual(resp.status_code, 400)


# ============================================================
# 3. CRUD KATEGORI
# ============================================================
class TestCategoryCRUD(KagoTestCase):

    def test_get_categories(self):
        resp = self.client.get('/api/menu/categories')
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIsInstance(data, list)

    def test_create_category(self):
        cat_data = {'name': 'Test Kategori'}
        resp = self.client.post('/api/menu/categories',
                                data=json.dumps(cat_data),
                                content_type='application/json')
        self.assertEqual(resp.status_code, 201)
        data = resp.get_json()
        self.assertIn('id', data)

    def test_delete_category(self):
        # Create first
        cat_data = {'name': 'Test Hapus'}
        resp = self.client.post('/api/menu/categories',
                                data=json.dumps(cat_data),
                                content_type='application/json')
        cat_id = resp.get_json()['id']

        # Delete
        resp = self.client.delete(f'/api/menu/categories/{cat_id}')
        self.assertEqual(resp.status_code, 200)

    def test_create_category_missing_name(self):
        resp = self.client.post('/api/menu/categories',
                                data=json.dumps({}),
                                content_type='application/json')
        self.assertEqual(resp.status_code, 400)


# ============================================================
# 4. CRUD MEJA + QR
# ============================================================
class TestTableCRUD(KagoTestCase):

    def test_get_tables(self):
        resp = self.client.get('/api/table/')
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIsInstance(data, list)

    def test_create_table(self):
        table_data = {'table_number': '99', 'status': 'available'}
        resp = self.client.post('/api/table/',
                                data=json.dumps(table_data),
                                content_type='application/json')
        self.assertEqual(resp.status_code, 201)
        data = resp.get_json()
        self.assertIn('id', data)

    def test_update_table(self):
        # Create
        table_data = {'table_number': '98', 'status': 'available'}
        resp = self.client.post('/api/table/',
                                data=json.dumps(table_data),
                                content_type='application/json')
        table_id = resp.get_json()['id']

        # Update
        update_data = {'status': 'occupied'}
        resp = self.client.put(f'/api/table/{table_id}',
                               data=json.dumps(update_data),
                               content_type='application/json')
        self.assertEqual(resp.status_code, 200)

    def test_delete_table(self):
        table_data = {'table_number': '97', 'status': 'available'}
        resp = self.client.post('/api/table/',
                                data=json.dumps(table_data),
                                content_type='application/json')
        table_id = resp.get_json()['id']

        resp = self.client.delete(f'/api/table/{table_id}')
        self.assertEqual(resp.status_code, 200)

    def test_generate_qr(self):
        # Get existing tables first
        resp = self.client.get('/api/table/')
        tables = resp.get_json()
        if tables:
            table_id = tables[0]['id']
            resp = self.client.get(f'/api/table/{table_id}/qr')
            self.assertEqual(resp.status_code, 200)
            data = resp.get_json()
            self.assertIn('qr_url', data)

    def test_generate_qr_nonexistent(self):
        resp = self.client.get('/api/table/nonexistent_id/qr')
        self.assertEqual(resp.status_code, 404)


# ============================================================
# 5. ALUR PEMESANAN (ORDER)
# ============================================================
class TestOrderFlow(KagoTestCase):

    def test_create_order(self):
        order_data = {
            'table_id': '',
            'order_type': 'dine_in',
            'total': 50000,
            'items': [
                {'menu_id': 'test', 'name': 'Nasi Goreng', 'price': 25000, 'qty': 2}
            ]
        }
        resp = self.client.post('/api/order/',
                                data=json.dumps(order_data),
                                content_type='application/json')
        self.assertEqual(resp.status_code, 201)
        data = resp.get_json()
        self.assertIn('id', data)
        self.assertIn('order_number', data)
        self.assertEqual(data['status'], 'pending')

    def test_get_orders(self):
        resp = self.client.get('/api/order/')
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIsInstance(data, list)

    def test_get_single_order(self):
        # Create order first
        order_data = {
            'table_id': '',
            'order_type': 'takeaway',
            'total': 30000,
            'items': [{'menu_id': 'm1', 'name': 'Es Teh', 'price': 10000, 'qty': 3}]
        }
        resp = self.client.post('/api/order/',
                                data=json.dumps(order_data),
                                content_type='application/json')
        order_id = resp.get_json()['id']

        resp = self.client.get(f'/api/order/{order_id}')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()['order_number'], resp.get_json()['order_number'])

    def test_get_nonexistent_order(self):
        resp = self.client.get('/api/order/fake_id_123')
        self.assertEqual(resp.status_code, 404)

    def test_update_order_status(self):
        # Create order
        order_data = {
            'table_id': '',
            'order_type': 'dine_in',
            'total': 20000,
            'items': [{'menu_id': 'm1', 'name': 'Kopi', 'price': 20000, 'qty': 1}]
        }
        resp = self.client.post('/api/order/',
                                data=json.dumps(order_data),
                                content_type='application/json')
        order_id = resp.get_json()['id']

        # Update status
        resp = self.client.put(f'/api/order/{order_id}/status',
                               data=json.dumps({'status': 'processing'}),
                               content_type='application/json')
        self.assertEqual(resp.status_code, 200)

    def test_update_order_invalid_status(self):
        order_data = {
            'table_id': '',
            'order_type': 'dine_in',
            'total': 15000,
            'items': []
        }
        resp = self.client.post('/api/order/',
                                data=json.dumps(order_data),
                                content_type='application/json')
        order_id = resp.get_json()['id']

        resp = self.client.put(f'/api/order/{order_id}/status',
                               data=json.dumps({'status': 'invalid_status'}),
                               content_type='application/json')
        self.assertEqual(resp.status_code, 400)

    def test_order_status_flow(self):
        """Test full status flow: pending → processing → completed → paid"""
        order_data = {
            'table_id': '',
            'order_type': 'dine_in',
            'total': 40000,
            'items': [{'menu_id': 'm1', 'name': 'Mie Ayam', 'price': 40000, 'qty': 1}]
        }
        resp = self.client.post('/api/order/',
                                data=json.dumps(order_data),
                                content_type='application/json')
        order_id = resp.get_json()['id']

        for status in ['processing', 'completed', 'paid']:
            resp = self.client.put(f'/api/order/{order_id}/status',
                                   data=json.dumps({'status': status}),
                                   content_type='application/json')
            self.assertEqual(resp.status_code, 200, f"Gagal update ke {status}")


# ============================================================
# 6. PEMBAYARAN (PAYMENT)
# ============================================================
class TestPayment(KagoTestCase):

    def _create_order(self, total=50000):
        order_data = {
            'table_id': '',
            'order_type': 'dine_in',
            'total': total,
            'items': [{'menu_id': 'm1', 'name': 'Nasi Goreng', 'price': total, 'qty': 1}]
        }
        resp = self.client.post('/api/order/',
                                data=json.dumps(order_data),
                                content_type='application/json')
        return resp.get_json()['id']

    def test_payment_cash_success(self):
        order_id = self._create_order(50000)
        payment_data = {
            'order_id': order_id,
            'method': 'cash',
            'amount_paid': 60000
        }
        resp = self.client.post('/api/payment/',
                                data=json.dumps(payment_data),
                                content_type='application/json')
        self.assertEqual(resp.status_code, 201)
        data = resp.get_json()
        self.assertEqual(data['method'], 'cash')
        self.assertEqual(data['change'], 10000)

    def test_payment_cash_exact(self):
        order_id = self._create_order(30000)
        payment_data = {
            'order_id': order_id,
            'method': 'cash',
            'amount_paid': 30000
        }
        resp = self.client.post('/api/payment/',
                                data=json.dumps(payment_data),
                                content_type='application/json')
        self.assertEqual(resp.status_code, 201)
        data = resp.get_json()
        self.assertEqual(data['change'], 0)

    def test_payment_cash_insufficient(self):
        order_id = self._create_order(50000)
        payment_data = {
            'order_id': order_id,
            'method': 'cash',
            'amount_paid': 40000
        }
        resp = self.client.post('/api/payment/',
                                data=json.dumps(payment_data),
                                content_type='application/json')
        self.assertEqual(resp.status_code, 400)
        self.assertIn('error', resp.get_json())

    def test_payment_qris(self):
        order_id = self._create_order(75000)
        payment_data = {
            'order_id': order_id,
            'method': 'qris',
            'amount_paid': 0
        }
        resp = self.client.post('/api/payment/',
                                data=json.dumps(payment_data),
                                content_type='application/json')
        self.assertEqual(resp.status_code, 201)
        data = resp.get_json()
        self.assertEqual(data['method'], 'qris')
        self.assertEqual(data['amount_paid'], 75000)

    def test_payment_nonexistent_order(self):
        payment_data = {
            'order_id': 'fake_order_id',
            'method': 'cash',
            'amount_paid': 50000
        }
        resp = self.client.post('/api/payment/',
                                data=json.dumps(payment_data),
                                content_type='application/json')
        self.assertEqual(resp.status_code, 400)

    def test_payment_missing_fields(self):
        resp = self.client.post('/api/payment/',
                                data=json.dumps({}),
                                content_type='application/json')
        self.assertEqual(resp.status_code, 400)

    def test_get_payment(self):
        order_id = self._create_order(25000)
        payment_data = {
            'order_id': order_id,
            'method': 'cash',
            'amount_paid': 30000
        }
        resp = self.client.post('/api/payment/',
                                data=json.dumps(payment_data),
                                content_type='application/json')
        payment_id = resp.get_json()['id']

        resp = self.client.get(f'/api/payment/{payment_id}')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()['order_id'], order_id)


# ============================================================
# 7. CONCURRENCY TEST — ORDER COUNTER
# ============================================================
class TestConcurrency(KagoTestCase):

    def test_concurrent_order_creation(self):
        """Buat 5 order secara bersamaan, pastikan nomor antrian unik"""
        order_numbers = []
        errors = []

        def create_order(idx):
            try:
                order_data = {
                    'table_id': '',
                    'order_type': 'dine_in',
                    'total': 10000 * (idx + 1),
                    'items': [{'menu_id': f'm{idx}', 'name': f'Item {idx}', 'price': 10000 * (idx + 1), 'qty': 1}]
                }
                resp = self.client.post('/api/order/',
                                        data=json.dumps(order_data),
                                        content_type='application/json')
                if resp.status_code == 201:
                    data = resp.get_json()
                    order_numbers.append(data['order_number'])
                else:
                    errors.append(f"Order {idx} gagal: {resp.status_code}")
            except Exception as e:
                errors.append(f"Order {idx} error: {str(e)}")

        threads = [threading.Thread(target=create_order, args=(i,)) for i in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(len(errors), 0, f"Errors: {errors}")
        self.assertEqual(len(order_numbers), 5)
        # Pastikan semua nomor antrian unik
        self.assertEqual(len(set(order_numbers)), 5, "Ada nomor antrian duplikat!")
        print(f"\n  [OK] Concurrent order numbers: {order_numbers}")


# ============================================================
# 8. FRONTEND PAGES TEST
# ============================================================
class TestFrontendPages(KagoTestCase):

    def test_login_page(self):
        resp = self.client.get('/login.html')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'KAGO', resp.data)

    def test_index_page(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_customer_menu_page(self):
        resp = self.client.get('/customer/menu.html')
        self.assertEqual(resp.status_code, 200)

    def test_cashier_dashboard_page(self):
        resp = self.client.get('/cashier/dashboard.html')
        self.assertEqual(resp.status_code, 200)

    def test_kitchen_dashboard_page(self):
        resp = self.client.get('/kitchen/dashboard.html')
        self.assertEqual(resp.status_code, 200)

    def test_admin_dashboard_page(self):
        resp = self.client.get('/admin/dashboard.html')
        self.assertEqual(resp.status_code, 200)

    def test_order_page(self):
        resp = self.client.get('/order')
        self.assertEqual(resp.status_code, 200)


# ============================================================
# RUN TESTS
# ============================================================
if __name__ == '__main__':
    print("=" * 60)
    print("  KAGO — Phase 8 Testing")
    print("=" * 60)
    unittest.main(verbosity=2)
