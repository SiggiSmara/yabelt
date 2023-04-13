# Working name: YABELT

Yet Another Basic ELT Framework

## Basic workflow

1. Choose your source db and destination db types from the available dbs via the `.env` file 
   (can also be defined via API calls).  Currently the focus is on Microsoft SQL server and PostgresSQL.  Possible others would be SQLite, Oracle DB and MySQL/MariaDB.
2. Set up the source db table definitions including the frequency of inserts and updates for each table. (API)
3. Populate the tables in the destination db (API)
4. Start the db sync process (API)
5. Look at the latency table in the destination db for statistics on performance

## sql server on linux docker

See https://learn.microsoft.com/en-us/sql/linux/quickstart-install-connect-docker?view=sql-server-ver16&pivots=cs1-bash

``` sh
docker pull mcr.microsoft.com/mssql/server:2022-latest

docker run -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=Forvitinn5!" \
   -p 1433:1433 --name sql1 --hostname sql1 \
   -d \
   mcr.microsoft.com/mssql/server:2022-latest

docker ps -a

docker exec -t sql1 cat /var/opt/mssql/log/errorlog | grep connection

docker stop sql1
```

## Based on

https://github.com/tiangolo/full-stack-fastapi-postgresql
https://testdriven.io/blog/fastapi-and-celery/
https://progressstory.com/tech/python/production-ready-celery-configuration/
