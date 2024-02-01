FROM python:3.11.3

# Set the working directory in the container
WORKDIR /usr/src/app

# Install any needed packages specified in requirements.txt
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source code
COPY models/ ./models/
COPY data_sources/ ./data_sources/
COPY utils/ ./utils/
COPY source_data/ ./source_data/
COPY data_source.py ./

# Define environment variables
ENV NEO4J_URI=localhost:7687
ENV NEO4J_USER=neo4j
ENV NEO4J_PASSWORD=password

# Make port 80 available to the world outside this container
EXPOSE 80

# Run the script when the container launches
CMD ["python", "./data_source.py"]