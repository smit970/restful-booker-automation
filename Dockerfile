# 1. Base Image: Start with a lightweight Linux + Python 3.9
FROM python:3.9-slim

# 2. Setup Work Directory: Create a folder named /app inside the container
WORKDIR /app

# 3. Copy Requirements FIRST (Optimization):
# Docker caches this step. If requirements don't change, it won't re-install them.
COPY requirements.txt .

# 4. Install Dependencies:
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your code:
# This moves all your .py and .json files into /app
COPY . .

# 6. The Command: What happens when the container starts?
# Run pytest and generate a report
CMD ["pytest", "-v", "-s", "--html=report.html"]