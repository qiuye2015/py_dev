# ./bin/flink run -py mysql2es.py -d
# ./bin/flink run -py mongo2es.py -d

# ./bin/flink run --target local --jobmanager 127.0.0.1:8081 --python examples/python/table/word_count.py
# ./bin/flink run --python mongo2es.py
./bin/flink run -py mysql2es.py
