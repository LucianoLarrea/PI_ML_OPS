FROM tiangolo/uvicorn-gunicorn-fastapi

RUN pip install pandas
RUN pip install pyarrow

COPY    ./app   .
COPY   ./data ./data
