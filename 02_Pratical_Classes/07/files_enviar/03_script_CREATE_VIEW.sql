--#############
--# Paulo Trigo
--#############


--==============
-- DB connection
--==============
\set dataBase db_e_commerce_sample
;
\set userName postgres
;
\connect :dataBase :userName
--==========================
--==========================


-- additional information about "client_encoding" in:
-- http://www.postgresql.org/docs/9.6/static/multibyte.html
-- \encoding WIN1250
;



---------------------------------
DROP VIEW IF EXISTS v_export;
DROP VIEW IF EXISTS v_number_of_events_per_session_number_of_cookies;
DROP VIEW IF EXISTS v_number_of_cookies_number_of_sessions;
DROP VIEW IF EXISTS v_cookie_number_of_sessions;
DROP VIEW IF EXISTS v_cookie_session_number_of_events;
---------------------------------



--=============================================================================
-- total number of events (each tuple is an event)
--=============================================================================
SELECT COUNT(*) as total_events
FROM track
;



--=============================================================================
-- total number of distinct cookies (visitors)
--=============================================================================
SELECT COUNT(*) AS total_number_of_cookies
FROM (SELECT DISTINCT cookie_id FROM track) AS T
;



--=============================================================================
-- aggregate (group) cookies and sessions and get the total number of events
--=============================================================================
CREATE VIEW v_cookie_session_number_of_events (cookie_id, session_id, number_of_events_per_session)
AS
SELECT cookie_id, session_id, COUNT(*) AS number_of_events_per_session
FROM track
GROUP BY cookie_id, session_id
ORDER BY cookie_id, session_id;


SELECT *
FROM v_cookie_session_number_of_events
;



--=============================================================================
-- aggregate cookie and get the total number of sessions (for each cookie)
-- and the total number of events for each session
--=============================================================================
CREATE VIEW v_cookie_number_of_sessions (cookie_id, number_of_sessions, total_events)
AS
SELECT 
    cookie_id, 
    COUNT(session_id) AS number_of_sessions, 
    SUM(number_of_events_per_session) AS total_events
FROM v_cookie_session_number_of_events
GROUP BY cookie_id
ORDER BY cookie_id;

SELECT *
FROM v_cookie_number_of_sessions
;



--=============================================================================
-- aggregate number of sessions and get total cookies (visitors) at each session
--=============================================================================
CREATE VIEW v_number_of_cookies_number_of_sessions (number_of_cookies, number_of_sessions)
AS
SELECT 
    COUNT(cookie_id) AS number_of_cookies, 
    number_of_sessions
FROM v_cookie_number_of_sessions
GROUP BY number_of_sessions
ORDER BY number_of_sessions;


SELECT *
FROM v_number_of_cookies_number_of_sessions
;



--=============================================================================
-- aggregate the number of events per session and get the distribution of
-- the number of cookies (visitors)
--=============================================================================
CREATE VIEW v_number_of_events_per_session_number_of_cookies (number_of_events_per_session, number_of_cookies)
AS
SELECT 
    number_of_events_per_session, 
    COUNT(DISTINCT cookie_id) AS number_of_cookies
FROM v_cookie_session_number_of_events
GROUP BY number_of_events_per_session
ORDER BY number_of_events_per_session;


SELECT *
FROM v_number_of_events_per_session_number_of_cookies
;



--=============================================================================
-- build a view for the data to be exported and to be transformed into a basket
-- this may be different depending on the basket you want to build
--=============================================================================
CREATE VIEW v_export (cookie_id, session_id, product_gui)
AS
SELECT T1.cookie_id, T2.session_id, T2.product_gui
FROM 
    (SELECT *
     FROM v_cookie_number_of_sessions
     WHERE number_of_sessions >= 1 AND number_of_sessions <= 30) AS T1
INNER JOIN
    track AS T2
ON T1.cookie_id = T2.cookie_id
WHERE T2.product_gui NOT IN ('open', 'home')
ORDER BY T1.cookie_id, T2.session_id, T2.product_gui;


SELECT *
FROM v_export
;





