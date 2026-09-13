# KAGO - Sistem Kasir & Pemesanan Berbasis Web

## Overview
KAGO is a web-based cashier and ordering system built with Python (Flask) and Firebase (Firestore). It supports role-based access for admin, cashier, and kitchen staff, with real-time order tracking and QR code ordering for customers.

## Features
- User authentication with JWT and bcrypt
- Role-based access control (admin, cashier, kitchen)
- Menu and category management
- Table management with QR code generation
- Order processing with real-time status updates
- Payment processing (cash and dummy QRIS)
- Kitchen dashboard with live order updates
- Customer self-ordering via QR codes

## Tech Stack
- **Backend**: Python 3, Flask
- **Frontend**: HTML, CSS, JavaScript
- **Database**: Firebase Firestore
- **Storage**: Firebase Storage
- **Authentication**: JWT (PyJWT) + Flask-Bcrypt

## Installation

### Prerequisites
- Python 3.7+
- pip
- Firebase project with Firestore and Storage enabled

### Setup
1. Clone the repository
2. Navigate to the backend directory:
   ```bash
   cd backend
   ```
3. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
4. Activate the virtual environment:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
6. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Update the values in `.env` with your configuration

### Firebase Setup
1. Create a Firebase project in the [Firebase Console](https://console.firebase.google.com/)
2. Enable Firestore Database
3. Enable Firebase Storage
4. Generate a service account key (Project Settings > Service Accounts > Generate New Private Key)
5. Save the key as `serviceAccountKey.json` in the backend directory

## Usage
1. Start the Flask development server:
   ```bash
   python run.py
   ```
2. Open your browser and navigate to `http://localhost:5000`

### User Roles
- **Admin**: Can manage menu, categories, tables, and view reports
- **Cashier**: Can process orders and payments
- **Kitchen**: Can view and update order statuses in real-time
- **Customer**: Can scan QR codes to view menu and place orders

## Project Structure
```
KAGO/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── extensions.py
│   │   ├── routes/
│   │   ├── services/
│   │   └── middleware/
│   ├── serviceAccountKey.json
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── customer/
│   ├── cashier/
│   ├── kitchen/
│   ├── admin/
│   ├── css/
│   └── js/
├── .env
├── package.json
└── README.md
```

## API Endpoints
- `POST /api/auth/login` - User login
- `GET /api/menu/` - Get all menu items
- `POST /api/menu/` - Create new menu item
- `PUT /api/menu/<menu_id>` - Update menu item
- `DELETE /api/menu/<menu_id>` - Delete menu item
- `GET /api/order/` - Get all orders
- `POST /api/order/` - Create new order
- `GET /api/order/<order_id>` - Get order by ID
- `PUT /api/order/<order_id>/status` - Update order status
- `POST /api/payment/` - Process payment
- `GET /api/payment/<payment_id>` - Get payment by ID
- `GET /api/table/` - Get all tables
- `POST /api/table/` - Create new table
- `PUT /api/table/<table_id>` - Update table
- `DELETE /api/table/<table_id>` - Delete table
- `GET /api/table/<table_id>/qr` - Generate QR code for table

## Development
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Test all functionality before deployment

## License
This project is licensed under the MIT License.
