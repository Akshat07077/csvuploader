# CSV File Management System

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Technology Stack](#technology-stack)
4. [Installation](#installation)
5. [Usage](#usage)
6. [API Endpoints](#api-endpoints)
7. [Models](#models)
8. [Forms](#forms)
9. [Serializers](#serializers)
10. [Running Tests](#running-tests)
11. [Contributing](#contributing)
12. [License](#license)
13. [Acknowledgements](#acknowledgements)

## Introduction

The CSV File Management System is a web application built with Django that allows users to upload, view, edit, and delete CSV files. Users can also add new rows and columns to the CSV files and export the edited files.

## Features

- User authentication (signup and login)
- Upload CSV files
- View CSV file contents
- Edit rows and columns in CSV files
- Add new rows and columns to CSV files
- Export edited CSV files
- Delete CSV files
- Responsive design with Bootstrap

## Technology Stack

- Python
- Django
- Bootstrap
- HTML
- CSS
- JavaScript
- SQLite (default, can be replaced with PostgreSQL, MySQL, etc.)
- Django REST Framework (for API endpoints)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Akshat/csvuploader.git
   cd csvuploader
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

4. Install the required dependencies:

   ```bash
   pip install -r r.txt
   ```

5. Run database migrations:

   ```bash
   python manage.py migrate
   ```

6. Create a superuser:

   ```bash
   python manage.py createsuperuser
   ```

7. Start the development server:

   ```bash
   python manage.py runserver
   ```

8. Open your browser and navigate to `http://127.0.0.1:8000`.

## Usage

### User Authentication

- Navigate to the signup page to create a new account.
- Login using the credentials.

### Uploading CSV Files

- After logging in, navigate to the upload page.
- Choose a CSV file to upload and submit the form.

### Viewing and Editing CSV Files

- Go to the file list page to see all uploaded CSV files.
- Click on a file to view its contents.
- Edit rows and columns as needed.
- Add new rows or columns using the provided form.
- Export the edited CSV file.

### Deleting CSV Files

- Click the delete button on the file list or view page to delete a CSV file.

## API Endpoints

### User Authentication

- **Signup:** `POST /api/signup/`
- **Login:** `POST /api/login/`

### CSV File Management

- **Upload CSV:** `POST /api/csv/upload/`
- **List CSV Files:** `GET /api/csv/`
- **View CSV File:** `GET /api/csv/<file_id>/`
- **Delete CSV File:** `DELETE /api/csv/<file_id>/`

## Models

### CSVfiles

- `user`: ForeignKey to the User model.
- `file`: FileField to store the CSV file.
- `uploaded_at`: DateTimeField to store the upload timestamp.

### CSVData

- `file`: ForeignKey to the CSVfiles model.
- `row_number`: IntegerField to store the row number.
- `data`: JSONField to store the row data.

## Forms

- `UserCreationForm`: Django's built-in user creation form.
- `CSVForm`: Form for uploading CSV files.
- `CSVUpdateForm`: Form for updating CSV file contents.


## Running Tests

To run the tests, use the following command:

```bash
python manage.py test
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgements

- Django: [https://www.djangoproject.com/](https://www.djangoproject.com/)
- Bootstrap: [https://getbootstrap.com/](https://getbootstrap.com/)
- Django REST Framework: [https://www.django-rest-framework.org/](https://www.django-rest-framework.org/)
```
