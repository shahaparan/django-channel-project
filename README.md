# Check Python version
python3 --version

# Create a virtual environment
python3 -m venv venv

# Change permissions of the virtual environment directory (not recommended for security reasons, use with caution)
sudo chmod -R 777 venv

# Install necessary system packages for Python virtual environments
sudo apt install python3.10-venv

# Activate the virtual environment
source venv/bin/activate

# Deactivate the virtual environment when done
deactivate

# Install project dependencies from requirements.txt
pip install -r requirements.txt

# Apply database migrations
python manage.py migrate

# Start the Django development server
python3 manage.py runserver



# Remove the project directory if necessary (replace 'python-django' with the correct directory name)
rm -r python-django

# Start a new Django project named 'ecommerce' in the current directory
django-admin startproject ecommerce .

# Start a new Django app named 'inventory'
python manage.py startapp inventory

# Create new migrations based on the changes detected in your models
python3 manage.py makemigrations

# Create a Django superuser for accessing the admin interface
python3 manage.py createsuperuser
# Follow the prompts to create the superuser, e.g., username: admin


# If you encounter permission issues, refer to this link for a fix:
# https://bobbyhadz.com/blog/python-could-not-install-packages-due-to-an-environmenterror-errno-13

# The above link suggests a fix like:
# pip install --user package_name
