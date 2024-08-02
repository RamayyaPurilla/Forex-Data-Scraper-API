Please Kindly read the README file from code block.


Forex Data Scraper and API:
        This project involves scraping historical forex (foreign exchange) data from Yahoo Finance, storing it in a SQLite database, and providing a REST API to query this data. The project includes a data scraper, an API server, and a periodic job to keep the data updated.

Assignment Overview:
    Task-1: Scraping Historical Exchange Data
        Scrape Historical Data:
            The scraper fetches historical exchange rates from Yahoo Finance using a combination of currency codes.
            The data is stored in an SQLite database.
    Task-2: Building a REST API
        API Endpoints:
            POST /api/forex-data: Query historical forex data based on given parameters.
            GET /api/all-data: Retrieve all stored forex data.
        Periodic Data Scraping:
            A script is used to periodically scrape data and keep the database updated.

Setup:
    1. Clone the Repository:
        git clone <repository-url>
        cd <repository-directory>
    2. Install Dependencies:
        pip install -r requirements.txt
    3. Initialize the Database
        python database.py

Usage:
    Starting the API Server:
        To start the Flask API server, run:
            python app.py
    The server will start on http://127.0.0.1:5000. You can access the following endpoints:

        POST /api/forex-data:
        Parameters:
            from: The base currency code (e.g., GBP).
            to: The target currency code (e.g., INR).
            period: The time period for the data (e.g., 1W, 1M, 3M, 6M, 1Y).
            Response: JSON array of forex data including date and rate.

        GET /api/all-data:
            Response: JSON array of all forex records in the database.

Running the Data Scraper:
    To manually trigger data scraping, run: python cron_job.py
        This script will scrape data for predefined currency pairs and periods, then store the data in the database. It includes a small delay between requests to manage rate limits.


Automating Data Scraping:
    To automate the data scraping process, you can set up a CRON job or equivalent scheduler depending on your operating system. Schedule cron_job.py to run periodically to keep your data updated.

File Descriptions:
    app.py: 
        Contains the Flask application with routes for accessing forex data. Handles data queries based on parameters and responds with JSON data.
    cron_job.py: 
        A script that periodically runs the scraper for different currency pairs and periods. Handles errors and includes delays between requests.
    scraper.py:
         Defines functions to scrape data from Yahoo Finance, parse the response, and store the data in the SQLite database.
    database.py: 
        Provides functions to connect to the SQLite database and initialize the schema.
    requirements.txt: 
        Lists required Python packages and their versions.

Contributing:
    Feel free to open issues or submit pull requests for improvements or bug fixes.

