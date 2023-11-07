sourceHost="127.0.0.1"
sourcePort=13306
archiveUser="root"
archivePwd=123456
sourceDb="test"
sourceTable="db_test"
archiveCondition="1=1"

batchSize=1000
txnSize=500

charset="UTF8"
#charset="utf8mb4"
archiveFilePath="tmp_archive"


#${ptArchiverPath}/
#
pt-archiver \
  --limit=${batchSize} \
  --txn-size ${txnSize} \
  --progress ${batchSize}  \
  --charset=${charset} \
  --no-check-charset \
  --file './%D-%t-%Y-%m-%d-%H-%i-%s' \
  --source h=${sourceHost},P=${sourcePort},u=${archiveUser},p=${archivePwd},D=${sourceDb},t=${sourceTable} \
  --where "${archiveCondition}" \
  --no-delete \
  ${extensionCmd}
