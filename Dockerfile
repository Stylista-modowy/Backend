FROM python:3.10

RUN apt-get update && apt-get install libgl1 -y

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./sql_app /code/sql_app

#
EXPOSE 5000

# 
CMD ["uvicorn", "sql_app.main:app", "--host", "0.0.0.0", "--port", "5000"]
