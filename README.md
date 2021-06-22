PIX4D-CHALLENGE
---------

A django REST API.

_______________

## Installation

Requires Python 3.9.

Clone this Git repository, then move to the directory and run the following command:

To set up a virtual environment:

    python -m venv .venv
    source .venv/bin/activate 

To run the project:

    pip install -r requirements.txt
    python manage.py migrate
    python manage.py runserver 8080

To run the Docker container:

    docker build -t pix4d .
    docker run -it -p 8000:8000 pix4d

_______________


## License

This repository uses the [MIT License](/LICENSE).
