FROM python:3.12

RUN pip install pandas sqlalchemy psycopg2-binary

COPY import_all.py /app/import_all.py

CMD ["python", "/app/import_all.py"]