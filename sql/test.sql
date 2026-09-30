SELECT
    c.name,
    c.country,
    o.noOrder
FROM clients c
INNER JOIN orders o
    ON c.noClient = o.noClient
ORDER BY c.name;