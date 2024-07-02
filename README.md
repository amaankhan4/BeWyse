# User Authentication & Profile Management System

A secure and efficient web application for user registration, login, and profile management, utilizing Django, MongoDB, and Firebase.

## Technologies Used

- **Backend**: Python, Django
- **Database**: MongoDB
- **Authentication**: Firebase, JWT
- **API**: RESTful API

## Project Overview

The User Authentication & Profile Management System is designed to provide a robust solution for managing user accounts. This includes functionalities for user registration, login, and profile management, with a focus on security and efficiency.

### Key Features

- **User Registration**: Secure user registration with email verification.
- **User Login**: Secure login with email and password.
- **Profile Management**: Users can update their profiles, including personal information and preferences.
- **Data Storage**: Integrates MongoDB for efficient and scalable data storage.
- **Authentication Services**: Utilizes Firebase for secure user authentication.
- **RESTful API Endpoints**: Enhances front-end and back-end communication, ensuring a secure and smooth user experience.

## Performance Improvements

- **User Onboarding Speed**: Achieved a 40% increase in user onboarding speed.
- **Data Retrieval Efficiency**: Improved data retrieval efficiency by 25%, making the application faster and more responsive.

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/amaankhan4/BeWyse
    cd BeWyse
    ```

2. **Set Up Virtual Environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Backend Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure Firebase**:
    - Set up a Firebase project and obtain your Firebase configuration credentials.
    - Add your Firebase configuration to your Django settings.

5. **Run Migrations**:
    ```bash
    python manage.py migrate
    ```

## Usage

1. **Start the Server**:
    ```bash
    python manage.py runserver
    ```

2. **Access the Application**:
    Open your browser and go to `http://localhost:8000` to start using the User Authentication & Profile Management System.
