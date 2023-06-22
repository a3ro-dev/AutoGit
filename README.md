# AutoGit

AutoGit is a Python script that provides various Git functionalities such as creating a Git repository, generating a README.md file, and pushing to a remote repository.

## Installation

1. Clone the repository
    `git clone https://github.com/a3ro-dev/AutoGit`
2. Run `pip install -r requirements.txt` to install the required packages.
   - openai
   - psutil
3. Put your openai api key in utils/keys.py if you want to access generational participants.
4. Run `python main.py` to start the program.

## Usage

After running `main.py`, AutoGit will display a menu with the following options:

### 1. Setup Git and GitSSH

This option allows you to install Git and configure GitSSH.

### 2. Generate README.md for a file

This option generates a README.md file for a specified file.

### 3. Generate README.md for a repository

This option generates a README.md file for an entire repository.

### 4. Create a Git repository

This option creates a new Git repository.

### 5. Create a Git repository, generate README.md, and push to remote repository

This option combines options 4 and 2/3, creating a new Git repository, generating a README.md file for the repository, and pushing it to a remote repository.

## Utilities

AutoGit uses the following utilities:

- `utils.git`: A package used to install and to configure Git and GitSSH.
- `utils.generation`: A package used to generate the content for the README.md file.
- `utils.sysinfo`: A package used to print the system information.

## License

This project is licensed under the terms of the MIT license. See the [LICENSE](LICENSE) file for more information.