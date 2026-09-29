/*
LeetCode 1193 - Monthly Transactions I
URL: https://leetcode.com/problems/monthly-transactions-i/

Table: Transactions
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| id            | int     |
| country       | varchar |
| state         | enum    |
| amount        | int     |
| trans_date    | date    |
+---------------+---------+
id is the primary key (column with unique values) for this table.
state is an ENUM (category) of type ('approved', 'declined'). Each row
contains information about a single transaction: the country it was made
in, its state, its amount, and the date it took place.

Task:
Write a solution to find, for each month and country, the number of
transactions and their total amount, the number of approved transactions
and their total amount.
Return the result table in any order.

Example 1:
Input:
Transactions table:
+------+---------+----------+--------+------------+
| id   | country | state    | amount | trans_date |
+------+---------+----------+--------+------------+
| 121  | US      | approved | 1000   | 2018-12-18 |
| 122  | US      | declined | 2000   | 2018-12-19 |
| 123  | US      | approved | 2000   | 2019-01-01 |
| 124  | DE      | approved | 2000   | 2019-01-07 |
+------+---------+----------+--------+------------+

Output:
+----------+---------+-------------+----------------+---------------------+------------------------+
| month    | country | trans_count | approved_count | trans_total_amount  | approved_total_amount  |
+----------+---------+-------------+----------------+---------------------+------------------------+
| 2018-12  | US      | 2           | 1              | 3000                | 1000                   |
| 2019-01  | US      | 1           | 1              | 2000                | 2000                   |
| 2019-01  | DE      | 1           | 1              | 2000                | 2000                   |
+----------+---------+-------------+----------------+---------------------+------------------------+
*/

SELECT
    DATE_FORMAT(trans_date, '%Y-%m') AS month,
    country,
    COUNT(*) AS trans_count,
    SUM(CASE WHEN state = 'approved' THEN 1 ELSE 0 END) AS approved_count,
    SUM(amount) AS trans_total_amount,
    SUM(CASE WHEN state = 'approved' THEN amount ELSE 0 END) AS approved_total_amount
FROM Transactions
GROUP BY month, country;

/*
Observation:
- The grouping key is a composite of (month, country), not just one of
  them, since the required breakdown is per month AND per country - two
  rows with the same country but different months (like the two US rows
  in Dec 2018 vs Jan 2019) must land in separate groups.
- DATE_FORMAT(trans_date, '%Y-%m') collapses a full date down to a
  year-month bucket that becomes both a SELECT column and part of the
  GROUP BY key; aliasing it as `month` lets it be reused in GROUP BY by
  name in dialects that support it (MySQL does; some dialects require
  repeating the expression instead of the alias).
- COUNT(*) / SUM(amount) give the "all transactions" totals per group,
  while the approved-only totals reuse the same
  SUM(CASE WHEN state = 'approved' THEN ... ELSE 0 END) conditional
  pattern seen in earlier problems (e.g. confirmation rate) - counting
  or summing only rows matching a condition inside an aggregate, without
  needing a separate query or a WHERE filter that would drop the
  non-approved rows needed for the "total" columns.
- Because state only has two possible values, `ELSE 0` for the approved
  count is equivalent to `WHEN state = 'declined' THEN 0`; this pattern
  generalizes to more states without changing the ELSE branch.
*/
