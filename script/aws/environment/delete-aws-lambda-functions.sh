aws lambda list-functions --region eu-west-1 | jq -r '.Functions | .[] | .FunctionName' |
while read uname1; do
echo "Deleting $uname1";
$(aws lambda delete-function --region eu-west-1 --function-name $uname1);
done