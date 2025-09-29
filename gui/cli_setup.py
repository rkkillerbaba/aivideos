import subprocess
import sys
import os
import importlib.util

def run_command(cmd):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result.returncode

def clone_roop():
    run_command("git clone https://github.com/FurkanGozukara/rop_fixed roop")

def clone_basicsr():
    run_command("cd roop && git clone https://github.com/FurkanGozukara/BasicSR")

def install_requirements():
    run_command("cd roop && pip install -r a.txt")

def uninstall_basicsr():
    run_command("pip uninstall basicsr --yes")

def install_basicsr_editable():
    run_command("cd roop/BasicSR && pip install -e .")

def patch_opennsfw2():
    module_name = "opennsfw2._inference"
    try:
        spec = importlib.util.find_spec(module_name)
        if spec is None or spec.origin is None:
            print(f"Could not find the module '{module_name}'. Is opennsfw2 installed?")
        else:
            file_path = spec.origin
            print(f"Found file to patch at: {file_path}")
            with open(file_path, 'r') as f:
                lines = f.readlines()
            patched = False
            with open(file_path, 'w') as f:
                for line in lines:
                    if "cv2.destroyAllWindows()" in line:
                        f.write("#" + line)
                        patched = True
                        print("Found and patched the problematic line.")
                    else:
                        f.write(line)
            if patched:
                print("Patch applied successfully!")
            else:
                print("Warning: The line 'cv2.destroyAllWindows()' was not found. The file may already be patched or has changed.")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure the 'opennsfw2' library is installed correctly.")

def main():
    clone_roop()
    clone_basicsr()
    install_requirements()
    uninstall_basicsr()
    install_basicsr_editable()
    patch_opennsfw2()

if __name__ == "__main__":
    main()
