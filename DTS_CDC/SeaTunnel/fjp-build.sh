# Install Subproject Locally
# ./mvnw install -Dmaven.test.skip

# Building seaTunnel from source
mvn clean package -pl seatunnel-dist -am -Dmaven.test.skip=true
# tar xf seatunnel-dist/target/apache-seatunnel-2.3.2-SNAPSHOT-bin.tar.gz
# cd apache-seatunnel-2.3.2-SNAPSHOT/
# ./bin/seatunnel.sh --config ./config/fjp.conf.template  -e local


# Building sub module
# mvn clean package -pl seatunnel-connectors-v2/connector-redis -am -DskipTests -T 1C
