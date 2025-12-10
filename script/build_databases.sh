# cd 项目目录 :
# bash "./script/build_databases.sh"

export DATABASES_PASSWORD="asdasdasd"
export USER_NAME="root"
export DATABASES_NAME="graduation"


mysql -u root -p${DATABASES_PASSWORD} << EOF

CREATE DATABASE IF NOT EXISTS ${DATABASES_NAME};

use ${DATABASES_NAME};


EOF

mysql -u ${USER_NAME} -p${DATABASES_PASSWORD} -D${DATABASES_NAME} < "./script.sql"