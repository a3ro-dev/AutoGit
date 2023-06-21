import platform
import subprocess
import os
import psutil
import datetime
import socket
import time


def print_system_info():
    # Print OS information
    os_name = platform.system()
    os_release = platform.release()
    print(f"🖥️  Operating System: {os_name} {os_release}")

    # Print system architecture
    system_architecture = platform.machine()
    print(f"💻  System Architecture: {system_architecture}")

    # Print number of CPU cores
    cpu_cores = psutil.cpu_count(logical=False)
    print(f"🔢  CPU Cores: {cpu_cores}")

    # Print CPU frequency
    cpu_frequency = psutil.cpu_freq().current
    print(f"⏱️  CPU Frequency: {cpu_frequency} MHz")

    # Print GPU information (if available)
    try:
        gpu_name = subprocess.check_output(["lshw", "-C", "display"], encoding="utf-8")
        gpu_name = gpu_name[gpu_name.find("product:") + 9 : gpu_name.find("vendor:")].strip()
        print(f"🎮  GPU: {gpu_name}")
    except Exception as e:
        pass

    # Print username
    username = os.getlogin()
    print(f"👤  Username: {username}")

    # Print available disk space
    disk_usage = psutil.disk_usage("/")
    total_disk_space = disk_usage.total / (1024 ** 3)
    available_disk_space = disk_usage.free / (1024 ** 3)
    print(f"💾  Disk Space: {available_disk_space:.2f} GB / {total_disk_space:.2f} GB")

    # Print network interfaces and IP addresses
    network_interfaces = psutil.net_if_addrs()
    for interface, addresses in network_interfaces.items():
        ip_addresses = [addr.address for addr in addresses if addr.family == socket.AF_INET]
        if ip_addresses:
            ip_addresses_str = ", ".join(ip_addresses)
            print(f"🌐  Network Interface {interface}: {ip_addresses_str}")

    # Print system hostname
    hostname = socket.gethostname()
    print(f"🏠  Hostname: {hostname}")

    # Print system uptime
    uptime = int(time.time() - psutil.boot_time())
    uptime_str = datetime.timedelta(seconds=uptime)
    print(f"⏲️   Uptime: {uptime_str}")

    # Print Git version
    git_version_output = subprocess.run(["git", "--version"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    git_version = git_version_output.stdout.strip()
    print(f"🐙  Git version: {git_version}")

    # Print Python version
    python_version = platform.python_version()
    print(f"🐍  Python version: {python_version}")

    # Print Node.js version (if installed)
    try:
        node_version_output = subprocess.run(["node", "--version"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        node_version = node_version_output.stdout.strip()
        print(f"🟢  Node.js version: {node_version}")
    except FileNotFoundError:
        pass

    # Print Java version (if installed)
    try:
        java_version_output = subprocess.run(["java", "-version"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        java_version = java_version_output.stdout.strip().split("\n")[0]
        print(f"☕  Java version: {java_version}")
    except FileNotFoundError:
        pass

    # Print version information for five other programming languages (if installed)
    languages = {
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
        try:
            version_output = subprocess.run([language, "--version"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            version = version_output.stdout.strip().split("\n")[0]
            print(f"{emoji}  {language.capitalize()} version: {version}")
        except FileNotFoundError:
            pass

    # Print current working directory and terminal type
    cwd = os.getcwd()
    terminal_type = os.environ.get("TERM_PROGRAM", "Unknown")
    print(f"📂  Current working directory: {cwd}")
    print(f"🖥️  Terminal type: {terminal_type}")
