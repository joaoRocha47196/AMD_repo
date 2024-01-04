--#############
--# Paulo Trigo
--#############


--==============
-- DB connection
--==============
\set dataBase db_e_commerce_project_b
;
\set userName postgres
;
\connect :dataBase :userName
--==========================
--==========================


-- additional information about "client_encoding" in:
-- http://www.postgresql.org/docs/9.6/static/multibyte.html
-- \encoding WIN1250
\encoding UTF8
;



---------------------------------
DROP VIEW IF EXISTS v_export;
DROP VIEW IF EXISTS v_product;
DROP VIEW IF EXISTS v_number_of_events_per_session_number_of_cookies;
DROP VIEW IF EXISTS v_number_of_cookies_number_of_sessions;
DROP VIEW IF EXISTS v_cookie_number_of_sessions;
DROP VIEW IF EXISTS v_cookie_session_number_of_events;
---------------------------------



--=============================================================================
-- total number of events (each tuple is an event)
--=============================================================================
\! echo "total number of events"
SELECT COUNT(*) as total_events
FROM track
;



--=============================================================================
-- total number of distinct cookies (visitors)
--=============================================================================
\! echo "total number of distinct cookies"
SELECT COUNT(DISTINCT cookie_id) AS total_number_of_cookies
FROM track;





--=============================================================================
-- aggregate (group) cookies and sessions and get the total number of events
--=============================================================================
\! echo "total number of events per cookie and session"
CREATE VIEW v_cookie_session_number_of_events (cookie_id, session_id, number_of_events_per_session)
AS
SELECT cookie_id, session_id, COUNT(*) AS number_of_events_per_session
FROM track
GROUP BY cookie_id, session_id
ORDER BY number_of_events_per_session DESC;


SELECT *
FROM v_cookie_session_number_of_events
WHERE number_of_events_per_session >= 100
;



--=============================================================================
-- aggregate cookie and get the total number of sessions (for each cookie)
-- and the total number of events for each session
--=============================================================================
\! echo "total number of sessions per cookie"
CREATE VIEW v_cookie_number_of_sessions (cookie_id, number_of_sessions, total_events)
AS
SELECT 
    cookie_id, 
    COUNT(session_id) AS number_of_sessions, 
    SUM(number_of_events_per_session) AS total_events
FROM v_cookie_session_number_of_events
GROUP BY cookie_id
ORDER BY number_of_sessions DESC;

SELECT *
FROM v_cookie_number_of_sessions
WHERE number_of_sessions >= 30
;

-- \! echo "number-of-visitors Vs number-of-sessions"
-- SELECT COUNT(cookie_id) AS number_of_visitors, number_of_sessions
-- FROM v_cookie_number_of_sessions
-- GROUP BY number_of_sessions
-- ORDER BY number_of_sessions;

-- \! echo "number-of-events-per-session Vs number-of-visitors"
-- SELECT number_of_events_per_session, COUNT(cookie_id) AS number_of_visitors
-- FROM v_cookie_session_number_of_events
-- GROUP BY number_of_events_per_session
-- ORDER BY number_of_events_per_session;

-- \! echo "Test: number-of-sessions = 18"
-- SELECT cookie_id AS visitor_id, number_of_sessions, total_events
-- FROM v_cookie_number_of_sessions
-- WHERE number_of_sessions = 18;


--=============================================================================
-- aggregate number of sessions and get total cookies (visitors) at each session
--=============================================================================
\! echo "total number of cookies per session"
CREATE VIEW v_number_of_cookies_number_of_sessions (number_of_cookies, number_of_sessions)
AS
SELECT 
    COUNT(cookie_id) AS number_of_cookies, 
    number_of_sessions
FROM v_cookie_number_of_sessions
GROUP BY number_of_sessions
ORDER BY number_of_cookies DESC;


-- SELECT *
-- FROM v_number_of_cookies_number_of_sessions
-- ;



--=============================================================================
-- aggregate the number of events per session and get the distribution of
-- the number of cookies (visitors) 
--=============================================================================
\! echo "total number of cookies per number of events per session"
CREATE VIEW v_number_of_events_per_session_number_of_cookies (number_of_events_per_session, number_of_cookies)
AS
SELECT 
    number_of_events_per_session, 
    COUNT(cookie_id) AS number_of_cookies
FROM v_cookie_session_number_of_events
GROUP BY number_of_events_per_session
ORDER BY number_of_events_per_session DESC;


-- SELECT *
-- FROM v_number_of_events_per_session_number_of_cookies
-- WHERE number_of_events_per_session >= 5 AND number_of_events_per_session <= 30
-- ;


--=============================================================================
-- build a view for the top products
--=============================================================================
\! echo "top products"
CREATE VIEW v_product AS
SELECT product_gui, COUNT(*) as frequency
FROM track
WHERE product_gui NOT IN ('open', 'home', '/customer/account/login/', '/customer/account/forgotpassword/' ) 
AND product_gui NOT LIKE '%/order_id/%' AND product_gui NOT LIKE '%/account/%' 
GROUP BY product_gui
ORDER BY frequency DESC
;

SELECT * FROM v_product
LIMIT 50
;


--=============================================================================
-- build a view for the data to be exported and to be transformed into a basket
-- this may be different depending on the basket you want to build
--=============================================================================
\! echo "data to be exported"
CREATE VIEW v_export (cookie_id, session_id, product_gui)
AS
SELECT T1.cookie_id, T2.session_id, T2.product_gui
FROM 
    (SELECT *
     FROM v_cookie_number_of_sessions
     WHERE number_of_sessions >= 5 AND number_of_sessions <= 30) AS T1
INNER JOIN
    track AS T2
ON T1.cookie_id = T2.cookie_id
WHERE T2.product_gui NOT IN ('open', 'home', '/customer/account/login/', '/customer/account/forgotpassword/' ) 
AND T2.product_gui NOT LIKE '%/order_id/%' AND T2.product_gui NOT LIKE '%/account/%' 
ORDER BY T1.cookie_id, T2.session_id, T2.product_gui;


-- SELECT *
-- FROM v_export
-- LIMIT 30
-- ;





