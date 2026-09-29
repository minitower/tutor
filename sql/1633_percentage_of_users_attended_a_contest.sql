/*
LeetCode 1633 - Percentage of Users Attended a Contest
URL: https://leetcode.com/problems/percentage-of-users-attended-a-contest/

Table: Users
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| user_id     | int     |
| user_name   | varchar |
+-------------+---------+
user_id is the primary key (column with unique values) for this table.
Each row of this table contains the name and the id of a user.

Table: Register
+---------------+------+
| Column Name   | Type |
+---------------+------+
| contest_id    | int  |
| user_id       | int  |
+---------------+------+
(contest_id, user_id) is the primary key (combination of columns with
unique values) for this table. Each row of this table contains the id
of a user and the contest they registered for.

Task:
Write a solution to find the percentage of users registered in each
contest rounded to two decimals.
Return the result table ordered by percentage in descending order. In
case of a tie, order it by contest_id in ascending order.

Example 1:
Input:
Users table:
+---------+-----------+
| user_id | user_name |
+---------+-----------+
| 6       | Donald    |
| 2       | Jonathan  |
| 8       | Jade      |
+---------+-----------+

Register table:
+------------+---------+
| contest_id | user_id |
+------------+---------+
| 215        | 6       |
| 209        | 2       |
| 208        | 2       |
| 210        | 6       |
| 208        | 6       |
| 209        | 8       |
| 209        | 6       |
| 215        | 8       |
| 208        | 8       |
| 210        | 2       |
| 207        | 2       |
| 210        | 8       |
+------------+---------+

Output:
+------------+------------+
| contest_id | percentage |
+------------+------------+
| 208        | 100.0      |
| 209        | 100.0      |
| 210        | 100.0      |
| 215        | 66.67      |
| 207        | 33.33      |
+------------+------------+

Explanation:
All the users registered in contests 208, 209, and 210, so the
percentage is 100%. Users 6 and 8 registered in contest 215, so the
percentage is ((2/3) * 100) = 66.67%. User 2 registered in contest 207,
so the percentage is ((1/3) * 100) = 33.33%.
*/

SELECT
    contest_id,
    ROUND(
        COUNT(DISTINCT user_id) * 100.0 / (SELECT COUNT(*) FROM Users),
        2
    ) AS percentage
FROM Register
GROUP BY contest_id
ORDER BY percentage DESC, contest_id ASC;

/*
Observation:
- The denominator (total number of users) is constant across every
  group, so it's computed once with a scalar subquery
  (SELECT COUNT(*) FROM Users) rather than via a join - a join would
  needlessly multiply rows and complicate the aggregation.
- COUNT(DISTINCT user_id) counts how many unique users registered for
  each contest_id. DISTINCT is technically redundant here since
  (contest_id, user_id) is already a primary key on Register (no
  duplicate rows possible per contest), but it's good defensive
  practice for this kind of "count participants" pattern.
- Multiplying by 100.0 (not 100) forces floating-point/decimal division
  instead of integer division, which matters in dialects like MySQL
  where COUNT(...) * 100 / COUNT(...) could otherwise truncate.
- ROUND(..., 2) satisfies the "rounded to two decimals" requirement.
- ORDER BY percentage DESC, contest_id ASC implements the tie-breaking
  rule directly: primary sort descending by percentage, secondary sort
  ascending by contest_id for ties (e.g. the three 100% contests come
  back in contest_id order 208, 209, 210).
*/
