/*
LeetCode 570 - Managers with at Least 5 Direct Reports
URL: https://leetcode.com/problems/managers-with-at-least-5-direct-reports

Table: Employee
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| name        | varchar |
| department  | varchar |
| managerId   | int     |
+-------------+---------+
id is the primary key (column with unique values) for this table.
Each row indicates the name of an employee, their department, and the id
of their manager. If managerId is null, the employee has no manager.
No employee is the manager of themself.

Task:
Write a solution to find managers with at least five direct reports.
Return the result table in any order.

Example 1:
Input:
Employee table:
+-----+-------+------------+-----------+
| id  | name  | department | managerId |
+-----+-------+------------+-----------+
| 101 | John  | A          | null      |
| 102 | Dan   | A          | 101       |
| 103 | James | A          | 101       |
| 104 | Amy   | A          | 101       |
| 105 | Anne  | A          | 101       |
| 106 | Ron   | B          | 101       |
+-----+-------+------------+-----------+

Output:
+------+
| name |
+------+
| John |
+------+
*/

SELECT e.name
FROM Employee e
JOIN Employee r ON r.managerId = e.id
GROUP BY e.id, e.name
HAVING COUNT(r.id) >= 5;

/*
Observation:
- A self-join on Employee is needed: the outer alias (e) represents the
  candidate manager, the inner alias (r) represents rows whose managerId
  points back to that manager - i.e. their direct reports.
- Grouping by e.id (not just e.name) is important in case two different
  managers happen to share the same name; grouping only by name could
  incorrectly merge their report counts.
- HAVING COUNT(r.id) >= 5 filters groups after aggregation, keeping only
  managers with 5 or more direct reports - this can't be done with WHERE
  since WHERE runs before aggregation.
- Employees with managerId = null are simply never matched as r in the
  join, so they naturally don't affect the count for anyone.
*/
