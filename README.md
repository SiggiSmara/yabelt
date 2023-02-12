# Working name: YABELT

Yet Another Basic ELT Framework

## Basic workflow

1. Choose your source db and destination db types from the available dbs via the `.env` file.  Currently the focus is on Microsoft SQL server and PostgresSQL.  Possible others would be SQLite, Oracle DB and MySQL/MariaDB.
2. Set up the source db and decide on the frequency of inserts and updates for each table.
3. Start the source db process to populate the tables.
4. Start the destination db sync process
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
