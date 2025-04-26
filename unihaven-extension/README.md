# UniHaven Extension

## Overview
The UniHaven Extension is a web application designed to provide accommodation services for multiple universities, including the University of Hong Kong (HKU), Chinese University of Hong Kong (CUHK), and Hong Kong University of Science and Technology (HKUST). This project aims to streamline the accommodation management process for students and university specialists.

## Features
- **University-Specific Pages**: Each university has its own dedicated pages for accommodation listings, details, and login functionalities.
- **Authentication**: Secure login system with token-based authentication for access control.
- **Accommodation Management**: University specialists can manage accommodations, reservations, and view details specific to their institution.
- **Geocoding Services**: Integration of geocoding services to provide location-based information for accommodations.
- **Email Notifications**: Automated email notifications for reservation confirmations and updates.

## Project Structure
```
unihaven-extension
├── src
│   ├── apps
│   │   ├── hku
│   │   ├── cuhk
│   │   └── hkust
│   ├── common
│   ├── static
│   ├── settings
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── requirements.txt
├── .env
└── README.md
```

## Installation
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

## Usage
- Access the accommodation services for each university through the following URLs:
  - HKU: `/hku/accommodations/`
  - CUHK: `/cuhk/accommodations/`
  - HKUST: `/hkust/accommodations/`

- Use the login page to authenticate as a university member.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.