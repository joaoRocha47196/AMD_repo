#!/bin/bash

DB_NAME="my_db"
USER="postgres"
PASSWORD="password1234"
HOST="127.0.0.1"

export PGPASSWORD=$PASSWORD

# Check if the database exists
if psql -h $HOST -U $USER -lqt | cut -d \| -f 1 | grep -qw $DB_NAME; then
    dropdb -h $HOST -U $USER $DB_NAME
fi

# Create DB
createdb -h $HOST -U $USER $DB_NAME

# Connect to DB and create a table
psql -h $HOST -U $USER $DB_NAME <<EOF
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

\l
\dt 
EOF

echo "Done!"
