import streamlit as st
import subprocess
import importlib.util

st.title("AI Tools Web GUI")

if st.button("Clone roop repo"):
    result = subprocess.run("git clone https://github.com/FurkanGozukara/rop_fixed roop", shell=True, capture_output=True, text=True)
    st.text(result.stdout + result.stderr)

if st.button("Clone BasicSR repo"):
    result = subprocess.run("cd roop && git clone https://github.com/FurkanGozukara/BasicSR", shell=True, capture_output=True, text=True)
    st.text(result.stdout + result.stderr)

if st.button("Install requirements (a.txt)"):
    result = subprocess.run("cd roop && pip install -r a.txt", shell=True, capture_output=True, text=True)
    st.text(result.stdout + result.stderr)

if st.button("Uninstall basicsr"):
    result = subprocess.run("pip uninstall basicsr --yes", shell=True, capture_output=True, text=True)
    st.text(result.stdout + result.stderr)

if st.button("Install BasicSR editable"):
    result = subprocess.run("cd roop/BasicSR && pip install -e .", shell=True, capture_output=True, text=True)
    st.text(result.stdout + result.stderr)

if st.button("Patch opennsfw2"):
    module_name = "opennsfw2._inference"
    try:
        spec = importlib.util.find_spec(module_name)
        if spec is None or spec.origin is None:
            st.error(f"Could not find the module '{module_name}'. Is opennsfw2 installed?")
        else:
            file_path = spec.origin
            with open(file_path, 'r') as f:
                lines = f.readlines()
            patched = False
            with open(file_path, 'w') as f:
                for line in lines:
                    if "cv2.destroyAllWindows()" in line:
                        f.write("#" + line)
                        patched = True
                    else:
                        f.write(line)
            if patched:
                st.success("Patch applied successfully!")
            else:
                st.warning("The line 'cv2.destroyAllWindows()' was not found. The file may already be patched or has changed.")
    except Exception as e:
        st.error(f"An error occurred: {e}\nPlease ensure the 'opennsfw2' library is installed correctly.")
