DROP TABLE IF EXISTS ;
DROP TABLE IF EXISTS case_date;
DROP TABLE IF EXISTS covid_history;
DROP TABLE IF EXISTS vaccinations_in_US;


CREATE TABLE (
	current_date text,
	case int
);

CREATE TABLE case_date(
	state text,
	case int
);

CREATE TABLE covid_history(
	
);

CREATE TABLE vaccinations_in_US(
	state text,
	vaccinations int
);
