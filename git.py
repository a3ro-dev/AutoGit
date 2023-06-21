import os
import platform
import subprocess
import sys
import openai
import keys

openai.api_key = keys.api

class Git:
    def __init__(self, email):
        self.email = email
        
    def install_git(self):
        # Check if Git is installed
        try:
            subprocess.run(["git", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except FileNotFoundError as e:
            print(f"{e}\n")
            print("Git is not installed. Installing Git...")
            # Install Git based on the operating system
            if os.name == "nt":  # Windows
                subprocess.run(["winget", "install", "--id", "Git.Git", "-e", "--source", "winget"])
            if sys.platform.startswith("linux") or sys.platform.startswith("darwin"):  # Linux and macOS
                # Check the specific Linux distribution or macOS package manager
                if sys.platform.startswith("linux"):
                    distro = self.get_linux_distribution().lower()
                else:
                    distro = platform.mac_ver()[0].lower()
                # Install Git based on the Linux distribution or macOS package manager
                if distro in ["debian", "ubuntu"]:
                    subprocess.run(["sudo", "apt-get", "install", "-y", "git"])
                elif distro == "fedora":
                    subprocess.run(["sudo", "dnf", "install", "-y", "git"])
                elif distro == "gentoo":
                    subprocess.run(["sudo", "emerge", "--ask", "--verbose", "dev-vcs/git"])
                elif distro == "arch":
                    subprocess.run(["sudo", "pacman", "-S", "git"])
                elif distro == "opensuse":
                    subprocess.run(["sudo", "zypper", "install", "git"])
                elif distro == "mageia":
                    subprocess.run(["sudo", "urpmi", "git"])
                elif distro == "nixos":
                    subprocess.run(["nix-env", "-i", "git"])
                elif distro == "freebsd":
                    subprocess.run(["sudo", "pkg", "install", "git"])
                elif distro == "openbsd":
                    subprocess.run(["sudo", "pkg_add", "git"])
                elif distro == "alpine":
                    subprocess.run(["sudo", "apk", "add", "git"])
                elif distro == "darwin":
                    if subprocess.run(["which", "brew"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0:
                        subprocess.run(["brew", "install", "git"])
                    elif subprocess.run(["which", "port"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0:
                        subprocess.run(["sudo", "port", "install", "git"])
                    else:
                        print("Homebrew or MacPorts not found. Please install Git manually.")
                        return 
                else:
                    print("Unsupported Linux distribution or macOS version. Please install Git manually.")
                    return
            else:
                print("Unsupported operating system. Please install Git manually.")
                return
            
    def get_linux_distribution(self):
        try:
            with open("/etc/os-release", "r") as f:
                lines = f.readlines()
                for line in lines:
                    if line.startswith("ID="):
                        return line.split("=")[1].strip().lower()
        except FileNotFoundError as e:
            print(e)
            

        return ""
    
    def generate_ssh_key(self):
        # Generate SSH key pair
        home_dir = os.path.expanduser("~")
        ssh_dir = os.path.join(home_dir, ".ssh")
        key_file = os.path.join(ssh_dir, "id_rsa.pub")
        print("Contents of .ssh directory:")
        for file_name in os.listdir(ssh_dir):
            print(f">-+-< {file_name} >-+-<")
        subprocess.run(["ssh-keygen", "-t", "rsa", "-b", "4096", "-C", self.email])

        # Print SSH key 
        with open(key_file, "r") as f:
            ssh_key = f.read()
        print("SSH key:")
        print(ssh_key)

    
        # Print documentation on how to connect to GitHub
        print("Documentation:")
        print("1. Copy the SSH key above.")
        print("2. Go to your GitHub account settings.")
        print("3. Click on 'SSH and GPG keys'.")
        print("4. Click on 'New SSH key' or 'Add SSH key'.")
        print("5. Paste the copied SSH key into the 'Key' field.")
        print("6. Provide a suitable title for the key.")
        print("7. Click 'Add SSH key' or 'Add key'.")
        confirmation: str = str(input("Are you done with these steps?: [y/n]"))
        if confirmation == "y":
            # Check if an existing SSH connection to GitHub exists
            github_host = "github.com"
            ssh_config_file = os.path.join(ssh_dir, "config")
            with open(ssh_config_file, "r") as f:
                ssh_config = f.read()
            if github_host in ssh_config:
                print("Existing SSH connection to GitHub:")
                print(ssh_config)
            subprocess.run(["ssh", "-T", "git@github.com"])
    
        else:
            issue: str = str(input("What is the issue that you are you facing?: "))
            response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are a github expert and a DevOps enthusiast, your name is AutoGit and you help people setup git and github."},
                {"role": "user", "content": issue}
            ],
        )

        assistant_reply = response.choices[0].message.content.strip() #type: ignore
        print(assistant_reply)
        confirmation: str = str(input("Is Your Issue Solved? [y/n]: ")) 
        if confirmation == "y":
            # Check if an existing SSH connection to GitHub exists
            github_host = "github.com"
            ssh_config_file = os.path.join(ssh_dir, "config")
            with open(ssh_config_file, "r") as f:
                ssh_config = f.read()
            if github_host in ssh_config:
                print("Existing SSH connection to GitHub:")
                print(ssh_config)
            subprocess.run(["ssh", "-T", "git@github.com"])
        else:
            print("Issue Still Not Solved? Search for the issue on Google.")
            sys.exit()

if __name__ == "__main__":
    # Example usage
    email = input("Enter Your Email: ")
    git = Git(email=email)
    git.install_git()
    git.generate_ssh_key()
