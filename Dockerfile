# Use an official Python runtime as a base image
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/

# Expose port 8000 for the Gunicorn server
EXPOSE 8000

RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# Set the default command to run Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "librarySystem.wsgi:application"]
