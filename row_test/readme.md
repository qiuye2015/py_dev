```bash
# insert
py insert_data.py 50m 5000000

create table 80m_row_test like 50m_row_test
insert into 80m_row_test (`person_id`, `person_name`, `insert_time`, `update_time`)
select `person_id`, `person_name`, `insert_time`, `update_time` from 10m_row_test

# select
python select_data.py 50m 20 1

# get buffer pool info
SHOW ENGINE INNODB STATUS
SHOW STATUS LIKE 'innodb_buffer_pool_page%'
```
