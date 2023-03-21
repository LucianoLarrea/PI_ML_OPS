FROM tiangolo/uvicorn-gunicorn-fastapi

RUN pip install pandas

COPY    ./app   ./app
COPY   ./data ./data
