import sys
import os
from cx_Freeze import setup, Executable

# Base setup
base = "Win32GUI" if sys.platform == "win32" else None

# File inclusions
include_files = [
    ("src/preprocessing/training_columns.csv", "src/preprocessing/training_columns.csv"),
    ("src/preprocessing/scaler.joblib", "src/preprocessing/scaler.joblib"),
    ("src/model/lenn1.3.keras", "src/model/lenn1.3.keras")
]

# Build options
build_options = {
    "packages": [
        "os", "customtkinter", "pandas", "numpy",
        "sklearn", "keras", "tensorflow", "joblib",
        "src.gui", "src.preprocessing", "src.prediction"
    ],
    "include_files": include_files,
    "excludes": ["tkinter"],
    "optimize": 1,
    "path": sys.path + ["src"]
}

executables = [
    Executable(
        "src/gui/gui_5_0.py",
        base=base,
        target_name="LoanEligibilityChecker",
        #icon="assets/icon.ico" if sys.platform == "win32" else None
    )
]

setup(
    name="Loan Eligibility Checker",
    version="1.0",
    description="Loan Prediction Application",
    options={"build_exe": build_options},
    executables=executables,
    package_dir={"": "src"},
    packages=["gui", "preprocessing", "prediction"]
)
