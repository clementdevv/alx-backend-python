# 1. Use a base image with Python 3.10 
FROM python:3.10

# 2. Set working directory inside the container
WORKDIR /app

# 3. Copy the requirements file into the container
COPY requirements.txt /app/

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy all project files into the container
COPY . /app/

# 6. Expose Django's default port
EXPOSE 8000

# 7. Run the Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

#-p