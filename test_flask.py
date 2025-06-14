try:
    import flask
    from flask import Flask
    print("Flask imported successfully!")
    print(f"Flask version: {flask.__version__}")  # Use flask module, not Flask class
    print(f"Flask location: {flask.__file__}")
except ImportError as e:
    print(f"Error importing Flask: {e}")
