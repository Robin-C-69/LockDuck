FROM python:3.10.15-slim

# Create working directory
RUN mkdir -p /lockduck
WORKDIR /lockduck

# Install requirements
COPY app/requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy application
COPY app /lockduck

# Run the app
CMD ["python","/lockduck/app.py"]
