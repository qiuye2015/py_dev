sourceHost="127.0.0.1"
sourcePort=13306
archiveUser="root"
archivePwd=123456
sourceDb="test"
#sourceTable="db_test"
sourceTable="db_test_copy"
archiveCondition="1=1"

destHost="127.0.0.1"
destPort=13306
destDb="test"
#destTable="db_test_copy"
destTable="db_test"


batchSize=1000
txnSize=500

#charset="UTF8"
charset="utf8mb4"
archiveModeEnum="--bulk-delete"


#${ptArchiverPath}/
pt-archiver \
--source h=${sourceHost},P=${sourcePort},u=${archiveUser},p=${archivePwd},D=${sourceDb},t=${sourceTable} \
--dest h=${destHost},P=${destPort},u=${archiveUser},p=${archivePwd},D=${destDb},t=${destTable} \
--progress ${batchSize}  \
--where "${archiveCondition}"  \
--statistics  \
--charset=${charset}  \
--limit=${batchSize}  \
--txn-size ${txnSize}  \
--no-delete \
${archiveModeEnum}  \
--replace ${extensionCmd}