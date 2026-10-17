
# ModelRoute Logging Schema

## 1. Purpose

This document defines the structured logging format for ModelRoute.
Logs help us debug requests, track routing decisions, monitor latency,
measure token usage, and investigate failures.

## 2. Schema Version

Version: 1.0

## 3. Common Log Fields

| Field | Type | Required | Description |
|---|---|---|---|
| schema_version | string | Yes | Logging schema version |
| timestamp | ISO 8601 datetime | Yes | Time of the event in UTC |
| request_id | string | Yes | Unique identifier for a request |
| event_type | string | Yes | Type of event |
| selected_model | string or null | No | Model selected by the router |
| provider | string or null | No | Model provider |
| latency_ms | number or null | No | Duration in milliseconds |
| input_tokens | integer or null | No | Input tokens used |
| output_tokens | integer or null | No | Output tokens generated |
| estimated_cost_usd | number or null | No | Estimated request cost |
| cache_status | string or null | No | Cache hit, miss, or bypass |
| retry_count | integer | Yes | Number of retries |
| fallback_used | boolean | Yes | Whether fallback was used |
| status | string | Yes | success, error, or in_progress |
| error_code | string or null | No | Standardized error identifier |

## 4. Event Types

- request_received
- routing_decision
- cache_lookup
- provider_call_started
- provider_call_completed
- fallback_triggered
- request_completed
- request_failed

## 5. Example Log Record

```json
{
  "schema_version": "1.0",
  "timestamp": "2026-10-17T09:30:00Z",
  "request_id": "req_example_001",
  "event_type": "request_completed",
  "selected_model": "example-model",
  "provider": null,
  "latency_ms": 450.5,
  "input_tokens": 120,
  "output_tokens": 80,
  "estimated_cost_usd": null,
  "cache_status": "miss",
  "retry_count": 0,
  "fallback_used": false,
  "status": "success",
  "error_code": null
}
```

The values above are illustrative.

## 6. Logging Rules

- Use UTC timestamps in ISO 8601 format.
- Reuse the same request_id across events belonging to one request.
- Keep field names and data types consistent.
- Use null when a value is unavailable.
- Never log API keys, access tokens, or authorization headers.
- Avoid logging sensitive personal data or full prompts by default.
- Record failures with standardized error codes.
- Do not include request IDs or user-specific data as Prometheus labels.

## 7. Validation

The implementation must validate log records and test successful requests,
failed requests, retries, fallback routing, and cache behavior.

## 8. Monitoring Integration

Structured logs are used for debugging.
Langfuse can be used for LLM traces and generation details.
Prometheus collects aggregate metrics, and Grafana visualizes them.
