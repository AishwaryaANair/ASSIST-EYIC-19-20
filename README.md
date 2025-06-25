ASSIST Project for E-Yantra Ideas Competition# ASSIST-EYIC-19-20

IoT Assist Web Application - A modern PHP-based web application for IoT device management and assistance.

## Features

- Secure user authentication
- IoT device management
- Emergency response system
- Voice login capability
- Modern, responsive UI

## Requirements

- PHP 7.4 or higher
- MySQL/MariaDB
- Composer
- Web server (Apache/Nginx)

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   composer install
   ```

3. Copy `.env.example` to `.env` and configure:
   ```bash
   cp .env.example .env
   ```
   Update the following variables:
   - `DB_HOST`
   - `DB_NAME`
   - `DB_USER`
   - `DB_PASS`

4. Set up database:
   - Create the database
   - Import the SQL schema

5. Configure web server:
   - Point web root to `/public`
   - Enable URL rewriting

## Security

- Uses modern password hashing (bcrypt)
- SQL injection prevention (PDO prepared statements)
- CSRF protection
- XSS prevention
- Secure session handling

## Directory Structure

```
src/
├── Auth/           # Authentication classes
├── Database/       # Database connection and models
├── Controllers/    # MVC controllers
├── Views/          # MVC views
├── Public/         # Web accessible files
└── Config/         # Configuration files
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details

To install the application:

1. Paste this folder in the xampp htdocs folder. Import the assist.sql file into your phpmyadmin database.
2. Replace the username and password in the connection.php files in the parent and admin directory as required.
3. Use the email Ids of assistadmin@gmail.com and assistuser@gmail.com to log in to admin and user panels with the passwords mainadmin and mainuser respectively. (or you can create your own user - from the GUI and admin - from the database)

To run the code on Raspberry Pi:
1. Make sure OpenCV and tensorflow are installed correctly and the hardware is connected properly.