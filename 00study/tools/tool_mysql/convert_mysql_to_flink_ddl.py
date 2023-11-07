import re

def convert_mysql_to_flink_ddl(mysql_ddl):
    flink_ddl = ""

    # Remove backticks
    mysql_ddl = mysql_ddl.replace("`", "")

    # Extract table name
    table_name_match = re.search(r"CREATE TABLE (\w+)", mysql_ddl)
    if table_name_match:
        table_name = table_name_match.group(1)
        flink_ddl += f"CREATE TABLE {table_name} (\n"

        # Extract column definitions
        column_defs = re.findall(r"(\w+)\s+(.*?)\s+(NOT NULL)?(?: DEFAULT .*?)?(?: COMMENT '.*?')?,?", mysql_ddl)
        for column_def in column_defs:
            column_name = column_def[0]
            column_type = column_def[1]
            flink_ddl += f"  {column_name} {column_type}"
            if column_def[2] is not None:
                flink_ddl += " NOT NULL"
            flink_ddl += ",\n"

        # Extract primary key
        primary_key_match = re.search(r"PRIMARY KEY \((.*?)\)", mysql_ddl)
        if primary_key_match:
            primary_key_columns = primary_key_match.group(1)
            flink_ddl += f"  PRIMARY KEY ({primary_key_columns}),\n"

        # Extract unique keys
        unique_keys_matches = re.findall(r"UNIQUE KEY `\w+` \((.*?)\)", mysql_ddl)
        for unique_key_match in unique_keys_matches:
            unique_key_columns = unique_key_match
            flink_ddl += f"  UNIQUE ({unique_key_columns}),\n"

        flink_ddl = flink_ddl.rstrip(",\n") + "\n)"

    return flink_ddl

# Example usage
mysql_create_table = """
CREATE TABLE `fjp` (
  `id` bigint(20) NOT NULL DEFAULT '0' COMMENT 'id',
  `partition_id` bigint(20) NOT NULL DEFAULT '0' COMMENT 'parition id',
  `rowkey` varchar(100) NOT NULL DEFAULT '' COMMENT 'rowkey',
  `fjp_date` int(11) NOT NULL DEFAULT '0' COMMENT 'meta.date',
  PRIMARY KEY (`id`),
  UNIQUE KEY `rowkey` (`rowkey`),
  KEY `fjp_date` (`fjp_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='keydata' shardkey=fjp_date;
"""

flink_ddl = convert_mysql_to_flink_ddl(mysql_create_table)
print(flink_ddl)
