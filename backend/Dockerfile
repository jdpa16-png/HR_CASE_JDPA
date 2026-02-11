From python:3.14-slim

RUN pip install uv

WORKDIR /app

#Copy dependencies files first
COPY pyproject.toml uv.lock ./

#Install dependencies
RUN uv sync

#Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

#Start FastAPI app
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]