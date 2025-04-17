from cx_Freeze import setup, Executable
import os
import sys

base_path = os.path.abspath(os.path.dirname(__file__))

build_exe_options = {
    "include_msvcr": True,
    "packages": [
        "customtkinter", "tkinter", "pandas", "numpy", "matplotlib",
        "sklearn", "scipy", "joblib", "keras", "tensorflow", "tensorboard"
    ],
    "includes": ["matplotlib.backends.backend_tkagg"],
    "include_files": [
        os.path.join(base_path, "gui"),
        os.path.join(base_path, "model"),
        os.path.join(base_path, "preprocessing"),
        os.path.join(base_path, "prediction"),
        os.path.join(base_path, "requirements.txt"),
        (r"C:\Users\namei\AppData\Local\Programs\Python\Python310\python310.dll",
         "python310.dll")
    ]
}

base = "Win32GUI" if sys.platform == "win32" else None

setup(
    name="P-LEPS",
    version="1.0",
    description="Machine learning app to predict loan eligibility",
    options={"build_exe": build_exe_options},
    executables=[Executable("gui/gui_5_0.py", base=base)]
)
