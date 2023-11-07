sourceHost="127.0.0.1"
sourcePort=13306
archiveUser="root"
archivePwd=123456
sourceDb="test"
sourceTable="db_test"
archiveCondition="1=1"

batchSize=20000
txnSize=1000

#charset="UTF8"
charset="utf8mb4"
archiveModeEnum="--purge"


#${ptArchiverPath}/
pt-archiver \
--source h=${sourceHost},P=${sourcePort},u=${archiveUser},p=${archivePwd},D=${sourceDb},t=${sourceTable} \
--where "${archiveCondition}"  \
--limit=${batchSize} \
--txn-size ${txnSize} \
--progress ${batchSize}  \
--charset=${charset} \
--file "${archiveFilePath}/%D-%t-%Y-%m-%d-%H-%i-%s" \
${extensionCmd}
