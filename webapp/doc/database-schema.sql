DROP TABLE IF EXISTS vaccinations_region;
DROP TABLE IF EXISTS case_date;
DROP TABLE IF EXISTS vaccinations_in_US;


CREATE TABLE vaccinations_region(
	region text,
	vaccination int
);
CREATE TABLE case_date(
	state text,
	date text,
	case integer
);

CREATE TABLE cases_in_US(
	state text,
	cases int
);


