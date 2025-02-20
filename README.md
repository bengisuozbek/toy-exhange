# toy_app

TOY EXCHANGE APPLICATION

* Introduction:
    - By using this application, people can reach more toys more easily by exchange method. Children can choose the toys they want from the application by looking at the toy photos. 
    - Users, whether logged in or not, can access a page displaying all available toys. However, access to other sections of the platform requires users to be logged in. A protection mechanism is in place for admins, registered users, and non-registered users. Admins have the privilege to view sensitive data within the system.
    - Users can send messages to other users regarding a toy or submit a request for it. Messaging is not real-time; users need to refresh the page to see new messages. To improve this, I plan to integrate WebSocket for real-time communication. 
    - When a user decides to proceed with an exchange, they send a request, which the other party must approve to finalize the trade. I am working on a business plan to enhance the flow of accepted requests.
    - Users can see the market prices of the toys they are viewing through web scraping. Information about similar products from sites like Cimri will be displayed in a dedicated section. To ensure data freshness, I plan to schedule a daily automated task to update the information.

* To Login, 
    - Test User: 
        * USERNAME:   test
        * PASSWORD:   Pass1234

* Technology: Python Django
* Python Version: 3.13.2 
* Database: Sqlite

* To build the project:
    - Create a virtual environment:
        * python3 -m venv {Virtual_Env_Name}
    - To activate a virtual environment:
        * source {Virtual_Env_Name}/bin/activate
    - Stop to virtual environment:
        * deactivate
    - To install necessary packages&frameworks:
        * pip install --upgrade pip
        * pip3 install -r requirements.txt
    - Create the SQLite database and apply migrations:
        * python manage.py migrate
    - To run the project:
        * python manage.py runserver

* mysite: 
    - Sign In with Facebook and Google were implemented before. Now, two of them does not work. The connection should be updated.
    - urls.py:
        - It contains most endpoints that are used in the project.
    - static folder:
        - Two folders that are called css, and images are included. 
        - images folder contains csv files that were taken from related price websites (ex. Cimri)
     
* Catalog:
    - catalog/models.py:
        - Tables were creted using the Code First approach. 
        - The auth_user and auth_group tables are built-in tables in Django. All other tables have been added for the design of the project. 
    - catalog/views.py:
        - Contains main HTTP REQUEST mechanism of the page.
        - Login, Registration, All products, Support... are handled on the page. 
        - It is said that the structure is monolith. To improve the project, a service layer, data layer should be applied firstly. 
        - Earlier, Forgot Password mail was sent from "toy.exchange.application@gmail.com", after the Gmail procedure changed. New mail server can be added to send emails.
    - catalog/decorators:
        - Pages are secured. 
        - Users role is examined to open related pages. 

* Price:
    - price/models.py:
        - To create related database tables.
    - Web Scraping used for getting prices for the products. The main aim is to show people that how much is the current price of the toy.
    - The prices are getting from Cimri, then it is saved as CSV file. 
    - Next step is showing the users the current toys price and also, related toys.

* Messages: 
    - No other platforms used. 
    - Messages are kept in database. Unwanted situation. Its process should be changed as WebSocket. The connection between users are synchronized and can be get messages for the current time.
    - Messages can be found by searching with its recever_id or sender_id.
    - The communication is not synchronized. WebSocket can be used. 

* Templates:
    - All the front-end related pages included in the folder.
    - HTML, CSS, and JavaScript were used to create the visual side of the website.
    - Bootstrap and Bulma have been used for design.
    - Comman files used to make code easier and organized. Almost all HTML files use base.html as a template and it contains navbar.html for the navigation menu and footer.html for the footer.