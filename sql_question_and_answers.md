## MySQL 

**Q**: Remember some basic MySQL terminal command: 

- log in
- backup 
  - one database
  - backup all databases
- restore
  - one database
  - all database

**A**: Assuming I am log in as root user.

```shell
# log in
$ mysql -u root -p  # -u user, -p password

# backup the sakila database
$ mysqldump -u root -p sakila > /path/to/backup/directory/sakila.sql
# back up with compression
$ mysqldump -u root -p -C sakila > /path/to/backup/directory/sakila.sql.tgz

# backup all databases
$ mysqldump -u root -p --all-databases > /path/to/backup/directory/all_databases.sql

# restore one database from backup as database called aaa
$ mysql -u root -p aaa < /path/to/backup/directory/sakila.sql

# restore all databases, which overwrite all current ones !!!
$ mysql -u root -p < /path/to/backup/directory/all_databases.sql
```



## Basic concepts

**Q**: How to understand data integrity of a SQL database?

**A**: Data integrity refers to the accuracy, consistency, and reliability of data stored in a database. Data integrity is enforced by database constraint. There are four types of data integrity and each is enforced by different database constraints.

- Row integrity: all rows must have an identifier (normally primary key) to tell records apart. Enforced by
  - primary key constraint
  - unique constraint
- Column integrity: all data stored in a column must adhere to the same format and definition such as data type, length, and default value. Enforced by 
  - foreign key constraint
  - check constraint, which is a user defined rule
  - default constraint
  - data type constraint
  - nullability constraint
- Referential integrity: the tables that foreign keys pointing to in a table must exist. Enforced by 
  - foreign key constraint
- Use-defined integrity enforced by 
  - check constraint



**Q**: How to understand database normalization?

refer to https://www.essentialsql.com/get-ready-to-learn-sql-11-database-third-normal-form-explained-in-simple-english/

**A**: Database normalization is used to organize a relational database according to norm forms (NFs) to reduce data redundancy and improve data integrity. 

- 1NF (first normal form) rules: Being the most important form, the 1NF, however, does not have a explicit definition.  Usually it follows the following rules
  - Each table cell should contain an atomic value. Whether or not a value is atomic depends on what you want. For example, telephone number with area code.
  - There is no repeating groups of columns such as Custom1Name, Custom2Name, ... (why even doing this?)
  - Create a primary key for each table.
- 2NF: In addition to be in the 1NF, 
  - All the non-key columns are dependent on the primary key so that the whole table has a single purpose serving the object represented by the primary key. For example, for a person_ID, the column County with values of "USA", "CHINA", ... is not in the 2NF. When not in the 2NF, there will be repeating numbers or strings other than repeating foreign keys. Creating new tables to mitigate repeating issue if necessary and replace repeats with foreign keys.
- 3NF: in addition to be in the 2NF,
  - It contains only columns that are non-transitively dependent on the primary key. Examples of transitive dependence:
    - Person table has columns PersonID, BodyMassIndex, and IsOverweight. The column IsOverweight transitively depends on the primary key through BodyMassIndex.
    - Car table has columns VehicleID, Model, and Manufacturer. Manufacturer transitively depends on the primary key through Model.

## Work as a database manager

**Q**: How to show, create, drop, and select databases?

**A**: run as MySql code.

```mysql
-- show all available databases
SHOW DATABASES;

-- use sakila 
USE sakila;

-- show which database is being used
SELECT DATABASE();

-- create database called aaa
CREATE DATABASE aaa;

-- delete database aaa
DROP DATABASE aaa;
```



**Q**: How to display, create, and delete tables in a database?

**A**: After `USE` a database, we can work on the tables of the database.

```mysql
-- list names of all tables in a database
SHOW tables;

-- display the definition of a table
SHOW CREATE TABLE film;   # using sakila 

-- create a new table
CREATE TABLE IF NOT EXISTS aaa (
    id INT(5) UNSIGNED NOT NULL AUTO_INCREMENT,
    name CHAR(20) NOT NULL,
    film_id SMALLINT(5) UNSIGNED NOT NULL,
    
    PRIMARY KEY (id),
    INDEX USING BTREE (name),
    CONSTRAINT FOREIGN KEY (film_id)
        REFERENCES film (film_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- delete a table
DROP TABLE aaa;
```

**Q**: How to display all columns of a table? How to add, delete, modify a column? 

**A**: In addition to these tasks, we can also add or drop a constraint to a column, which is another topic.

```mysql
-- show column details of a table
DESCRIBE table_name;

-- add, and drop columns
ALTER TABLE aaa ADD COLUMN age INT UNSIGNED;
ALTER TABLE aaa DROP COLUMN age;

-- modify a column definition
ALTER TABLE aaa MODIFY name VARCHAR(56) NOT NULL

-- change column name, have to attach definition
ALTER TABLE aaa CHANGE COLUMN id aaa_id INT UNSIGNED NOT NULL AUTO_INCREMENT;
```



**Q**: How to insert new rows? How to change values of cells? How to delete rows?

**A**: To insert new rows, you must provide values for all columns without default values. 

```mysql
# manually insert values, can spam multiple rows
INSERT INTO table_1 (col_1, col_2, ...)
VALUES (value_1, value_2, ...),
       (value_a, value_b, ...);
       
# insert with query result
INSERT INTO table_1 (name, film_id)
	SELECT name, film_id
	FROM table_2;
```























## Work as a database user

### Operations

**Q**: What are the types of joins? How and when to use them?

**A**: The `JOIN` operator is used to combine the columns of two tables under conditions. Syntax example:

```sql
/* works for inner join,
left join, right join, 
and full join */
select * 
from customer c
	inner join orders o    
	on c.customer_id = o.customer_id  -- keep this even for full join
```

- `inner join`: keep only rows from both tables where the `on` condition met.
- `outer join` has three types:
  - `left join` or `left outer join`: keep all rows from left table and those meet conditions from the right
  - `right join` or `right outer join`: keep all rows from right table and those meet conditions from the left
  - `full join` or `full outer join`:  keep all row from both table no matter condition met or not. 

**Q**: What is `UNION` for and how to use it?

**A**: The `UNION` operator is used to combine the rows of the result-set of two `SELECT` statements. The result-sets must have the same columns in the same order. It only keeps unique rows. To allow for duplicated rows, use `UNION ALL`. 

```sql
(SELECT return_date, 
    rental_date,
    first_name,
    last_name,
    store_id
FROM rental r INNER JOIN customer c
ON r.customer_id=c.customer_id
ORDER BY last_name desc
LIMIT 5)

UNION

(SELECT return_date, 
    rental_date,
    first_name,
    last_name,
    store_id
FROM rental r, customer c
WHERE r.customer_id=c.customer_id and c.store_id < 3
ORDER BY last_name
LIMIT 5);
```



