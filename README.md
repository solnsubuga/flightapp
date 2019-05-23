# Flight application API

An application that allows users to book flights and pay for the tickets.

## Dependancies

- [python 3.6](https://www.python.org/downloads/release/python-360/)
- [django](https://www.djangoproject.com/)
- [django rest framework](https://www.django-rest-framework.org/)

## Set Up

In order to run the API Application

1.  Clone this repository and create a virtual environment in a terminal shell `virtualenv env` and Install the dependencies `pip install -r requirements.txt` You could as well use `pipenv`. Install [pipenv](https://docs.pipenv.org/en/latest/) and run `pipenv install` to install the requirements

2.  Make a copy of `.env-example`, rename it to `.env` and replace the details below

    ```
        DB_NAME=your-database-name
        DB_USER=your-database-user
        DB_PASSWORD=your-password
        DB_PORT=5432
        DEBUG=True
        ALLOWED_HOSTS=.localhost

    ```

3.  Run the migrations using the dev settings file: `./manage.py migrate`

4.  Run the command `source .env` and then run the application by running commands `./manage.py runserver`

## API End points

| EndPoint                              | Method | Description             |
| ------------------------------------- | ------ | ----------------------- |
| `/auth/signup`                        | POST   | Register a user         |
| `/auth/signin`                        | POST   | Login a user            |
| `/api/v1/flights/`                    | GET    | Get flights             |
| `/api/v1/flight/<flight_id>/`         | GET    | Get a specific flight   |
| `/api/v1/flight/<flight_id>/book/`    | POST   | Book a flight           |
| `/api/v1/flight/<flight_id>/payment/` | POST   | Pay for a flight ticket |

## License

The project is licensed under Apache License.
