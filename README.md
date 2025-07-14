# Community Forum

This is a community forum application built with Django. It allows users to register, create topics, and participate in discussions.

## Features

*   **User Authentication:** Users can register, log in, and log out. It also supports social authentication with Google.
*   **Categories and Forums:** The forum is organized into categories and forums.
*   **Threads and Comments:** Users can create threads within forums and comment on them.
*   **Rich Text Editor:** The application uses CKEditor 5 for a rich text editing experience when creating threads and comments.
*   **User Profiles:** Each user has a profile page.

## Technologies Used

*   **Backend:** Django
*   **Frontend:** HTML, CSS, JavaScript
*   **Database:** SQLite (default)
*   **Authentication:** django-allauth
*   **Rich Text Editor:** django-ckeditor-5

## Getting Started

### Prerequisites

*   Python 3.x
*   Pip

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/community-forum.git
    ```

2.  **Navigate to the `application` directory:**

    ```bash
    cd community-forum/application
    ```

3.  **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Create a `.env` file and add the following environment variables:**

    ```
    CLIENT_ID=<your-google-client-id>
    SECRET=<your-google-secret>
    ```

5.  **Run the database migrations:**

    ```bash
    python manage.py migrate
    ```

6.  **Run the development server:**

    ```bash
    python manage.py runserver
    ```

The application will be available at `http://127.0.0.1:8000`.

## Application Structure

*   **`application/`:** The main Django project directory.
    *   **`application/`:** The project's settings and configuration.
    *   **`forum/`:** The core forum application, including models, views, and templates for categories, forums, threads, and comments.
    *   **`users/`:** The user management application, including a custom user model and views.
    *   **`templates/`:** The application's templates.
    *   **`static/`:** The application's static files (CSS, JavaScript, images).
*   **`manage.py`:** The Django management script.
*   **`requirements.txt`:** The project's dependencies.
*   **`db.sqlite3`:** The SQLite database file.

## Contributing

Contributions are welcome! Please feel free to open an issue or submit a pull request.
