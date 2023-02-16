# Start with a base image
FROM python:3

# Copy our application code
WORKDIR /var/app
COPY . .
COPY requirements.txt .

# Fetch app specific dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pwd
RUN ls

# Expose port
EXPOSE 5000

# Start the app
CMD ["gunicorn", "wsgi:app", "--bind", "0.0.0.0:5000"]