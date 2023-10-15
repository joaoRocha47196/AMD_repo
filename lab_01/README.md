sudo dnf install postgresql postgresql-server
sudo postgresql-setup --initdb
sudo systemctl start postgresql
sudo systemctl enable postgresql

sudo su - postgres

psql


---

$ sudo -i -u postgres

$ createdb mydb --> create db
$ dropdb mydb --> delete
$ psql mydb



---

# \list --> List of databases
# \dt --> List of relations
# \c --> Connect to a database


---
CREATE TABLE products (
product_no integer PRIMARY KEY,
name text,
price numeric
);


CREATE TABLE orders (
order_id integer PRIMARY KEY,
product_no integer REFERENCES products (product_no),
quantity integer
);

CREATE TABLE order_items (
product_no integer REFERENCES products ON DELETE RESTRICT,
order_id integer REFERENCES orders ON DELETE CASCADE,
quantity integer,
PRIMARY KEY (product_no, order_id)
);