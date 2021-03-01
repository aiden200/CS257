DROP TABLE IF EXISTS vaccinations_region;
DROP TABLE IF EXISTS case_date;
DROP TABLE IF EXISTS vaccinations_in_US;


CREATE TABLE vaccinations_region(
	region text,
	people_with_1_or_more_doses integer,
	people_with_1_or_more_doses_per_100K integer,
	people_with_2_doses integer,
	people_with_2_doses_per_100K integer,
);

CREATE TABLE cases_date(
	states text,
	day date,
	cases integer,
	cases_increased integer
);

CREATE TABLE cases_and_vaccination_in_US(
	states text,
	cases integer,
	cases_increased integer,
	vaccination integer
);
