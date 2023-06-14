#!/bin/bash
abort() {
    printf "%s\n" "$@"
    exit 1
}

ACAI_CURRENT=(
    'router.route()'
    'requiredParams'
    'request.params'
    'event.records'
    'approximateCreationDateTime'
    'awsRegion'
    'eventID'
    'eventName'
    'eventSource'
    'eventSourceARN'
    'streamViewType'
    'sizeBytes'
    'userIdentity'
    'timeToLiveExpired'
    'requestParameters'
    'responseElements'
    's3SchemaVersion'
    'messageId'
    'rawBody'
)
ALC_UPGRADE=(
    'router.route(event)'
    'requiredQuery'
    'request.query'
    'await event.getRecords()'
    'created'
    'region'
    'id'
    'name'
    'source'
    'sourceARN'
    'streamType'
    'size'
    'identity'
    'expired'
    'request'
    'response'
    'version'
    'id'
    'raw'
)

echo '================================='
echo 'Upgrading ALC Node v1.x to v2.x 🤓'
echo '================================='

read -r -p 'Do you want to upgrade your NODE project from ALC 1.x to 2.x? [y/N] ' UPGRADE_RESPONSE
if [[ ! "$UPGRADE_RESPONSE" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    abort 'Come back when you are ready...'
fi
read -r -p 'Have you created a clean branch to make these changes on? [y/N] ' BRANCH_RESPONSE
if [[ ! "$BRANCH_RESPONSE" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    abort 'Please make a clean branch and come back when you are ready...'
fi

PWD=$(pwd)
echo "Current directory: ${PWD}"
read -r -p 'Is the above currently the root of your project directory? [y/N] ' DIRECTORY_RESPONSE

if [[ ! "$DIRECTORY_RESPONSE" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    abort 'Please navigate to the root of directory of your project and try again...'
fi

read -r -p 'Please enter the relative path of your code from this current directory (no starting slash): ' CODE_RESPONSE

APP_FILES=$(find "$CODE_RESPONSE" -type f -name "*.js")
for FILE in $APP_FILES; do
    echo "Upgrading file: ${FILE}";
    # shellcheck disable=SC2068
    for i in ${!ACAI_CURRENT[@]}; do
        OLD=${ACAI_CURRENT[$i]}
        NEW=${ALC_UPGRADE[$i]}
        echo "Replacing: ${OLD} with ${NEW}"
        sed -n "s/${OLD}/${NEW}/g" "${FILE}"
    done
    echo "Done with file: ${FILE}"
done

echo ''
echo 'Please make sure to check & review each file INDIVIDUALLY before creating a PR and submitting these changes.'
echo ''
echo 'If you have any issues, or concerns please reach create a issue here: https://github.com/syngenta-digital/package-node-alc/issues'
echo ''
echo 'Thank you for using the ALC!!!'
