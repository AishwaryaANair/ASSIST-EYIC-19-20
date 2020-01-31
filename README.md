ASSIST Project for E-Yantra Ideas Competition 2019-20

Consists of the Application and Doucmentation

Dependencies: 
1. XAMPP with sendmail
2. Python 3
3. OpenCV
4. TensorFlow

To install the application:

1. Paste this folder in the xampp htdocs folder. Import the assist.sql file into your phpmyadmin database.
2. Replace the username and password in the connection.php files in the parent and admin directory as required.
3. Use the email Ids of assistadmin@gmail.com and assistuser@gmail.com to log in to admin and user panels with the passwords mainadmin and mainuser respectively. (or you can create your own user - from the GUI and admin - from the database)

To run the code on Raspberry Pi:
1. Make sure OpenCV and tensorflow are installed correctly and the hardware is connected properly.
2. Run python finalASSIST.py in the respective directory.