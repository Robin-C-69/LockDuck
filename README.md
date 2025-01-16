# LockDuck

### A simple password manager

Lockduck runs locally using Docker

## Installation

<ins>Prerequisite:</ins> Docker setup on your machine

1. Clone the repository:
    ```sh
    git clone https://github.com/Robin-C-69/lockduck.git
    ```

## Usage

1. Build and run the Docker container:
    ```sh
    cd lockduck
    ./start.sh
    ```
   *<ins>Note:</ins> A docker volume will be created at your default location. Try to delete it and your datas will magically disappear*

2. Once your container is running, you have 3 options:
   - 0: Exit
   - 1: Register a new user
   - 2: Login with an existing user
   
3. Once you access the main menu, you have 8 options:
- `create`: Add a new password
  - `-l` or `--login`: The login associated with the password *(required)*
  - `-p` or `--password`: The password *(required)*
  - `-u` or `--url`: The URL associated with the password *(required)*


- `get`: Get a password
  - `-l` or `--login`: The login associated with the link
      
      OR
      - `a` or `--all`: Get all passwords


- `update`: Update a password
  - `-l` or `--login`: The login associated with the password *(required)*
  - `-nl` or `--new-link`: The new link
  - `-nu` or `--new-username`: The new username
  - `-np` or `--new-password`: The new password

      
- `delete`: Delete a password
  - `-l` or `--login`: The login associated with the password
      
  OR
  - `a` or `--all`: Delete all passwords


- `generate`: Generate a random password
  - `-l` or `--length`: The length of the password *(default 12)*


- `exit` or `quit`: Exit the program


- `logout`: Logout of the current user


- `help`: Display the help menu

## License

This project is not licensed<br>
This project is for educational purposes only<br>
Any use of this project is at your own risk

