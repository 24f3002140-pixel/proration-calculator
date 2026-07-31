PRORATION CALCULATOR API

Endpoint:
POST /charge

Example request:
{
  "old_price": 19,
  "new_price": 39,
  "days_remaining": 19,
  "days_in_actual_month": 30,
  "spec": "v2"
}

Example response:
{
  "charge": 12.666666666666666
}
