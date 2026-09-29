/*
LeetCode 1934 - Confirmation Rate
URL: https://leetcode.com/problems/confirmation-rate/

Table: Signups
+----------------+----------+
| Column Name    | Type     |
+----------------+----------+
| user_id        | int      |
| time_stamp     | datetime |
+----------------+----------+
user_id is the primary key (column with unique values) for this table.
Each row contains information about the signup time for the user with
id user_id.

Table: Confirmations
+----------------+----------+
| Column Name    | Type     |
+----------------+----------+
| user_id        | int      |
| time_stamp     | datetime |
| action         | ENUM     |
+----------------+----------+
(user_id, time_stamp) is the primary key (column with unique values) for
this table. user_id is a foreign key (reference column) to the Signups
table. action is an ENUM (category) of the type ('confirmed', 'timeout').
This table contains the confirmation requests sent to the users after
they signed up, either resulting in a 'confirmed' or 'timeout' action.

Task:
The confirmation rate of a user is the number of 'confirmed' messages
divided by the total number of requests that user sent. Users that did
not request any confirmation messages have a confirmation rate of 0.
Round the confirmation rate to two decimals.

Write a solution to find the confirmation rate of each user.
Return the result table in any order.

Example 1:
Input:
Signups table:
+---------+---------------------+
| user_id | time_stamp          |
+---------+---------------------+
| 3       | 2020-03-21 10:16:13 |
| 7       | 2020-01-04 13:57:59 |
| 2       | 2020-07-29 23:09:44 |
| 6       | 2020-12-09 10:39:37 |
+---------+---------------------+

Confirmations table:
+---------+---------------------+-----------+
| user_id | time_stamp          | action    |
+---------+---------------------+-----------+
| 3       | 2020-03-21 10:16:14 | confirmed |
| 3       | 2020-06-13 15:37:14 | confirmed |
| 7       | 2020-01-04 13:58:02 | confirmed |
| 7       | 2020-01-04 13:58:13 | timeout   |
| 7       | 2020-01-05 00:00:23 | confirmed |
| 2       | 2020-07-29 23:09:56 | timeout   |
| 2       | 2020-07-29 23:22:34 | timeout   |
| 6       | 2020-12-09 10:39:37 | confirmed |
+---------+---------------------+-----------+

Output:
+---------+-------------------+
| user_id | confirmation_rate |
+---------+-------------------+
| 6       | 1.00              |
| 3       | 1.00              |
| 7       | 0.67              |
| 2       | 0.00              |
+---------+-------------------+
*/

SELECT
    s.user_id,
    ROUND(
        COALESCE(
            AVG(CASE WHEN c.action = 'confirmed' THEN 1 ELSE 0 END),
            0
        ),
        2
    ) AS confirmation_rate
FROM Signups s
LEFT JOIN Confirmations c ON s.user_id = c.user_id
GROUP BY s.user_id;

/*
Observation:
- Every user in Signups must appear in the output, even those with zero
  confirmation requests - that's why the join is a LEFT JOIN from
  Signups to Confirmations, not an inner join. An inner join would drop
  user 2's row entirely if they never requested confirmation (in this
  example they did request, but timed out both times).
- AVG(CASE WHEN action = 'confirmed' THEN 1 ELSE 0 END) is a common
  pattern for turning a ratio-of-rows calculation into an aggregate:
  each row contributes 1 if confirmed, 0 otherwise, and AVG naturally
  computes (count of confirmed) / (count of total rows) per group.
- COALESCE(..., 0) handles the case where a user has no matching
  Confirmations rows at all: the LEFT JOIN produces a single row with
  c.action = NULL for that user, AVG() over an empty/NULL-only set
  returns NULL, and COALESCE converts that NULL into 0 as required.
- ROUND(..., 2) is applied after the AVG/COALESCE to satisfy the
  "round to two decimals" requirement (e.g. 2/3 -> 0.67).
- Grouping by s.user_id (the primary key of Signups) guarantees one
  output row per signed-up user, matching the expected result shape.
*/
