import platform
import subprocess
import os
import psutil
import datetime
import socket
import time
import threading

def print_system_info():
    """
     Prints information about the system.
    """
    # Printing of OS information
    os_name = platform.system()
    os_release = platform.release()
    print(f"🖥️  Operating System: {os_name} {os_release}")

    # Printing system architecture
    system_architecture = platform.machine()
    print(f"💻  System Architecture: {system_architecture}")

    # Print number of CPU cores
    cpu_cores = psutil.cpu_count(logical=False)
    print(f"🔢  CPU Cores: {cpu_cores}")

    # Print CPU frequency
    cpu_frequency = psutil.cpu_freq().current
    print(f"⏱️  CPU Frequency: {cpu_frequency} MHz")

    # Thread function to get GPU information
    def get_gpu_info():
        try:
            gpu_name = subprocess.check_output(["lshw", "-C", "display"], encoding="utf-8")
            gpu_name = gpu_name[gpu_name.find("product:") + 9: gpu_name.find("vendor:")].strip()
            print(f"🎮  GPU: {gpu_name}")
        except Exception as e:
            pass

    # Print the username
    username = os.getlogin()
    print(f"👤  Username: {username}")

    # Print the available disk space
    disk_usage = psutil.disk_usage("/")
    total_disk_space = disk_usage.total / (1024 ** 3)
    available_disk_space = disk_usage.free / (1024 ** 3)
    print(f"💾  Disk Space: {available_disk_space:.2f} GB / {total_disk_space:.2f} GB")

    # Print network interfaces and IP addresses
    def print_network_info():
        network_interfaces = psutil.net_if_addrs()
        for interface, addresses in network_interfaces.items():
            ip_addresses = [addr.address for addr in addresses if addr.family == socket.AF_INET]
            if ip_addresses:
                ip_addresses_str = ", ".join(ip_addresses)
                print(f"🌐  Network Interface {interface}: {ip_addresses_str}")

    # Thread function to print network information
    network_thread = threading.Thread(target=print_network_info)

    # Print system hostname
    hostname = socket.gethostname()
    print(f"🏠  Hostname: {hostname}")

    # Printing system uptime
    uptime = int(time.time() - psutil.boot_time())
    uptime_str = datetime.timedelta(seconds=uptime)
    print(f"⏲️   Uptime: {uptime_str}")

    # Printed Git version
    git_version_output = subprocess.run(["git", "--version"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    git_version = git_version_output.stdout.strip()
    print(f"🐙  Git version: {git_version}")

    # Printed Python version
    python_version = platform.python_version()
    print(f"🐍  Python version: {python_version}")

    # Thread function to print Node.js version (if installed)
    def print_node_version():
        try:
            node_version_output = subprocess.run(["node", "--version"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            node_version = node_version_output.stdout.strip()
            print(f"🟢  Node.js version: {node_version}")
        except FileNotFoundError:
            pass

    # Thread to print Node.js version
    node_thread = threading.Thread(target=print_node_version)

    # Thread function to print version information for other programming languages
    def print_language_version(language, emoji):
        try:
            version_output = subprocess.run([language, "--version"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            version = version_output.stdout.strip().split("\n")[0]
            print(f"{emoji}  {language.capitalize()} version: {version}")
        except FileNotFoundError:
            pass

    # Threads for printing version information of programming languages
    language_threads = []
    languages = {
        "java": "☕",
        "groovy": "🎵",
        "dotnet": "🔨",
        "php": "🐘",
        "perl": "🐪",
        "rustc": "🦀",
        "swift": "🍎",
        "kotlin": "🏔️",
        "scala": "🚀",
        "php": "🐘"
    }

    for language, emoji in languages.items():
        language_thread = threading.Thread(target=print_language_version, args=(language, emoji))
        language_threads.append(language_thread)

    # Start all the threads
    network_thread.start()
    node_thread.start()
    for language_thread in language_threads:
        language_thread.start()

    # Wait for all the threads to finish
    network_thread.join()
    node_thread.join()
    for language_thread in language_threads:
        language_thread.join()

    # Print current working directory and terminal type
    cwd = os.getcwd()
    terminal_type = os.environ.get("TERM_PROGRAM", "Unknown")
    print(f"📂  Current working directory: {cwd}")
    print(f"🖥️  Terminal type: {terminal_type}")
