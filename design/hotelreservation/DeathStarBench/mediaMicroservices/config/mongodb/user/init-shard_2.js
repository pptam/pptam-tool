rs.initiate(
{
  "_id": "user-mongodb-shard-2",
  "version": 1,
  "members": [
    {
      "_id": 1,
      "host": "user-mongodb-shard-2_1:27017"
    },
    {
      "_id": 2,
      "host": "user-mongodb-shard-2_2:27017"
    }
  ]
}
)