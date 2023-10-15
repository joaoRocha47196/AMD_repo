c) Combining `v1_domain` and `v1` with `v1_domain` always appearing on top can be achieved using a `UNION ALL` combined with an `ORDER BY`. However, for ordering purposes, we'll introduce an artificial ordering column.

Let's modify both views slightly to add the order column:

```sql
-- Modify v1_domain to include an ordering column
CREATE OR REPLACE VIEW v1_domain AS
SELECT 
    1 AS order_col, -- for ordering
    'ConstantValue1'::text AS VC1,
    'ConstantValue2'::text AS VC2,
    'ConstantValue3'::text AS VC3;

-- Modify v1 to include an ordering column
CREATE OR REPLACE VIEW v1( order_col, VC1, VC2, VC3 ) AS
SELECT 
    2 AS order_col, -- for ordering
    r2.c1 as VC1, 
    r2.c1_r1 as VC2, 
    r3.C1 as VC3
FROM r2
JOIN r3 ON r2.c1_r1 = r3.C1_R1;
```

Then, the SELECT statement to combine them:

```sql
SELECT VC1, VC2, VC3
FROM (
    SELECT * FROM v1_domain
    UNION ALL
    SELECT * FROM v1
) combined_views
ORDER BY order_col;
```

d) Now, create the `v1_dataset` view:

```sql
CREATE VIEW v1_dataset AS
SELECT VC1, VC2, VC3
FROM (
    SELECT * FROM v1_domain
    UNION ALL
    SELECT * FROM v1
) combined_views
ORDER BY order_col;
```

To test:

```sql
SELECT * FROM v1_dataset;
```

e) If you populate `r2` and `r3` with additional tuples, the behavior of `v1` and consequently `v1_dataset` will reflect these changes since they are views built on top of those tables. However, the `v1_domain` row will always be at the top of the `v1_dataset` view due to our artificial order column.

Let's add a sample tuple:

```sql
INSERT INTO r2( c1, c1_r1, c2, c3 )
VALUES ( '444', 4, 'xxx444', 'yyy444' );

INSERT INTO R3( C1_R1, C1_R4, C1 )
VALUES( 4, 10, '2012-04-30' );
```

Now, if you explore the `v1_dataset` view:

```sql
SELECT * FROM v1_dataset;
```

You should see the new data, with `v1_domain` still appearing at the top.