-- 10w
CREATE TABLE 100k_row_test(
	`id` int NOT NULL AUTO_INCREMENT,
	`person_id` int NOT NULL,
	`person_name` VARCHAR(200),
	`insert_time` int,
	`update_time` int,
    PRIMARY KEY (`id`),
    KEY `query_by_update_time` (`update_time`),
    KEY `query_by_person_id_insert_time` (`insert_time`)
);

CREATE TABLE 200k_row_test(
	`id` int NOT NULL AUTO_INCREMENT,
	`person_id` int NOT NULL,
	`person_name` VARCHAR(200),
	`insert_time` int,
	`update_time` int,
    PRIMARY KEY (`id`),
    KEY `query_by_update_time` (`update_time`),
    KEY `query_by_person_id_insert_time` (`insert_time`)
);

CREATE TABLE 500k_row_test(
	`id` int NOT NULL AUTO_INCREMENT,
	`person_id` int NOT NULL,
	`person_name` VARCHAR(200),
	`insert_time` int,
	`update_time` int,
    PRIMARY KEY (`id`),
    KEY `query_by_update_time` (`update_time`),
    KEY `query_by_person_id_insert_time` (`insert_time`)
);

-- 100w
CREATE TABLE 1m_row_test(
	`id` int NOT NULL AUTO_INCREMENT,
	`person_id` int NOT NULL,
	`person_name` VARCHAR(200),
	`insert_time` int,
	`update_time` int,
    PRIMARY KEY (`id`),
    KEY `query_by_update_time` (`update_time`),
    KEY `query_by_person_id_insert_time` (`insert_time`)
);

CREATE TABLE 2m_row_test(
	`id` int NOT NULL AUTO_INCREMENT,
	`person_id` int NOT NULL,
	`person_name` VARCHAR(200),
	`insert_time` int,
	`update_time` int,
    PRIMARY KEY (`id`),
    KEY `query_by_update_time` (`update_time`),
    KEY `query_by_person_id_insert_time` (`insert_time`)
);

CREATE TABLE 5m_row_test(
	`id` int NOT NULL AUTO_INCREMENT,
	`person_id` int NOT NULL,
	`person_name` VARCHAR(200),
	`insert_time` int,
	`update_time` int,
    PRIMARY KEY (`id`),
    KEY `query_by_update_time` (`update_time`),
    KEY `query_by_person_id_insert_time` (`insert_time`)
);

-- 1000w
CREATE TABLE 10m_row_test(
	`id` int NOT NULL AUTO_INCREMENT,
	`person_id` int NOT NULL,
	`person_name` VARCHAR(200),
	`insert_time` int,
	`update_time` int,
    PRIMARY KEY (`id`),
    KEY `query_by_update_time` (`update_time`),
    KEY `query_by_person_id_insert_time` (`insert_time`)
);

CREATE TABLE 20m_row_test(
	`id` int NOT NULL AUTO_INCREMENT,
	`person_id` int NOT NULL,
	`person_name` VARCHAR(200),
	`insert_time` int,
	`update_time` int,
    PRIMARY KEY (`id`),
    KEY `query_by_update_time` (`update_time`),
    KEY `query_by_person_id_insert_time` (`insert_time`)
);

CREATE TABLE 30m_row_test(
	`id` int NOT NULL AUTO_INCREMENT,
	`person_id` int NOT NULL,
	`person_name` VARCHAR(200),
	`insert_time` int,
	`update_time` int,
    PRIMARY KEY (`id`),
    KEY `query_by_update_time` (`update_time`),
    KEY `query_by_person_id_insert_time` (`insert_time`)
);

CREATE TABLE 50m_row_test(
	`id` int NOT NULL AUTO_INCREMENT,
	`person_id` int NOT NULL,
	`person_name` VARCHAR(200),
	`insert_time` int,
	`update_time` int,
    PRIMARY KEY (`id`),
    KEY `query_by_update_time` (`update_time`),
    KEY `query_by_person_id_insert_time` (`insert_time`)
);

CREATE TABLE 80m_row_test(
	`id` int NOT NULL AUTO_INCREMENT,
	`person_id` int NOT NULL,
	`person_name` VARCHAR(200),
	`insert_time` int,
	`update_time` int,
    PRIMARY KEY (`id`),
    KEY `query_by_update_time` (`update_time`),
    KEY `query_by_person_id_insert_time` (`insert_time`)
);