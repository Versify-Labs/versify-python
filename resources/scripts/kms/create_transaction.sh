curl --request POST \
  --url https://api-eu1.tatum.io/v3/polygon/transaction \
  --header 'Content-Type: application/json' \
  --header 'x-api-key: API_KEY' \
  --data '{
  "data": "My note to recipient.",
  "nonce": 0,
  "to": "0x5b0f1E51B45752e96373791a403C33749abF0e07",
  "currency": "MATIC",
  "fee": {
    "gasLimit": "40000",
    "gasPrice": "20"
  },
  "amount": ".00001",
  "signatureId": "f78458f8-1124-4045-a716-6b32666f3470"
}'
