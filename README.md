
# Roomio
 
## Project Setup Instructions

This guide will walk you through setting up a Python virtual environment and installing the necessary dependencies for your project.

### Step 1: Install virtualenv

Before creating a virtual environment, you need to ensure that `virtualenv` is installed on your system. You can install it using pip, the Python package installer. Open a terminal or command prompt and execute the following command:

```bash
pip install virtualenv
```

### Create virtual env
```bash
virtualenv projectenv
```

### Activate the Virtual Environment

On Windows:
```bash
source projectenv/Scripts/activate
```

On Mac:
```bash
source projectenv/bin/activate
```

### Install required packages
```terminal
pip install -r requirements.txt
```

### Using dotenv to manage environment variables

To manage your application's environment variables more securely and conveniently, you can use the `python-dotenv` package. This allows you to load environment variables from a `.env` file into your project. Here’s how you can set it up:

1. Install `python-dotenv` using pip:
   ```bash
   pip install python-dotenv
   

2. Create a `.env` file in the root of your project directory. Add your environment variables to this file. For example:
   ```plaintext
   DB_NAME=dmname
   DB_USER=usrname
   DB_PASSWORD=pwd
   DB_HOST=host
   DB_PORT=8000 #can be any

3. Load the environment variables from the `.env` file in your project. Make sure to do this early in your application's startup. For a Django project, you can do this in the `settings.py` file:
   ```python
   from dotenv import load_dotenv
   import os

   load_dotenv()  # This loads the environment variables from the .env file.

   # Now you can use os.getenv to access your environment variables.
   DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    },
   }

By following these steps, you ensure that your sensitive information and configuration are not hardcoded into your application's source code, providing an additional layer of security.

