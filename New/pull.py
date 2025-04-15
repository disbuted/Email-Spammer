# Make sure you've got git installed on your system for this :)
# https://git-scm.com/downloads
# https://desktop.github.com/download/

import subprocess

def run_command(command):
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True, shell=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        exit(1)

def main():
    print("Automate pulling changes from a forked repository into your main repository.")
    
    repo_path = input("Enter the path to your main repository (e.g., /path/to/your/main-repo): ").strip()
    fork_username = input("Enter the GitHub username of the fork's owner: ").strip()
    fork_repo_name = input("Enter the name of the fork repository: ").strip()

    print(f"Navigating to {repo_path}...")
    run_command(f"cd {repo_path}")
    
    fork_remote_url = f"https://github.com/{fork_username}/{fork_repo_name}.git"
    print(f"Adding the fork as a remote: {fork_remote_url}")
    run_command(f"git remote add fork {fork_remote_url}")
    
    print("Verifying remotes...")
    run_command("git remote -v")
    
    print("Fetching changes from the fork...")
    run_command("git fetch fork")
    
    print("Switching To Main")
    run_command("git checkout main")
    print("Merging From Form Branch/Main")
    run_command("git merge fork/main")
    
    print("Pushing Changes")
    run_command("git push origin main")
    
    print("Merged Succesfully And Pushed")

if __name__ == "__main__":
    main()