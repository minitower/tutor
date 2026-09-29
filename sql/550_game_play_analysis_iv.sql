/*
LeetCode 550 - Game Play Analysis IV
URL: https://leetcode.com/problems/game-play-analysis-iv/

Table: Activity
+--------------+---------+
| Column Name  | Type    |
+--------------+---------+
| player_id    | int     |
| device_id    | int     |
| event_date   | date    |
| games_played | int     |
+--------------+---------+
(player_id, event_date) is the primary key (combination of columns with
unique values) for this table. Each row is a record of a player who
logged in and played a number of games (possibly 0) on some date using
some device.

Task:
Write a solution to report the fraction of players that logged in again
on the day after the day they first logged in, rounded to 2 decimals.
In other words, determine the number of players who logged in on the
day immediately following their first login date, divided by the total
number of players.

Example 1:
Input:
Activity table:
+-----------+-----------+------------+--------------+
| player_id | device_id | event_date | games_played |
+-----------+-----------+------------+--------------+
| 1         | 2         | 2016-03-01 | 5            |
| 1         | 2         | 2016-03-02 | 6            |
| 2         | 3         | 2017-06-25 | 1            |
| 3         | 1         | 2016-03-02 | 0            |
| 3         | 4         | 2018-07-03 | 5            |
+-----------+-----------+------------+--------------+

Output:
+----------+
| fraction |
+----------+
| 0.33     |
+----------+

Explanation:
Player 1 first logged in on 2016-03-01 and logged in again the next day
(2016-03-02), so player 1 counts. Player 2 only has one login record, so
there's no "next day" to check. Player 3 first logged in on 2016-03-02,
but their only other record is 2018-07-03 (not the immediate next day),
so player 3 doesn't count. 1 out of 3 players counts -> 1/3 = 0.33.
*/

WITH first_login AS (
    SELECT
        player_id,
        MIN(event_date) AS first_date
    FROM Activity
    GROUP BY player_id
)
SELECT
    ROUND(
        COUNT(DISTINCT a.player_id) * 1.0 / (SELECT COUNT(*) FROM first_login),
        2
    ) AS fraction
FROM Activity a
JOIN first_login f
  ON a.player_id = f.player_id
 AND a.event_date = DATE_ADD(f.first_date, INTERVAL 1 DAY);

/*
Observation:
- This needs each player's first login date before anything else can be
  checked, so a CTE (first_login) computes MIN(event_date) grouped by
  player_id - a classic "find the earliest row per group" step that
  gets reused, so it's pulled out rather than repeated inline.
- The main query then re-joins Activity back to first_login, but instead
  of just matching on player_id, it also requires
  a.event_date = DATE_ADD(f.first_date, INTERVAL 1 DAY) - this is what
  captures "logged in on the day immediately after their first login."
  Only players with an actual activity row on that exact next day
  survive the join (player 1 in the example; player 3 does not, since
  their next record is over two years later, not the next day).
- The denominator is the total player count, taken as
  (SELECT COUNT(*) FROM first_login) - equivalent to counting distinct
  players in Activity, but reusing the CTE avoids a second GROUP BY.
- COUNT(DISTINCT a.player_id) in the numerator guards against
  double-counting in case a player could otherwise match the join
  condition more than once (not possible here since (player_id,
  event_date) is unique, but it's a safe habit for this pattern).
- Multiplying by 1.0 before dividing forces non-integer division so the
  ROUND produces a proper decimal like 0.33 rather than risking integer
  truncation in dialects where / on two integers floors the result.
*/
