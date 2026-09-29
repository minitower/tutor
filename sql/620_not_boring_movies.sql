/*
LeetCode 620 - Not Boring Movies
URL: https://leetcode.com/problems/not-boring-movies/

Table: Cinema
+----------------+---------+
| Column Name    | Type    |
+----------------+---------+
| id             | int     |
| movie          | varchar |
| description    | varchar |
| rating         | float   |
+----------------+---------+
id is the primary key (column with unique values) for this table.
Each row contains information about the name of a movie, its class, its
description, and its rating. id is an auto-increment column starting
from 1.

Task:
Write a solution to report the movies with an odd-numbered ID and a
description that is not "boring".
Return the result table ordered by rating in descending order.

Example 1:
Input:
Cinema table:
+----+------------+-------------+--------+
| id | movie      | description | rating |
+----+------------+-------------+--------+
| 1  | War        | great 3D    | 8.9    |
| 2  | Science    | fiction     | 8.5    |
| 3  | irish      | boring      | 6.2    |
| 4  | Ice song   | Fantacy     | 8.6    |
| 5  | House card | Interesting | 9.1    |
+----+------------+-------------+--------+

Output:
+----+------------+-------------+--------+
| id | movie      | description | rating |
+----+------------+-------------+--------+
| 5  | House card | Interesting | 9.1    |
| 1  | War        | great 3D    | 8.9    |
+----+------------+-------------+--------+
*/

SELECT *
FROM Cinema
WHERE id % 2 = 1
  AND description <> 'boring'
ORDER BY rating DESC;

/*
Observation:
- `id % 2 = 1` is the standard way to filter odd-numbered ids; since id
  is an auto-increment integer primary key, the modulo operator works
  reliably here without needing to worry about NULLs or non-integer
  values.
- `description <> 'boring'` excludes exactly the rows whose description
  literally equals "boring" (row id 3 in the example) - it's a plain
  string inequality, not a pattern match, so descriptions merely
  containing the word "boring" elsewhere would still pass (not an issue
  with this dataset).
- Both conditions are combined with AND directly in the WHERE clause
  since this is a simple row-level filter with no aggregation needed -
  no GROUP BY/HAVING or joins required.
- ORDER BY rating DESC satisfies the required output ordering; row id 2
  (even) and row id 4 (even) and row id 3 (boring) are all filtered out,
  leaving ids 1 and 5, sorted 9.1 before 8.9.
*/
