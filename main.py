import utils.git as git
import utils.generation as readmegen
import utils.sysinfo as sysinfo
import subprocess
import os 


class AutoGit:
    def createRepo(self, repo_path):
        # Check if the repo already exists
        repo_path: str = str(input("Enter the repo path: "))
        if not subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], cwd=repo_path, stdout=subprocess.PIPE).stdout.decode().strip() == "true":
            # Create a new repo
            subprocess.run(["git", "init"], cwd=repo_path)
            print(f"Created Git repository at {repo_path}")

        # Create a .gitignore file if it doesn't exist
        gitignore_path = os.path.join(repo_path, ".gitignore")
        if not os.path.exists(gitignore_path):
            # Generate the .gitignore contents
            with open(".gitignore", w) as gitignore_contents:
            # Print the contents of the default .gitignore file
                print("Default .gitignore contents:")
                print(gitignore_contents.read())

            # Ask the user to customize the .gitignore file
            print("Please enter the names of additional files to ignore (or 'none' or '0' to skip):")
            while True:
                file_name = input("> ")
                if file_name.lower() in ["none", "0"]:
                    break
                gitignore_contents += f"\n{file_name}"

            # Write the modified .gitignore file
            with open(gitignore_path, "w") as f:
                f.write(gitignore_contents)

            # Add .gitignore to the repository
            subprocess.run(["git", "add", gitignore_path], cwd=repo_path)

            # Commit the changes to the repository
            subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=repo_path)

            print(f"Updated .gitignore file at {gitignore_path}")

        print("AutoGit initialized")




print("Welcome to AutoGit 🙏")
sysinfo.print_system_info()
    
