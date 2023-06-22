from utils.git import GitSSH 
from utils.generation import ReadmeGen 
from utils.sysinfo import print_system_info
import subprocess
import os 
import time
import fnmatch


class AutoGit:
    """
    Automation Of Git, Implemented Using `subprocess`
    """
    @staticmethod
    def createRepo():
        """
         Creates a new git repository.
        """
        # Check if the repo already exists
        try:
            repo_path: str = str(input("Enter the repo path: "))
            # Create a new repository if it doesn t exist.
            if not subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], cwd=repo_path, stdout=subprocess.PIPE).stdout.decode().strip() == "true":
                # Create a new repo
                subprocess.run(["git", "init"], cwd=repo_path)
                print(f"Created Git repository at {repo_path}")

            # Create a .gitignore file if it doesn't exist
            gitignore_path = os.path.join(repo_path, ".gitignore")
            # Generate the. gitignore file and commit the changes to the repository
            if not os.path.exists(gitignore_path):
                # Generate the .gitignore contents
                with open(".gitignore", "w") as gitignore_contents: #type: ignore
                # Print the contents of the default .gitignore file
                    print("Default .gitignore contents:")
                    print(gitignore_contents.read()) #type: ignore

                # Ask the user to customize the .gitignore file
                print("Please enter the names of additional files to ignore (or 'none' or '0' to skip):")
                # input file name and return gitignore contents
                while True:
                    file_name = input("> ")
                    # If file_name is none 0 or none 0
                    if file_name.lower() in ["none", "0"]:
                        break
                    gitignore_contents: str = gitignore_contents + f"\n{file_name}"
            
                # Convert gitignore_contents to a string
                gitignore_contents_str = str(gitignore_contents)

                # Write the modified .gitignore file
                with open(gitignore_path, "w") as f: 
                    f.write(gitignore_contents_str) 

                # Add .gitignore to the repository
                subprocess.run(["git", "add", gitignore_path], cwd=repo_path)

                # Commit the changes to the repository
                subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=repo_path)

                print(f"Updated .gitignore file at {gitignore_path}")
        except Exception as e:
            print(e)

    @staticmethod
    def read_repo_contents(repo_dir: str):
        """
         Reads the contents of a git repository and returns it as a string.
         
         @param repo_dir - The path to the repository. Must be a directory.
         
         @return The contents of the repository or None if there was an error
        """
        try:
            gitignore_path = os.path.join(repo_dir, ".gitignore")
            ignored_patterns = []

            # Returns a list of ignored patterns.
            if os.path.isfile(gitignore_path):
                with open(gitignore_path, "r") as f:
                    lines = f.readlines()
                    ignored_patterns = [line.strip() for line in lines if line.strip() and not line.strip().startswith("#")]

            output = ""
            # Return a string containing the contents of the repo_dir.
            for root, dirs, files in os.walk(repo_dir):
                # Remove ignored directories
                dirs[:] = [d for d in dirs if not any(fnmatch.fnmatch(d, pattern) for pattern in ignored_patterns)]

                # Output the output of the files.
                for file in files:
                    file_path = os.path.join(root, file)
                    # Return true if file matches any of the ignored patterns.
                    if any(fnmatch.fnmatch(file, pattern) for pattern in ignored_patterns):
                        continue

                    with open(file_path, "r") as f:
                        file_content = f.read()

                    output += f"\n{file_path}\n{file_content}\n"

            return output
        except Exception as e:
            print(e)
    
    @staticmethod
    def push_repository():
        """
         Push repository to remote and verify it's remote URL Args : repo_path ( str ) : Path to the
        """
        try: 
            # Set the current working directory
            repo_path: str = str(input("Enter the repo path: "))
            os.chdir(repo_path)

            # Ask for branch name
            branch_name = input("Enter the branch name: ")

            # Ask for remote URL
            remote_url = input("Enter the remote URL: ")

            try:
                # Add the remote URL
                subprocess.run(["git", "remote", "add", "origin", remote_url])

                # Verify the new remote URL
                subprocess.run(["git", "remote", "-v"])

                # Push the changes to the remote branch
                subprocess.run(["git", "push", "origin", branch_name])

                print("Repository successfully pushed.")
            except subprocess.CalledProcessError as e:
                print(f"Error: Failed to push the repository. {e}")
        except Exception as e:
            print(e)
            

print("Welcome to AutoGit")
print_system_info()
time.sleep(1)
def print_menu():
    print("===== AUTOGIT MENU =====")
    print("1. Setup GIT and GITSSH")
    print("2. Generate README.md for a file")
    print("3. Generate README.md for a repository")
    print("4. Create a Git repository")
    print("5. Create a Git repository, generate README.md, and push to remote repository")
    print("0. Exit")
    print("================")

# Usage
print_menu()
user_choice = input("Enter your choice: ")

# Handle user choice
if user_choice == "2":
    file_name: str  = input("Enter the name of the file: ")
    readme_contents: str = str(ReadmeGen.generate_readme(file_name))
    # Write the README.md file
    with open("README.md", "w") as f:
        f.write(readme_contents)

elif user_choice == "3":
    repo: str = input("Enter the repository directory: ")
    repo_content: str = str(AutoGit.read_repo_contents(repo))
    readme_contents: str = str(ReadmeGen.generate_readme(repo_content))
    # Write the README.md file
    with open("README.md", "w") as f:
        f.write(readme_contents)

elif user_choice == "4":
    AutoGit.createRepo()
    
elif user_choice == "5":
    print("Initializing createRepo functionality")
    AutoGit.createRepo()
    time.sleep(5)
    print("Initializing readmeGen participants")
    repo = ""
    repo_content: str = str(AutoGit.read_repo_contents(repo))
    readme_contents: str = str(ReadmeGen.generate_readme(repo_content))
    # Write the README.md file
    with open("README.md", "w") as f:
        f.write(readme_contents)
    time.sleep(5)
    AutoGit.push_repository()

elif user_choice == "1":
    email = input("Enter Your Email: ")
    git = GitSSH(email=email)
    git.install_git()
    git.generate_ssh_key()

elif user_choice == "0":
    print("Exiting...")
else:
    print("Invalid choice")