# Asset Tracker

Welcome to the Asset Tracker Project.

## Project Description

1. Manage assets and assets types.
2. Manage assets status
3. System Admin can login logout and manage assets.

## Requirement

1. Python >= 3.10
2. Mysql >= 8.0

## Installation

To run this project locally, follow these steps:

1. Clone the repository: `git clone [repository URL]` or extract the .zip folder
2. Navigate to the project directory: `cd asset_tracker`
3. cp .env.example .env
MY_VARIABLE=my_value
ANOTHER_VARIABLE=another_value
5. Run and activate python virtual environment according to the os.
6. Install the project dependencies: `pip install -r requriements/development.txt`
7. Apply database migrations: `python manage.py migrate`
8. Start the development server: `python manage.py runserver`


## Installation with docker

To run this project locally in docker using docker-compose, follow these steps:

1. Create file .django and .mysql file under directory ./envs/.local/
2. Set the environment variable 
    .django: 
        - DOMAIN
        - SECRET_KEY
        - DEBUG=True
        - DATABASE_URL
    
    .mysql:
        - MYSQL_DATABASE
        - MYSQL_USER
        - MYSQL_PASSWORD
        - MYSQL_ROOT_PASSWORD
        - MYSQL_HOST
        - MYSQL_PORT
3. Run `sudo make build`
Note: make sure ports used in local.yml should not conflict with local system ports.


## Usage

To use this project, follow these steps:

1. Access the application in your web browser at `http://localhost:8000`

## Contributing

We welcome contributions to this project! If you would like to contribute, please follow these guidelines:

1. Fork the repository
2. Create a new branch: `git checkout -b [branch name]`
3. Make your changes and commit them: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin [branch name]`
5. Submit a pull request

## License

N/A

## Contact

If you have any questions or suggestions, feel free to contact us at [Ravi Kant Gautam](mailto:ravi.gautam@neosoftmail.com)
