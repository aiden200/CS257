SELECT nocs.noc_name 
FROM nocs
ORDER BY nocs.noc_name;

SELECT athletes.full_name, nocs.noc_name
FROM athletes, nocs, athletes_nocs
WHERE athletes.id = athletes_nocs.athlete_id
AND nocs.id = athletes_nocs.noc_id
AND nocs.region = 'Kenya';

SELECT games.games, events.event_name, medals.medal
FROM games, events, medals, athletes
WHERE athletes.id = medals.athlete_id
AND games.id = medals.game_id
AND events.id = medals.event_id
AND athletes.full_name LIKE '%Greg%%Louganis%'
ORDER BY games.game_year;

SELECT nocs.noc_name, COUNT(medals.medal)
FROM nocs, athletes, medals, athletes_nocs
WHERE athletes.id = medals.athlete_id
AND athletes.id = athletes_nocs.athlete_id
AND nocs.id = athletes_nocs.noc_id
AND medals.medal = 'Gold'
GROUP BY nocs.noc_name
ORDER BY COUNT(medals.medal) DESC