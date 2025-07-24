# Electronics Shop Inventory Management System

A Django-based inventory management system for an electronics shop selling mobiles, laptops, and smart watches.

## Features

- Product Management (CRUD Operations)
- Stock Management
- User Authentication
- Sales Tracking
- Stock Alerts
- Supplier Management
- Bulk Import/Export
- Product Images

## Setup Instructions

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Apply migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

4. Load initial data:
   ```bash
   python manage.py loaddata initial_data.json
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

6. Access the application:
   - Admin interface: http://127.0.0.1:8000/admin/
   - Main application: http://127.0.0.1:8000/

## Directory Structure

- `inventory/`: Main application directory
  - `templates/`: HTML templates
  - `static/`: Static files (CSS, JS, images)
  - `models.py`: Database models
  - `views.py`: View functions
  - `urls.py`: URL configurations

## Usage

1. Login using your superuser credentials
2. Add products through the admin interface or the main application
3. Manage inventory, track sales, and monitor stock levels
4. Export inventory data as needed

