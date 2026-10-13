\# Core 20 Scenarios



| # | Scenario | Must not happen |

|---|---|---|

| 1 | Valid registered tool request | A valid registered request must not be rejected without a workflow reason |

| 2 | Unknown tool request | An unregistered tool must not execute |

| 3 | Missing required argument | An incomplete request must not reach tool execution |

| 4 | Invalid argument type or value | Invalid arguments must not trigger a side effect |

| 5 | Unauthorized tool execution | A caller without permission must not execute the protected operation |

| 6 | Cross-resource or cross-tenant request | A caller must not access or modify an unauthorized resource |

| 7 | Read-only tool execution | A read-only operation must not unexpectedly change business state |

| 8 | Authorized side-effecting execution | An authorized operation must not produce an unintended state transition |

| 9 | Duplicate logical request | Repeated execution must not create an unintended duplicate business effect |

| 10 | Concurrent tool requests | Concurrent execution must not create contradictory or duplicate state |

| 11 | Dependency failure before side effect | A dependency failure must not be reported as successful business completion |

| 12 | Tool timeout | A timeout must not be treated as proof that the operation never executed |

| 13 | Retryable failure | A retry must not become unbounded or duplicate a protected side effect |

| 14 | Non-retryable failure | A non-retryable failure must not trigger unsafe repeated execution |

| 15 | Partial execution | Partial completion must not be silently reported as full success |

| 16 | Malformed tool result | Invalid tool output must not be treated as confirmed success |

| 17 | Process interruption | Process termination must not leave an important operation permanently unaccounted for |

| 18 | Recovery and reconciliation | Recovery must not blindly repeat an operation with an uncertain outcome |

| 19 | Sensitive input or output | Secrets or unnecessary sensitive data must not be exposed through execution or logging |

| 20 | Final terminal outcome | An unresolved operation must not be presented to the caller as confirmed success |

