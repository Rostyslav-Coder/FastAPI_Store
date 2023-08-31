# FastAPI_Store

## Online Shop Project
### This is a project of an online shop that sells various products such as books, electronics, clothing, and more. The project is built with Python, FastAPI, SQLite, Celery, and Redis. The project has the following features:

### RESTful API that provides endpoints for CRUD operations on products, orders, users, and other entities.
### SQLite database that stores the data of the online shop.
### Celery task queue that handles asynchronous tasks such as sending emails, processing payments, and generating reports.
### Redis cache that improves the performance and scalability of the online shop.
### Swagger UI that documents and tests the API.
### The project is still in development and will be updated with more features and improvements. The project is open source and anyone can contribute to it. The project is hosted on GitHub and can be accessed from [this link].

## How to run the project
### To run the project locally, you need to have Python 3.9 or higher installed on your computer. You also need to have Git installed on your computer. Follow these steps to run the project:

### Clone the project repository from GitHub using this command: git clone https://github.com/online-shop-project/online-shop.git
### Create a virtual environment for the project using this command: pipenv lock
### Activate the virtual environment using this command: pipenv sync
### Start the Celery worker using this command: celery -A app.celery worker --loglevel=info
### Start the Redis server using this command: redis-server
### Start the FastAPI server using this command: uvicorn app.main:app --reload
### Open your web browser and enter the URL of your local server followed by /docs. For example: http://localhost:8000/docs
### Enjoy browsing and testing the API!

## License and credit
### The project is licensed under the MIT License. You can find the license file in the LICENSE folder of the project. The project uses some third-party resources such as images, icons, fonts, and libraries. You can find the credit and license of these resources in the CREDITS folder of the project.