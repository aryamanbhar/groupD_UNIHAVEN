#Overview
A web application providing centralized accommodation management for HKU, CUHK, and HKUST. Designed for students and university specialists to streamline housing reservations, contracts, and notifications.

#Key Features
​University-Specific Portals: Dedicated pages for HKU, CUHK, and HKUST accommodations.
​Secure Authentication: Token-based login system with role-based access control.
​Contract Management: Create/view accommodation contracts (see limitations below).
​Notifications & Emails: Automated reservation confirmations and status updates.
​Geocoding Integration: Location mapping for accommodations.
​Rating System: Student feedback with improved validation logic.

#Limitations
​Contract Creation:
Occasional database integrity errors during contract creation, though contracts are ultimately created successfully. Refresh the /contracts page to verify.
​Email Delivery:
Relies on external SMTP services; delivery failures may occur if not properly configured.
​Rating Display:
Rating updates may require a page refresh to reflect changes.
​Geocoding Accuracy:
Location data depends on third-party API precision.
​Browser Compatibility:
Optimized for modern browsers (Chrome/Firefox/Edge latest versions).
​Access Control:
Contract editing limited to specialists; students can only view contracts.

#Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   cd unihaven-extension
   ```
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
4. Set up environment variables in the `.env` file:
   ```
   SECRET_KEY=<your-secret-key>
   DATABASE_URL=<your-database-url>
   ```
5. Run database migrations:
   ```
   python manage.py migrate
   ```
6. Start the development server:
   ```
   python manage.py runserver
   ```

#Usage
​Accommodation Portals:
HKU: /hku/accommodations
CUHK: /cuhk/accommodations
HKUST: /hkust/accommodations
​Contracts: Create via specialist dashboard, view at /contracts
​Notifications: Check email inbox after reservations/updates

#License: MIT (see LICENSE)
