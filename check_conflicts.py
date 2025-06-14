import os
import sys

print("Checking for flask conflicts...")
project_root = os.path.dirname(os.path.abspath(__file__))

# Check for any flask.py or flask directory in the project root
flask_file = os.path.join(project_root, "flask.py")
flask_dir = os.path.join(project_root, "flask")

if os.path.exists(flask_file):
    print(f"WARNING: Found conflicting file: {flask_file}")
    print("Consider renaming or removing this file.")

if os.path.exists(flask_dir) and os.path.isdir(flask_dir):
    print(f"WARNING: Found conflicting directory: {flask_dir}")
    print("Consider renaming or removing this directory.")

print("Checking sys.path directories...")
for path in sys.path:
    if os.path.isdir(path):
        flask_file_in_path = os.path.join(path, "flask.py")
        if os.path.exists(flask_file_in_path):
            print(f"WARNING: Found flask.py in Python path: {flask_file_in_path}")
