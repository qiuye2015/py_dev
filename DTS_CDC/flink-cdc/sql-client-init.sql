SET "execution.checkpointing.interval" = "4s";
SET "table.local-time-zone" = "Asia/Shanghai";
SET "sql-client.execution.result-mode" = "tableau";
SET "pipeline.name"= 'adw-to-es';
CREATE CATALOG fjp_catalog WITH(
    'type' = 'jdbc',
    'default-database' = 'mydb',
    'username' = 'root',
    'password' = '123456',
    'base-url' = 'jdbc:mysql://127.0.0.1:33065'
);
