#!/usr/bin/env bash
# Quick smoke test against the live HDX DataStore API.
# Usage: HDX_API_KEY=<your-key> bash test.sh
#    or: export HDX_API_KEY=<your-key> && bash test.sh

set -e

BASE="https://data.humdata.org/api/3/action"
RESOURCE="e3a18c4c-ec1b-457e-9f60-cee283c04e0c"

if [[ -z "$HDX_API_KEY" ]]; then
  echo "Error: HDX_API_KEY is not set."
  echo "Usage: HDX_API_KEY=<your-key> bash test.sh"
  exit 1
fi

echo "==> datastore_search (limit 2)"
curl -s -H "Authorization: $HDX_API_KEY" \
  "$BASE/datastore_search?resource_id=$RESOURCE&limit=2" \
  | python3 -m json.tool --indent 2 | head -40

echo ""
echo "==> datastore_info"
curl -s -H "Authorization: $HDX_API_KEY" \
  "$BASE/datastore_info?resource_id=$RESOURCE" \
  | python3 -m json.tool --indent 2 | head -40

echo ""
echo "==> datastore_search_sql"
curl -s -H "Authorization: $HDX_API_KEY" -G \
  --data-urlencode "sql=SELECT * FROM \"$RESOURCE\" LIMIT 2" \
  "$BASE/datastore_search_sql" \
  | python3 -m json.tool --indent 2 | head -40
