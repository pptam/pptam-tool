import grpc
import time
from datetime import datetime, timedelta

from proto.api_v2 import query_pb2, query_pb2_grpc
from google.protobuf.timestamp_pb2 import Timestamp

def get_epoch_nanos(dt):
    """Converts a datetime object to epoch nanoseconds."""
    return int(dt.timestamp() * 1e9)

def main():
    # Connect to the Jaeger gRPC endpoint
    channel = grpc.insecure_channel("jaeger-query:16685")
    client = query_pb2_grpc.QueryServiceStub(channel)

    # Define time range: last hour
    now = datetime.utcnow()
    one_hour_ago = now - timedelta(hours=1)

    # Build the request
    request = query_pb2.GetTraceSummariesRequest(
        start_time=get_epoch_nanos(one_hour_ago),
        end_time=get_epoch_nanos(now),
        num_traces=20  # You can increase this as needed
    )

    response = client.GetTraceSummaries(request)

    print(f"Found {len(response.trace_summaries)} trace summaries")

    # Download full traces
    for summary in response.trace_summaries:
        trace_id = summary.trace_id
        trace_request = query_pb2.GetTraceRequest(trace_id=trace_id)
        trace = client.GetTrace(trace_request)
        print(f"\nTrace ID: {trace_id}")
        for span in trace.trace.spans:
            print(f"  Span: {span.operation_name}, Start Time: {span.start_time}")

if __name__ == "__main__":
    main()
