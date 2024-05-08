-- sql script that ranks country origins of bands
-- ordered by the number of non-unique fans

-- query to select the origin column from metal_bands and calc the sum of fans column for each origin
SELECT origin, SUM(fans) AS nb_fans
-- specify table where we recieve data
FROM metal_bands
-- group the results by the origin column so that the SUM() function is applied to each of the grp of rows with same origin
GROUP BY origin
-- we order the results in descending order based on the total num of fans (nb_fans)
ORDER BY nb_fans DESC;

