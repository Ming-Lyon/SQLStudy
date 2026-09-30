SELECT
    c.noagent,
    c.horaire_paie,
    i.entree_organisme,
	i.libelle_du_contrat
FROM caleagt c
INNER JOIN info_agt i
    ON c.noagent = i.noagent
WHERE EXISTS (
    SELECT 1
    FROM paibasemensf p
    WHERE p.noagt = c.noagent
      AND p.regle_assujettissement = 'VACJH-Vacataires'
)
ORDER BY c.noagent;