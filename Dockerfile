FROM python:3.11

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./sql_app /code/sql_app

#
EXPOSE 3100

# 
CMD ["gunicorn", "sql_app.main:app"]
