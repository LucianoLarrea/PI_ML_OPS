FROM tiangolo/uvicorn-gunicorn-fastapi

RUN pip install pandas
RUN pip install pyarrow
RUN pip install fastparquet

COPY    ./app   .
COPY   ./data ./data
