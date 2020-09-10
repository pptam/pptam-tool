#!/usr/bin/env python
from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate a Token from the "Tokens Tab" in the UI
token = "pptam"
org = "pptam"
bucket = "pptam"

client = InfluxDBClient(url="http://localhost:9999", token=token)

write_api = client.write_api(write_options=SYNCHRONOUS)
write_api.write(bucket, org, ["mem,host=host1 used_percent=50"])
