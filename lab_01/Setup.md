sudo ls -la /var/lib/pgsql/data
sudo rm -r /var/lib/pgsql/data
sudo postgresql-setup --initdb

sudo systemctl start postgresql
sudo systemctl enable postgresql

sudo su - postgres
psql

\password postgres


---

cd "C:\Program Files\PostgreSQL\16\bin\"
.\psql.exe -U postgres

CREATE DATABASE my_db;





