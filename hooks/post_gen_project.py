import subprocess
import sys

def run_command(command):
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e.cmd}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        return False
    except FileNotFoundError:
        print(f"Command not found: {command[0]}")
        return False

def main():
    print("Running post-generation setup...")
    
    # Run uv sync
    print("Synchronizing project with uv...")
    if run_command(["uv", "sync"]):
        print("Project successfully synchronized with uv.")
    else:
        print("Failed to run 'uv sync'. Please make sure 'uv' is installed and run it manually.")

if __name__ == "__main__":
    main()
