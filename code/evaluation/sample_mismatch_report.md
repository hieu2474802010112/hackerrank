# Public sample mismatch diagnosis

Only dataset/sample_deletion_requests.csv and dataset/sample_output.csv are evaluated. Full output.csv contains different request IDs and is not merged with the public references. Predictions were computed before loading reference answers; no reference labels enter the solver.

## Status mismatches (9)

| Case | Predicted | Expected | Coverage warning |
| --- | --- | --- | --- |
| case_01 | INCOMPLETE | COMPLETE | No identity-linked primary account state |
| case_02 | INCOMPLETE | COMPLETE | No identity-linked primary account state |
| case_04 | INCOMPLETE | COMPLETE | No identity-linked primary account state |
| case_21 | INCOMPLETE | COMPLETE | tombstone_17: ambiguous resource ownership; No identity-linked primary account state |
| case_25 | INCOMPLETE | COMPLETE | No identity-linked primary account state |
| case_26 | INCOMPLETE | COMPLETE | No identity-linked primary account state |
| case_27 | INCOMPLETE | COMPLETE | No identity-linked primary account state |
| case_28 | INCOMPLETE | COMPLETE | No identity-linked primary account state |
| case_31 | INCOMPLETE | COMPLETE | No identity-linked primary account state |

## Correct status, differing steps (14)

case_03, case_07, case_08, case_09, case_10, case_17, case_18, case_20, case_22, case_23, case_24, case_29, case_30, case_32

## Full expected and predicted steps

### case_01 (STATUS_MISMATCH)

Predicted: INCOMPLETE; expected: COMPLETE.

Warnings: No identity-linked primary account state

Expected:
```json
[
  {
    "evidence_id": "evidence_54",
    "operation": "VERIFY_RECORD_ABSENT",
    "phase": "VERIFICATION",
    "resource_id": "account_001",
    "state": "ABSENT",
    "step_no": 1,
    "system_id": "account_service"
  }
]
```

Predicted:
```json
[]
```

### case_02 (STATUS_MISMATCH)

Predicted: INCOMPLETE; expected: COMPLETE.

Warnings: No identity-linked primary account state

Expected:
```json
[
  {
    "evidence_id": "evidence_54",
    "operation": "VERIFY_RECORD_ABSENT",
    "phase": "VERIFICATION",
    "resource_id": "account_002",
    "state": "ABSENT",
    "step_no": 1,
    "system_id": "account_service"
  }
]
```

Predicted:
```json
[]
```

### case_03 (STEPS_ONLY_MISMATCH)

Predicted: COMPLETE; expected: COMPLETE.

Warnings: none

Expected:
```json
[
  {
    "step_no": 1,
    "phase": "VERIFICATION",
    "system_id": "account_service",
    "resource_id": "account_7566",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": "evidence_94"
  },
  {
    "step_no": 2,
    "phase": "VERIFICATION",
    "system_id": "security_service",
    "resource_id": "audit_record_2016",
    "operation": "VERIFY_RECORD_PRESENT",
    "state": "PRESENT",
    "evidence_id": "evidence_94"
  },
  {
    "step_no": 3,
    "phase": "VERIFICATION",
    "system_id": "analytics_platform",
    "resource_id": "analytics_9406",
    "operation": "VERIFY_RECORD_ANONYMIZED",
    "state": "ANONYMIZED",
    "evidence_id": "evidence_94"
  }
]
```

Predicted:
```json
[
  {
    "step_no": 1,
    "phase": "VERIFICATION",
    "system_id": "account_service",
    "resource_id": "account_7566",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": "evidence_94"
  },
  {
    "step_no": 2,
    "phase": "VERIFICATION",
    "system_id": "security_service",
    "resource_id": "audit_record_2016",
    "operation": "VERIFY_RECORD_PRESENT",
    "state": "PRESENT",
    "evidence_id": "evidence_94"
  }
]
```

### case_04 (STATUS_MISMATCH)

Predicted: INCOMPLETE; expected: COMPLETE.

Warnings: No identity-linked primary account state

Expected:
```json
[
  {
    "evidence_id": "evidence_54",
    "operation": "VERIFY_RECORD_ABSENT",
    "phase": "VERIFICATION",
    "resource_id": "account_004",
    "state": "ABSENT",
    "step_no": 1,
    "system_id": "account_service"
  },
  {
    "evidence_id": "evidence_56",
    "operation": "VERIFY_RECORD_ANONYMIZED",
    "phase": "VERIFICATION",
    "resource_id": "analytics_901",
    "state": "ANONYMIZED",
    "step_no": 2,
    "system_id": "analytics_platform"
  }
]
```

Predicted:
```json
[]
```

### case_07 (STEPS_ONLY_MISMATCH)

Predicted: INCOMPLETE; expected: INCOMPLETE.

Warnings: No identity-linked primary account state

Expected:
```json
[
  {
    "evidence_id": "evidence_58",
    "operation": "REPORT_REMAINING_RECORD",
    "phase": "FINDING",
    "resource_id": "support_001",
    "state": "PRESENT",
    "step_no": 1,
    "system_id": "support_platform"
  },
  {
    "evidence_id": "",
    "operation": "DELETE_RECORD",
    "phase": "REMEDIATION",
    "resource_id": "support_001",
    "state": "ABSENT",
    "step_no": 2,
    "system_id": "support_platform"
  },
  {
    "evidence_id": "",
    "operation": "VERIFY_RECORD_ABSENT",
    "phase": "VERIFICATION",
    "resource_id": "account_007",
    "state": "ABSENT",
    "step_no": 3,
    "system_id": "account_service"
  },
  {
    "evidence_id": "",
    "operation": "VERIFY_RECORD_ABSENT",
    "phase": "VERIFICATION",
    "resource_id": "support_001",
    "state": "ABSENT",
    "step_no": 4,
    "system_id": "support_platform"
  }
]
```

Predicted:
```json
[
  {
    "step_no": 1,
    "phase": "FINDING",
    "system_id": "object_storage",
    "resource_id": "object_19",
    "operation": "REPORT_REMAINING_RECORD",
    "state": "PRESENT",
    "evidence_id": "evidence_46"
  },
  {
    "step_no": 2,
    "phase": "FINDING",
    "system_id": "support_platform",
    "resource_id": "support_001",
    "operation": "REPORT_REMAINING_RECORD",
    "state": "PRESENT",
    "evidence_id": "evidence_58"
  },
  {
    "step_no": 3,
    "phase": "REMEDIATION",
    "system_id": "object_storage",
    "resource_id": "object_19",
    "operation": "DELETE_RECORD",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 4,
    "phase": "REMEDIATION",
    "system_id": "support_platform",
    "resource_id": "support_001",
    "operation": "DELETE_RECORD",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 5,
    "phase": "VERIFICATION",
    "system_id": "object_storage",
    "resource_id": "object_19",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 6,
    "phase": "VERIFICATION",
    "system_id": "support_platform",
    "resource_id": "support_001",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": ""
  }
]
```

### case_08 (STEPS_ONLY_MISMATCH)

Predicted: INCOMPLETE; expected: INCOMPLETE.

Warnings: tombstone_17: ambiguous resource ownership; No identity-linked primary account state

Expected:
```json
[
  {
    "evidence_id": "evidence_59",
    "operation": "REPORT_REMAINING_RECORD",
    "phase": "FINDING",
    "resource_id": "export_001",
    "state": "PRESENT",
    "step_no": 1,
    "system_id": "export_service"
  },
  {
    "evidence_id": "",
    "operation": "DELETE_RECORD",
    "phase": "REMEDIATION",
    "resource_id": "export_001",
    "state": "ABSENT",
    "step_no": 2,
    "system_id": "export_service"
  },
  {
    "evidence_id": "",
    "operation": "VERIFY_RECORD_ABSENT",
    "phase": "VERIFICATION",
    "resource_id": "account_008",
    "state": "ABSENT",
    "step_no": 3,
    "system_id": "account_service"
  },
  {
    "evidence_id": "",
    "operation": "VERIFY_RECORD_ABSENT",
    "phase": "VERIFICATION",
    "resource_id": "export_001",
    "state": "ABSENT",
    "step_no": 4,
    "system_id": "export_service"
  }
]
```

Predicted:
```json
[
  {
    "step_no": 1,
    "phase": "FINDING",
    "system_id": "export_service",
    "resource_id": "export_001",
    "operation": "REPORT_REMAINING_RECORD",
    "state": "PRESENT",
    "evidence_id": "evidence_59"
  },
  {
    "step_no": 2,
    "phase": "REMEDIATION",
    "system_id": "export_service",
    "resource_id": "export_001",
    "operation": "DELETE_RECORD",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 3,
    "phase": "VERIFICATION",
    "system_id": "export_service",
    "resource_id": "export_001",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": ""
  }
]
```

### case_09 (STEPS_ONLY_MISMATCH)

Predicted: INCOMPLETE; expected: INCOMPLETE.

Warnings: No identity-linked primary account state

Expected:
```json
[
  {
    "step_no": 1,
    "phase": "FINDING",
    "system_id": "backup_service",
    "resource_id": "backup_4978",
    "operation": "REPORT_RESTORE_RISK",
    "state": "ACTIVE",
    "evidence_id": "evidence_93"
  },
  {
    "step_no": 2,
    "phase": "REMEDIATION",
    "system_id": "backup_service",
    "resource_id": "backup_4978",
    "operation": "BLOCK_RESTORE",
    "state": "BLOCKED",
    "evidence_id": ""
  },
  {
    "step_no": 3,
    "phase": "VERIFICATION",
    "system_id": "account_service",
    "resource_id": "account_3960",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 4,
    "phase": "VERIFICATION",
    "system_id": "security_service",
    "resource_id": "audit_record_4902",
    "operation": "VERIFY_RECORD_PRESENT",
    "state": "PRESENT",
    "evidence_id": ""
  },
  {
    "step_no": 5,
    "phase": "VERIFICATION",
    "system_id": "backup_service",
    "resource_id": "backup_4978",
    "operation": "VERIFY_RESTORE_BLOCKED",
    "state": "BLOCKED",
    "evidence_id": ""
  }
]
```

Predicted:
```json
[
  {
    "step_no": 1,
    "phase": "FINDING",
    "system_id": "backup_service",
    "resource_id": "backup_4978",
    "operation": "REPORT_RESTORE_RISK",
    "state": "ACTIVE",
    "evidence_id": "evidence_93"
  },
  {
    "step_no": 2,
    "phase": "REMEDIATION",
    "system_id": "backup_service",
    "resource_id": "backup_4978",
    "operation": "BLOCK_RESTORE",
    "state": "BLOCKED",
    "evidence_id": ""
  },
  {
    "step_no": 3,
    "phase": "VERIFICATION",
    "system_id": "backup_service",
    "resource_id": "backup_4978",
    "operation": "VERIFY_RESTORE_BLOCKED",
    "state": "BLOCKED",
    "evidence_id": ""
  }
]
```

### case_10 (STEPS_ONLY_MISMATCH)

Predicted: INCOMPLETE; expected: INCOMPLETE.

Warnings: No identity-linked primary account state

Expected:
```json
[
  {
    "evidence_id": "evidence_61",
    "operation": "REPORT_REMAINING_RECORD",
    "phase": "FINDING",
    "resource_id": "support_002",
    "state": "PRESENT",
    "step_no": 1,
    "system_id": "support_platform"
  },
  {
    "evidence_id": "",
    "operation": "DELETE_RECORD",
    "phase": "REMEDIATION",
    "resource_id": "support_002",
    "state": "ABSENT",
    "step_no": 2,
    "system_id": "support_platform"
  },
  {
    "evidence_id": "",
    "operation": "VERIFY_RECORD_ABSENT",
    "phase": "VERIFICATION",
    "resource_id": "account_010",
    "state": "ABSENT",
    "step_no": 3,
    "system_id": "account_service"
  },
  {
    "evidence_id": "",
    "operation": "VERIFY_RECORD_ABSENT",
    "phase": "VERIFICATION",
    "resource_id": "support_002",
    "state": "ABSENT",
    "step_no": 4,
    "system_id": "support_platform"
  }
]
```

Predicted:
```json
[
  {
    "step_no": 1,
    "phase": "FINDING",
    "system_id": "support_platform",
    "resource_id": "support_002",
    "operation": "REPORT_REMAINING_RECORD",
    "state": "PRESENT",
    "evidence_id": "evidence_61"
  },
  {
    "step_no": 2,
    "phase": "REMEDIATION",
    "system_id": "support_platform",
    "resource_id": "support_002",
    "operation": "DELETE_RECORD",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 3,
    "phase": "VERIFICATION",
    "system_id": "support_platform",
    "resource_id": "support_002",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": ""
  }
]
```

### case_17 (STEPS_ONLY_MISMATCH)

Predicted: INCOMPLETE; expected: INCOMPLETE.

Warnings: tombstone_17: ambiguous resource ownership

Expected:
```json
[
  {
    "step_no": 1,
    "phase": "FINDING",
    "system_id": "backup_service",
    "resource_id": "backup_3245",
    "operation": "REPORT_RESTORE_RISK",
    "state": "ACTIVE",
    "evidence_id": "evidence_01"
  },
  {
    "step_no": 2,
    "phase": "REMEDIATION",
    "system_id": "backup_service",
    "resource_id": "backup_3245",
    "operation": "BLOCK_RESTORE",
    "state": "BLOCKED",
    "evidence_id": ""
  },
  {
    "step_no": 3,
    "phase": "VERIFICATION",
    "system_id": "account_service",
    "resource_id": "account_4092",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 4,
    "phase": "VERIFICATION",
    "system_id": "security_service",
    "resource_id": "audit_record_1797",
    "operation": "VERIFY_RECORD_PRESENT",
    "state": "PRESENT",
    "evidence_id": ""
  },
  {
    "step_no": 5,
    "phase": "VERIFICATION",
    "system_id": "backup_service",
    "resource_id": "backup_3245",
    "operation": "VERIFY_RESTORE_BLOCKED",
    "state": "BLOCKED",
    "evidence_id": ""
  }
]
```

Predicted:
```json
[
  {
    "step_no": 1,
    "phase": "FINDING",
    "system_id": "backup_service",
    "resource_id": "backup_3245",
    "operation": "REPORT_RESTORE_RISK",
    "state": "ACTIVE",
    "evidence_id": "evidence_01"
  },
  {
    "step_no": 2,
    "phase": "REMEDIATION",
    "system_id": "backup_service",
    "resource_id": "backup_3245",
    "operation": "BLOCK_RESTORE",
    "state": "BLOCKED",
    "evidence_id": ""
  },
  {
    "step_no": 3,
    "phase": "VERIFICATION",
    "system_id": "account_service",
    "resource_id": "account_4092",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 4,
    "phase": "VERIFICATION",
    "system_id": "account_service",
    "resource_id": "account_6523",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 5,
    "phase": "VERIFICATION",
    "system_id": "security_service",
    "resource_id": "audit_record_1797",
    "operation": "VERIFY_RECORD_PRESENT",
    "state": "PRESENT",
    "evidence_id": ""
  },
  {
    "step_no": 6,
    "phase": "VERIFICATION",
    "system_id": "backup_service",
    "resource_id": "backup_3245",
    "operation": "VERIFY_RESTORE_BLOCKED",
    "state": "BLOCKED",
    "evidence_id": ""
  }
]
```

### case_18 (STEPS_ONLY_MISMATCH)

Predicted: INCOMPLETE; expected: INCOMPLETE.

Warnings: No identity-linked primary account state

Expected:
```json
[
  {
    "step_no": 1,
    "phase": "FINDING",
    "system_id": "search_service",
    "resource_id": "search_4013",
    "operation": "REPORT_REMAINING_RECORD",
    "state": "PRESENT",
    "evidence_id": "evidence_94"
  },
  {
    "step_no": 2,
    "phase": "FINDING",
    "system_id": "analytics_platform",
    "resource_id": "analytics_037",
    "operation": "REPORT_EXPOSED_PII",
    "state": "PRESENT",
    "evidence_id": "evidence_94"
  },
  {
    "step_no": 3,
    "phase": "FINDING",
    "system_id": "support_platform",
    "resource_id": "support_5569",
    "operation": "REPORT_EXPOSED_PII",
    "state": "PRESENT",
    "evidence_id": "evidence_94"
  },
  {
    "step_no": 4,
    "phase": "FINDING",
    "system_id": "integration_service",
    "resource_id": "data_flow_4890",
    "operation": "REPORT_ACTIVE_DATA_FLOW",
    "state": "ACTIVE",
    "evidence_id": "evidence_94"
  },
  {
    "step_no": 5,
    "phase": "REMEDIATION",
    "system_id": "integration_service",
    "resource_id": "data_flow_4890",
    "operation": "DISABLE_DATA_FLOW",
    "state": "DISABLED",
    "evidence_id": ""
  },
  {
    "step_no": 6,
    "phase": "REMEDIATION",
    "system_id": "search_service",
    "resource_id": "search_4013",
    "operation": "DELETE_RECORD",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 7,
    "phase": "REMEDIATION",
    "system_id": "support_platform",
    "resource_id": "support_5569",
    "operation": "REDACT_RECORD",
    "state": "REDACTED",
    "evidence_id": ""
  },
  {
    "step_no": 8,
    "phase": "REMEDIATION",
    "system_id": "analytics_platform",
    "resource_id": "analytics_037",
    "operation": "ANONYMIZE_RECORD",
    "state": "ANONYMIZED",
    "evidence_id": ""
  },
  {
    "step_no": 9,
    "phase": "VERIFICATION",
    "system_id": "account_service",
    "resource_id": "account_5521",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 10,
    "phase": "VERIFICATION",
    "system_id": "search_service",
    "resource_id": "search_4013",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 11,
    "phase": "VERIFICATION",
    "system_id": "security_service",
    "resource_id": "audit_record_6645",
    "operation": "VERIFY_RECORD_PRESENT",
    "state": "PRESENT",
    "evidence_id": ""
  },
  {
    "step_no": 12,
    "phase": "VERIFICATION",
    "system_id": "support_platform",
    "resource_id": "support_5569",
    "operation": "VERIFY_RECORD_REDACTED",
    "state": "REDACTED",
    "evidence_id": ""
  },
  {
    "step_no": 13,
    "phase": "VERIFICATION",
    "system_id": "analytics_platform",
    "resource_id": "analytics_037",
    "operation": "VERIFY_RECORD_ANONYMIZED",
    "state": "ANONYMIZED",
    "evidence_id": ""
  },
  {
    "step_no": 14,
    "phase": "VERIFICATION",
    "system_id": "integration_service",
    "resource_id": "data_flow_4890",
    "operation": "VERIFY_DATA_FLOW_DISABLED",
    "state": "DISABLED",
    "evidence_id": ""
  }
]
```

Predicted:
```json
[
  {
    "step_no": 1,
    "phase": "FINDING",
    "system_id": "search_service",
    "resource_id": "search_4013",
    "operation": "REPORT_REMAINING_RECORD",
    "state": "PRESENT",
    "evidence_id": "evidence_94"
  },
  {
    "step_no": 2,
    "phase": "FINDING",
    "system_id": "analytics_platform",
    "resource_id": "analytics_037",
    "operation": "REPORT_EXPOSED_PII",
    "state": "PRESENT",
    "evidence_id": "evidence_94"
  },
  {
    "step_no": 3,
    "phase": "FINDING",
    "system_id": "support_platform",
    "resource_id": "support_5569",
    "operation": "REPORT_EXPOSED_PII",
    "state": "PRESENT",
    "evidence_id": "evidence_94"
  },
  {
    "step_no": 4,
    "phase": "FINDING",
    "system_id": "integration_service",
    "resource_id": "data_flow_4890",
    "operation": "REPORT_ACTIVE_DATA_FLOW",
    "state": "ACTIVE",
    "evidence_id": "evidence_94"
  },
  {
    "step_no": 5,
    "phase": "REMEDIATION",
    "system_id": "integration_service",
    "resource_id": "data_flow_4890",
    "operation": "DISABLE_DATA_FLOW",
    "state": "DISABLED",
    "evidence_id": ""
  },
  {
    "step_no": 6,
    "phase": "REMEDIATION",
    "system_id": "search_service",
    "resource_id": "search_4013",
    "operation": "DELETE_RECORD",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 7,
    "phase": "REMEDIATION",
    "system_id": "support_platform",
    "resource_id": "support_5569",
    "operation": "REDACT_RECORD",
    "state": "REDACTED",
    "evidence_id": ""
  },
  {
    "step_no": 8,
    "phase": "REMEDIATION",
    "system_id": "analytics_platform",
    "resource_id": "analytics_037",
    "operation": "ANONYMIZE_RECORD",
    "state": "ANONYMIZED",
    "evidence_id": ""
  },
  {
    "step_no": 9,
    "phase": "VERIFICATION",
    "system_id": "search_service",
    "resource_id": "search_4013",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 10,
    "phase": "VERIFICATION",
    "system_id": "support_platform",
    "resource_id": "support_5569",
    "operation": "VERIFY_RECORD_REDACTED",
    "state": "REDACTED",
    "evidence_id": ""
  },
  {
    "step_no": 11,
    "phase": "VERIFICATION",
    "system_id": "analytics_platform",
    "resource_id": "analytics_037",
    "operation": "VERIFY_RECORD_ANONYMIZED",
    "state": "ANONYMIZED",
    "evidence_id": ""
  },
  {
    "step_no": 12,
    "phase": "VERIFICATION",
    "system_id": "integration_service",
    "resource_id": "data_flow_4890",
    "operation": "VERIFY_DATA_FLOW_DISABLED",
    "state": "DISABLED",
    "evidence_id": ""
  }
]
```

### case_20 (STEPS_ONLY_MISMATCH)

Predicted: INCOMPLETE; expected: INCOMPLETE.

Warnings: No identity-linked primary account state

Expected:
```json
[
  {
    "step_no": 1,
    "phase": "FINDING",
    "system_id": "search_service",
    "resource_id": "search_4262",
    "operation": "REPORT_REMAINING_RECORD",
    "state": "PRESENT",
    "evidence_id": "evidence_94"
  },
  {
    "step_no": 2,
    "phase": "FINDING",
    "system_id": "integration_service",
    "resource_id": "data_flow_1770",
    "operation": "REPORT_ACTIVE_DATA_FLOW",
    "state": "ACTIVE",
    "evidence_id": "evidence_94"
  },
  {
    "step_no": 3,
    "phase": "REMEDIATION",
    "system_id": "integration_service",
    "resource_id": "data_flow_1770",
    "operation": "DISABLE_DATA_FLOW",
    "state": "DISABLED",
    "evidence_id": ""
  },
  {
    "step_no": 4,
    "phase": "REMEDIATION",
    "system_id": "search_service",
    "resource_id": "search_4262",
    "operation": "DELETE_RECORD",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 5,
    "phase": "VERIFICATION",
    "system_id": "account_service",
    "resource_id": "account_5037",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 6,
    "phase": "VERIFICATION",
    "system_id": "search_service",
    "resource_id": "search_4262",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 7,
    "phase": "VERIFICATION",
    "system_id": "security_service",
    "resource_id": "audit_record_5569",
    "operation": "VERIFY_RECORD_PRESENT",
    "state": "PRESENT",
    "evidence_id": ""
  },
  {
    "step_no": 8,
    "phase": "VERIFICATION",
    "system_id": "integration_service",
    "resource_id": "data_flow_1770",
    "operation": "VERIFY_DATA_FLOW_DISABLED",
    "state": "DISABLED",
    "evidence_id": ""
  }
]
```

Predicted:
```json
[
  {
    "step_no": 1,
    "phase": "FINDING",
    "system_id": "search_service",
    "resource_id": "search_4262",
    "operation": "REPORT_REMAINING_RECORD",
    "state": "PRESENT",
    "evidence_id": "evidence_94"
  },
  {
    "step_no": 2,
    "phase": "FINDING",
    "system_id": "integration_service",
    "resource_id": "data_flow_1770",
    "operation": "REPORT_ACTIVE_DATA_FLOW",
    "state": "ACTIVE",
    "evidence_id": "evidence_94"
  },
  {
    "step_no": 3,
    "phase": "REMEDIATION",
    "system_id": "integration_service",
    "resource_id": "data_flow_1770",
    "operation": "DISABLE_DATA_FLOW",
    "state": "DISABLED",
    "evidence_id": ""
  },
  {
    "step_no": 4,
    "phase": "REMEDIATION",
    "system_id": "search_service",
    "resource_id": "search_4262",
    "operation": "DELETE_RECORD",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 5,
    "phase": "VERIFICATION",
    "system_id": "search_service",
    "resource_id": "search_4262",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 6,
    "phase": "VERIFICATION",
    "system_id": "integration_service",
    "resource_id": "data_flow_1770",
    "operation": "VERIFY_DATA_FLOW_DISABLED",
    "state": "DISABLED",
    "evidence_id": ""
  }
]
```

### case_21 (STATUS_MISMATCH)

Predicted: INCOMPLETE; expected: COMPLETE.

Warnings: tombstone_17: ambiguous resource ownership; No identity-linked primary account state

Expected:
```json
[
  {
    "step_no": 1,
    "phase": "VERIFICATION",
    "system_id": "account_service",
    "resource_id": "account_6440",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 2,
    "phase": "VERIFICATION",
    "system_id": "security_service",
    "resource_id": "audit_record_3737",
    "operation": "VERIFY_RECORD_PRESENT",
    "state": "PRESENT",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 3,
    "phase": "VERIFICATION",
    "system_id": "analytics_platform",
    "resource_id": "analytics_5335",
    "operation": "VERIFY_RECORD_ANONYMIZED",
    "state": "ANONYMIZED",
    "evidence_id": "evidence_92"
  }
]
```

Predicted:
```json
[
  {
    "step_no": 1,
    "phase": "VERIFICATION",
    "system_id": "security_service",
    "resource_id": "audit_record_3737",
    "operation": "VERIFY_RECORD_PRESENT",
    "state": "PRESENT",
    "evidence_id": ""
  }
]
```

### case_22 (STEPS_ONLY_MISMATCH)

Predicted: INCOMPLETE; expected: INCOMPLETE.

Warnings: No identity-linked primary account state

Expected:
```json
[
  {
    "step_no": 1,
    "phase": "FINDING",
    "system_id": "search_service",
    "resource_id": "search_8911",
    "operation": "REPORT_REMAINING_RECORD",
    "state": "PRESENT",
    "evidence_id": "evidence_05"
  },
  {
    "step_no": 2,
    "phase": "FINDING",
    "system_id": "analytics_platform",
    "resource_id": "analytics_4440",
    "operation": "REPORT_EXPOSED_PII",
    "state": "PRESENT",
    "evidence_id": "evidence_05"
  },
  {
    "step_no": 3,
    "phase": "REMEDIATION",
    "system_id": "search_service",
    "resource_id": "search_8911",
    "operation": "DELETE_RECORD",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 4,
    "phase": "REMEDIATION",
    "system_id": "analytics_platform",
    "resource_id": "analytics_4440",
    "operation": "ANONYMIZE_RECORD",
    "state": "ANONYMIZED",
    "evidence_id": ""
  },
  {
    "step_no": 5,
    "phase": "VERIFICATION",
    "system_id": "account_service",
    "resource_id": "account_4990",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 6,
    "phase": "VERIFICATION",
    "system_id": "search_service",
    "resource_id": "search_8911",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 7,
    "phase": "VERIFICATION",
    "system_id": "security_service",
    "resource_id": "audit_record_3482",
    "operation": "VERIFY_RECORD_PRESENT",
    "state": "PRESENT",
    "evidence_id": ""
  },
  {
    "step_no": 8,
    "phase": "VERIFICATION",
    "system_id": "analytics_platform",
    "resource_id": "analytics_4440",
    "operation": "VERIFY_RECORD_ANONYMIZED",
    "state": "ANONYMIZED",
    "evidence_id": ""
  }
]
```

Predicted:
```json
[
  {
    "step_no": 1,
    "phase": "FINDING",
    "system_id": "search_service",
    "resource_id": "search_8911",
    "operation": "REPORT_REMAINING_RECORD",
    "state": "PRESENT",
    "evidence_id": "evidence_05"
  },
  {
    "step_no": 2,
    "phase": "FINDING",
    "system_id": "analytics_platform",
    "resource_id": "analytics_4440",
    "operation": "REPORT_EXPOSED_PII",
    "state": "PRESENT",
    "evidence_id": "evidence_05"
  },
  {
    "step_no": 3,
    "phase": "REMEDIATION",
    "system_id": "search_service",
    "resource_id": "search_8911",
    "operation": "DELETE_RECORD",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 4,
    "phase": "REMEDIATION",
    "system_id": "analytics_platform",
    "resource_id": "analytics_4440",
    "operation": "ANONYMIZE_RECORD",
    "state": "ANONYMIZED",
    "evidence_id": ""
  },
  {
    "step_no": 5,
    "phase": "VERIFICATION",
    "system_id": "search_service",
    "resource_id": "search_8911",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 6,
    "phase": "VERIFICATION",
    "system_id": "security_service",
    "resource_id": "audit_record_3482",
    "operation": "VERIFY_RECORD_PRESENT",
    "state": "PRESENT",
    "evidence_id": ""
  },
  {
    "step_no": 7,
    "phase": "VERIFICATION",
    "system_id": "analytics_platform",
    "resource_id": "analytics_4440",
    "operation": "VERIFY_RECORD_ANONYMIZED",
    "state": "ANONYMIZED",
    "evidence_id": ""
  }
]
```

### case_23 (STEPS_ONLY_MISMATCH)

Predicted: INCOMPLETE; expected: INCOMPLETE.

Warnings: No identity-linked primary account state

Expected:
```json
[
  {
    "step_no": 1,
    "phase": "FINDING",
    "system_id": "export_service",
    "resource_id": "export_7364",
    "operation": "REPORT_REMAINING_RECORD",
    "state": "PRESENT",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 2,
    "phase": "FINDING",
    "system_id": "search_service",
    "resource_id": "search_898",
    "operation": "REPORT_REMAINING_RECORD",
    "state": "PRESENT",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 3,
    "phase": "REMEDIATION",
    "system_id": "export_service",
    "resource_id": "export_7364",
    "operation": "DELETE_RECORD",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 4,
    "phase": "REMEDIATION",
    "system_id": "search_service",
    "resource_id": "search_898",
    "operation": "DELETE_RECORD",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 5,
    "phase": "VERIFICATION",
    "system_id": "account_service",
    "resource_id": "account_410",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 6,
    "phase": "VERIFICATION",
    "system_id": "export_service",
    "resource_id": "export_7364",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 7,
    "phase": "VERIFICATION",
    "system_id": "search_service",
    "resource_id": "search_898",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 8,
    "phase": "VERIFICATION",
    "system_id": "security_service",
    "resource_id": "audit_record_4128",
    "operation": "VERIFY_RECORD_PRESENT",
    "state": "PRESENT",
    "evidence_id": ""
  }
]
```

Predicted:
```json
[
  {
    "step_no": 1,
    "phase": "FINDING",
    "system_id": "export_service",
    "resource_id": "export_7364",
    "operation": "REPORT_REMAINING_RECORD",
    "state": "PRESENT",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 2,
    "phase": "FINDING",
    "system_id": "search_service",
    "resource_id": "search_898",
    "operation": "REPORT_REMAINING_RECORD",
    "state": "PRESENT",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 3,
    "phase": "REMEDIATION",
    "system_id": "export_service",
    "resource_id": "export_7364",
    "operation": "DELETE_RECORD",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 4,
    "phase": "REMEDIATION",
    "system_id": "search_service",
    "resource_id": "search_898",
    "operation": "DELETE_RECORD",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 5,
    "phase": "VERIFICATION",
    "system_id": "export_service",
    "resource_id": "export_7364",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 6,
    "phase": "VERIFICATION",
    "system_id": "search_service",
    "resource_id": "search_898",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": ""
  }
]
```

### case_24 (STEPS_ONLY_MISMATCH)

Predicted: INCOMPLETE; expected: INCOMPLETE.

Warnings: tombstone_17: ambiguous resource ownership

Expected:
```json
[
  {
    "step_no": 1,
    "phase": "FINDING",
    "system_id": "account_service",
    "resource_id": "account_5334",
    "operation": "REPORT_REMAINING_RECORD",
    "state": "PRESENT",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 2,
    "phase": "FINDING",
    "system_id": "search_service",
    "resource_id": "search_5577",
    "operation": "REPORT_REMAINING_RECORD",
    "state": "PRESENT",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 3,
    "phase": "REMEDIATION",
    "system_id": "account_service",
    "resource_id": "account_5334",
    "operation": "DELETE_RECORD",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 4,
    "phase": "REMEDIATION",
    "system_id": "search_service",
    "resource_id": "search_5577",
    "operation": "DELETE_RECORD",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 5,
    "phase": "VERIFICATION",
    "system_id": "account_service",
    "resource_id": "account_5334",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 6,
    "phase": "VERIFICATION",
    "system_id": "search_service",
    "resource_id": "search_5577",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 7,
    "phase": "VERIFICATION",
    "system_id": "security_service",
    "resource_id": "audit_record_7095",
    "operation": "VERIFY_RECORD_PRESENT",
    "state": "PRESENT",
    "evidence_id": ""
  }
]
```

Predicted:
```json
[
  {
    "step_no": 1,
    "phase": "FINDING",
    "system_id": "account_service",
    "resource_id": "account_5334",
    "operation": "REPORT_REMAINING_RECORD",
    "state": "PRESENT",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 2,
    "phase": "FINDING",
    "system_id": "search_service",
    "resource_id": "search_5577",
    "operation": "REPORT_REMAINING_RECORD",
    "state": "PRESENT",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 3,
    "phase": "REMEDIATION",
    "system_id": "account_service",
    "resource_id": "account_5334",
    "operation": "DELETE_RECORD",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 4,
    "phase": "REMEDIATION",
    "system_id": "search_service",
    "resource_id": "search_5577",
    "operation": "DELETE_RECORD",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 5,
    "phase": "VERIFICATION",
    "system_id": "account_service",
    "resource_id": "account_5334",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 6,
    "phase": "VERIFICATION",
    "system_id": "search_service",
    "resource_id": "search_5577",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": ""
  }
]
```

### case_25 (STATUS_MISMATCH)

Predicted: INCOMPLETE; expected: COMPLETE.

Warnings: No identity-linked primary account state

Expected:
```json
[
  {
    "step_no": 1,
    "phase": "VERIFICATION",
    "system_id": "account_service",
    "resource_id": "account_3136",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 2,
    "phase": "VERIFICATION",
    "system_id": "security_service",
    "resource_id": "audit_record_451",
    "operation": "VERIFY_RECORD_PRESENT",
    "state": "PRESENT",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 3,
    "phase": "VERIFICATION",
    "system_id": "analytics_platform",
    "resource_id": "analytics_1895",
    "operation": "VERIFY_RECORD_ANONYMIZED",
    "state": "ANONYMIZED",
    "evidence_id": "evidence_92"
  }
]
```

Predicted:
```json
[
  {
    "step_no": 1,
    "phase": "VERIFICATION",
    "system_id": "security_service",
    "resource_id": "audit_record_451",
    "operation": "VERIFY_RECORD_PRESENT",
    "state": "PRESENT",
    "evidence_id": ""
  }
]
```

### case_26 (STATUS_MISMATCH)

Predicted: INCOMPLETE; expected: COMPLETE.

Warnings: No identity-linked primary account state

Expected:
```json
[
  {
    "step_no": 1,
    "phase": "VERIFICATION",
    "system_id": "account_service",
    "resource_id": "account_5684",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 2,
    "phase": "VERIFICATION",
    "system_id": "security_service",
    "resource_id": "audit_record_5416",
    "operation": "VERIFY_RECORD_PRESENT",
    "state": "PRESENT",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 3,
    "phase": "VERIFICATION",
    "system_id": "support_platform",
    "resource_id": "support_4715",
    "operation": "VERIFY_RECORD_REDACTED",
    "state": "REDACTED",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 4,
    "phase": "VERIFICATION",
    "system_id": "analytics_platform",
    "resource_id": "analytics_4566",
    "operation": "VERIFY_RECORD_ANONYMIZED",
    "state": "ANONYMIZED",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 5,
    "phase": "VERIFICATION",
    "system_id": "integration_service",
    "resource_id": "data_flow_6244",
    "operation": "VERIFY_DATA_FLOW_DISABLED",
    "state": "DISABLED",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 6,
    "phase": "VERIFICATION",
    "system_id": "backup_service",
    "resource_id": "backup_3120",
    "operation": "VERIFY_RESTORE_BLOCKED",
    "state": "BLOCKED",
    "evidence_id": "evidence_92"
  }
]
```

Predicted:
```json
[
  {
    "step_no": 1,
    "phase": "VERIFICATION",
    "system_id": "security_service",
    "resource_id": "audit_record_5416",
    "operation": "VERIFY_RECORD_PRESENT",
    "state": "PRESENT",
    "evidence_id": ""
  },
  {
    "step_no": 2,
    "phase": "VERIFICATION",
    "system_id": "support_platform",
    "resource_id": "support_4715",
    "operation": "VERIFY_RECORD_REDACTED",
    "state": "REDACTED",
    "evidence_id": ""
  },
  {
    "step_no": 3,
    "phase": "VERIFICATION",
    "system_id": "integration_service",
    "resource_id": "data_flow_6244",
    "operation": "VERIFY_DATA_FLOW_DISABLED",
    "state": "DISABLED",
    "evidence_id": ""
  },
  {
    "step_no": 4,
    "phase": "VERIFICATION",
    "system_id": "backup_service",
    "resource_id": "backup_3120",
    "operation": "VERIFY_RESTORE_BLOCKED",
    "state": "BLOCKED",
    "evidence_id": ""
  }
]
```

### case_27 (STATUS_MISMATCH)

Predicted: INCOMPLETE; expected: COMPLETE.

Warnings: No identity-linked primary account state

Expected:
```json
[
  {
    "step_no": 1,
    "phase": "VERIFICATION",
    "system_id": "account_service",
    "resource_id": "account_3866",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 2,
    "phase": "VERIFICATION",
    "system_id": "security_service",
    "resource_id": "audit_record_3830",
    "operation": "VERIFY_RECORD_PRESENT",
    "state": "PRESENT",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 3,
    "phase": "VERIFICATION",
    "system_id": "support_platform",
    "resource_id": "support_4707",
    "operation": "VERIFY_RECORD_REDACTED",
    "state": "REDACTED",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 4,
    "phase": "VERIFICATION",
    "system_id": "analytics_platform",
    "resource_id": "analytics_4574",
    "operation": "VERIFY_RECORD_ANONYMIZED",
    "state": "ANONYMIZED",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 5,
    "phase": "VERIFICATION",
    "system_id": "integration_service",
    "resource_id": "data_flow_2295",
    "operation": "VERIFY_DATA_FLOW_DISABLED",
    "state": "DISABLED",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 6,
    "phase": "VERIFICATION",
    "system_id": "backup_service",
    "resource_id": "backup_5970",
    "operation": "VERIFY_RESTORE_BLOCKED",
    "state": "BLOCKED",
    "evidence_id": "evidence_92"
  }
]
```

Predicted:
```json
[
  {
    "step_no": 1,
    "phase": "VERIFICATION",
    "system_id": "security_service",
    "resource_id": "audit_record_3830",
    "operation": "VERIFY_RECORD_PRESENT",
    "state": "PRESENT",
    "evidence_id": ""
  },
  {
    "step_no": 2,
    "phase": "VERIFICATION",
    "system_id": "support_platform",
    "resource_id": "support_4707",
    "operation": "VERIFY_RECORD_REDACTED",
    "state": "REDACTED",
    "evidence_id": ""
  },
  {
    "step_no": 3,
    "phase": "VERIFICATION",
    "system_id": "integration_service",
    "resource_id": "data_flow_2295",
    "operation": "VERIFY_DATA_FLOW_DISABLED",
    "state": "DISABLED",
    "evidence_id": ""
  },
  {
    "step_no": 4,
    "phase": "VERIFICATION",
    "system_id": "backup_service",
    "resource_id": "backup_5970",
    "operation": "VERIFY_RESTORE_BLOCKED",
    "state": "BLOCKED",
    "evidence_id": ""
  }
]
```

### case_28 (STATUS_MISMATCH)

Predicted: INCOMPLETE; expected: COMPLETE.

Warnings: No identity-linked primary account state

Expected:
```json
[
  {
    "step_no": 1,
    "phase": "VERIFICATION",
    "system_id": "account_service",
    "resource_id": "account_5482",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 2,
    "phase": "VERIFICATION",
    "system_id": "security_service",
    "resource_id": "audit_record_9265",
    "operation": "VERIFY_RECORD_PRESENT",
    "state": "PRESENT",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 3,
    "phase": "VERIFICATION",
    "system_id": "support_platform",
    "resource_id": "support_2351",
    "operation": "VERIFY_RECORD_REDACTED",
    "state": "REDACTED",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 4,
    "phase": "VERIFICATION",
    "system_id": "analytics_platform",
    "resource_id": "analytics_6077",
    "operation": "VERIFY_RECORD_ANONYMIZED",
    "state": "ANONYMIZED",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 5,
    "phase": "VERIFICATION",
    "system_id": "integration_service",
    "resource_id": "data_flow_2337",
    "operation": "VERIFY_DATA_FLOW_DISABLED",
    "state": "DISABLED",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 6,
    "phase": "VERIFICATION",
    "system_id": "backup_service",
    "resource_id": "backup_838",
    "operation": "VERIFY_RESTORE_BLOCKED",
    "state": "BLOCKED",
    "evidence_id": "evidence_92"
  }
]
```

Predicted:
```json
[
  {
    "step_no": 1,
    "phase": "VERIFICATION",
    "system_id": "security_service",
    "resource_id": "audit_record_9265",
    "operation": "VERIFY_RECORD_PRESENT",
    "state": "PRESENT",
    "evidence_id": ""
  },
  {
    "step_no": 2,
    "phase": "VERIFICATION",
    "system_id": "support_platform",
    "resource_id": "support_2351",
    "operation": "VERIFY_RECORD_REDACTED",
    "state": "REDACTED",
    "evidence_id": ""
  },
  {
    "step_no": 3,
    "phase": "VERIFICATION",
    "system_id": "integration_service",
    "resource_id": "data_flow_2337",
    "operation": "VERIFY_DATA_FLOW_DISABLED",
    "state": "DISABLED",
    "evidence_id": ""
  },
  {
    "step_no": 4,
    "phase": "VERIFICATION",
    "system_id": "backup_service",
    "resource_id": "backup_838",
    "operation": "VERIFY_RESTORE_BLOCKED",
    "state": "BLOCKED",
    "evidence_id": ""
  }
]
```

### case_29 (STEPS_ONLY_MISMATCH)

Predicted: INCOMPLETE; expected: INCOMPLETE.

Warnings: tombstone_17: ambiguous resource ownership; No identity-linked primary account state

Expected:
```json
[
  {
    "step_no": 1,
    "phase": "FINDING",
    "system_id": "search_service",
    "resource_id": "search_1993",
    "operation": "REPORT_REMAINING_RECORD",
    "state": "PRESENT",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 2,
    "phase": "FINDING",
    "system_id": "analytics_platform",
    "resource_id": "analytics_5208",
    "operation": "REPORT_EXPOSED_PII",
    "state": "PRESENT",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 3,
    "phase": "FINDING",
    "system_id": "support_platform",
    "resource_id": "support_5281",
    "operation": "REPORT_EXPOSED_PII",
    "state": "PRESENT",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 4,
    "phase": "FINDING",
    "system_id": "integration_service",
    "resource_id": "data_flow_3827",
    "operation": "REPORT_ACTIVE_DATA_FLOW",
    "state": "ACTIVE",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 5,
    "phase": "REMEDIATION",
    "system_id": "integration_service",
    "resource_id": "data_flow_3827",
    "operation": "DISABLE_DATA_FLOW",
    "state": "DISABLED",
    "evidence_id": ""
  },
  {
    "step_no": 6,
    "phase": "REMEDIATION",
    "system_id": "search_service",
    "resource_id": "search_1993",
    "operation": "DELETE_RECORD",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 7,
    "phase": "REMEDIATION",
    "system_id": "support_platform",
    "resource_id": "support_5281",
    "operation": "REDACT_RECORD",
    "state": "REDACTED",
    "evidence_id": ""
  },
  {
    "step_no": 8,
    "phase": "REMEDIATION",
    "system_id": "analytics_platform",
    "resource_id": "analytics_5208",
    "operation": "ANONYMIZE_RECORD",
    "state": "ANONYMIZED",
    "evidence_id": ""
  },
  {
    "step_no": 9,
    "phase": "VERIFICATION",
    "system_id": "account_service",
    "resource_id": "account_7012",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 10,
    "phase": "VERIFICATION",
    "system_id": "search_service",
    "resource_id": "search_1993",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 11,
    "phase": "VERIFICATION",
    "system_id": "security_service",
    "resource_id": "audit_record_3954",
    "operation": "VERIFY_RECORD_PRESENT",
    "state": "PRESENT",
    "evidence_id": ""
  },
  {
    "step_no": 12,
    "phase": "VERIFICATION",
    "system_id": "support_platform",
    "resource_id": "support_5281",
    "operation": "VERIFY_RECORD_REDACTED",
    "state": "REDACTED",
    "evidence_id": ""
  },
  {
    "step_no": 13,
    "phase": "VERIFICATION",
    "system_id": "analytics_platform",
    "resource_id": "analytics_5208",
    "operation": "VERIFY_RECORD_ANONYMIZED",
    "state": "ANONYMIZED",
    "evidence_id": ""
  },
  {
    "step_no": 14,
    "phase": "VERIFICATION",
    "system_id": "integration_service",
    "resource_id": "data_flow_3827",
    "operation": "VERIFY_DATA_FLOW_DISABLED",
    "state": "DISABLED",
    "evidence_id": ""
  }
]
```

Predicted:
```json
[
  {
    "step_no": 1,
    "phase": "FINDING",
    "system_id": "search_service",
    "resource_id": "search_1993",
    "operation": "REPORT_REMAINING_RECORD",
    "state": "PRESENT",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 2,
    "phase": "FINDING",
    "system_id": "analytics_platform",
    "resource_id": "analytics_5208",
    "operation": "REPORT_EXPOSED_PII",
    "state": "PRESENT",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 3,
    "phase": "FINDING",
    "system_id": "support_platform",
    "resource_id": "support_5281",
    "operation": "REPORT_EXPOSED_PII",
    "state": "PRESENT",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 4,
    "phase": "FINDING",
    "system_id": "integration_service",
    "resource_id": "data_flow_3827",
    "operation": "REPORT_ACTIVE_DATA_FLOW",
    "state": "ACTIVE",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 5,
    "phase": "REMEDIATION",
    "system_id": "integration_service",
    "resource_id": "data_flow_3827",
    "operation": "DISABLE_DATA_FLOW",
    "state": "DISABLED",
    "evidence_id": ""
  },
  {
    "step_no": 6,
    "phase": "REMEDIATION",
    "system_id": "search_service",
    "resource_id": "search_1993",
    "operation": "DELETE_RECORD",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 7,
    "phase": "REMEDIATION",
    "system_id": "support_platform",
    "resource_id": "support_5281",
    "operation": "REDACT_RECORD",
    "state": "REDACTED",
    "evidence_id": ""
  },
  {
    "step_no": 8,
    "phase": "REMEDIATION",
    "system_id": "analytics_platform",
    "resource_id": "analytics_5208",
    "operation": "ANONYMIZE_RECORD",
    "state": "ANONYMIZED",
    "evidence_id": ""
  },
  {
    "step_no": 9,
    "phase": "VERIFICATION",
    "system_id": "search_service",
    "resource_id": "search_1993",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 10,
    "phase": "VERIFICATION",
    "system_id": "support_platform",
    "resource_id": "support_5281",
    "operation": "VERIFY_RECORD_REDACTED",
    "state": "REDACTED",
    "evidence_id": ""
  },
  {
    "step_no": 11,
    "phase": "VERIFICATION",
    "system_id": "analytics_platform",
    "resource_id": "analytics_5208",
    "operation": "VERIFY_RECORD_ANONYMIZED",
    "state": "ANONYMIZED",
    "evidence_id": ""
  },
  {
    "step_no": 12,
    "phase": "VERIFICATION",
    "system_id": "integration_service",
    "resource_id": "data_flow_3827",
    "operation": "VERIFY_DATA_FLOW_DISABLED",
    "state": "DISABLED",
    "evidence_id": ""
  }
]
```

### case_30 (STEPS_ONLY_MISMATCH)

Predicted: INCOMPLETE; expected: INCOMPLETE.

Warnings: No identity-linked primary account state

Expected:
```json
[
  {
    "step_no": 1,
    "phase": "FINDING",
    "system_id": "search_service",
    "resource_id": "search_9359",
    "operation": "REPORT_REMAINING_RECORD",
    "state": "PRESENT",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 2,
    "phase": "FINDING",
    "system_id": "analytics_platform",
    "resource_id": "analytics_3697",
    "operation": "REPORT_EXPOSED_PII",
    "state": "PRESENT",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 3,
    "phase": "FINDING",
    "system_id": "support_platform",
    "resource_id": "support_6477",
    "operation": "REPORT_EXPOSED_PII",
    "state": "PRESENT",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 4,
    "phase": "FINDING",
    "system_id": "integration_service",
    "resource_id": "data_flow_8524",
    "operation": "REPORT_ACTIVE_DATA_FLOW",
    "state": "ACTIVE",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 5,
    "phase": "REMEDIATION",
    "system_id": "integration_service",
    "resource_id": "data_flow_8524",
    "operation": "DISABLE_DATA_FLOW",
    "state": "DISABLED",
    "evidence_id": ""
  },
  {
    "step_no": 6,
    "phase": "REMEDIATION",
    "system_id": "search_service",
    "resource_id": "search_9359",
    "operation": "DELETE_RECORD",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 7,
    "phase": "REMEDIATION",
    "system_id": "support_platform",
    "resource_id": "support_6477",
    "operation": "REDACT_RECORD",
    "state": "REDACTED",
    "evidence_id": ""
  },
  {
    "step_no": 8,
    "phase": "REMEDIATION",
    "system_id": "analytics_platform",
    "resource_id": "analytics_3697",
    "operation": "ANONYMIZE_RECORD",
    "state": "ANONYMIZED",
    "evidence_id": ""
  },
  {
    "step_no": 9,
    "phase": "VERIFICATION",
    "system_id": "account_service",
    "resource_id": "account_4163",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 10,
    "phase": "VERIFICATION",
    "system_id": "search_service",
    "resource_id": "search_9359",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 11,
    "phase": "VERIFICATION",
    "system_id": "security_service",
    "resource_id": "audit_record_1707",
    "operation": "VERIFY_RECORD_PRESENT",
    "state": "PRESENT",
    "evidence_id": ""
  },
  {
    "step_no": 12,
    "phase": "VERIFICATION",
    "system_id": "support_platform",
    "resource_id": "support_6477",
    "operation": "VERIFY_RECORD_REDACTED",
    "state": "REDACTED",
    "evidence_id": ""
  },
  {
    "step_no": 13,
    "phase": "VERIFICATION",
    "system_id": "analytics_platform",
    "resource_id": "analytics_3697",
    "operation": "VERIFY_RECORD_ANONYMIZED",
    "state": "ANONYMIZED",
    "evidence_id": ""
  },
  {
    "step_no": 14,
    "phase": "VERIFICATION",
    "system_id": "integration_service",
    "resource_id": "data_flow_8524",
    "operation": "VERIFY_DATA_FLOW_DISABLED",
    "state": "DISABLED",
    "evidence_id": ""
  }
]
```

Predicted:
```json
[
  {
    "step_no": 1,
    "phase": "FINDING",
    "system_id": "search_service",
    "resource_id": "search_9359",
    "operation": "REPORT_REMAINING_RECORD",
    "state": "PRESENT",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 2,
    "phase": "FINDING",
    "system_id": "analytics_platform",
    "resource_id": "analytics_3697",
    "operation": "REPORT_EXPOSED_PII",
    "state": "PRESENT",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 3,
    "phase": "FINDING",
    "system_id": "support_platform",
    "resource_id": "support_6477",
    "operation": "REPORT_EXPOSED_PII",
    "state": "PRESENT",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 4,
    "phase": "FINDING",
    "system_id": "integration_service",
    "resource_id": "data_flow_8524",
    "operation": "REPORT_ACTIVE_DATA_FLOW",
    "state": "ACTIVE",
    "evidence_id": "evidence_92"
  },
  {
    "step_no": 5,
    "phase": "REMEDIATION",
    "system_id": "integration_service",
    "resource_id": "data_flow_8524",
    "operation": "DISABLE_DATA_FLOW",
    "state": "DISABLED",
    "evidence_id": ""
  },
  {
    "step_no": 6,
    "phase": "REMEDIATION",
    "system_id": "search_service",
    "resource_id": "search_9359",
    "operation": "DELETE_RECORD",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 7,
    "phase": "REMEDIATION",
    "system_id": "support_platform",
    "resource_id": "support_6477",
    "operation": "REDACT_RECORD",
    "state": "REDACTED",
    "evidence_id": ""
  },
  {
    "step_no": 8,
    "phase": "REMEDIATION",
    "system_id": "analytics_platform",
    "resource_id": "analytics_3697",
    "operation": "ANONYMIZE_RECORD",
    "state": "ANONYMIZED",
    "evidence_id": ""
  },
  {
    "step_no": 9,
    "phase": "VERIFICATION",
    "system_id": "search_service",
    "resource_id": "search_9359",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 10,
    "phase": "VERIFICATION",
    "system_id": "support_platform",
    "resource_id": "support_6477",
    "operation": "VERIFY_RECORD_REDACTED",
    "state": "REDACTED",
    "evidence_id": ""
  },
  {
    "step_no": 11,
    "phase": "VERIFICATION",
    "system_id": "analytics_platform",
    "resource_id": "analytics_3697",
    "operation": "VERIFY_RECORD_ANONYMIZED",
    "state": "ANONYMIZED",
    "evidence_id": ""
  },
  {
    "step_no": 12,
    "phase": "VERIFICATION",
    "system_id": "integration_service",
    "resource_id": "data_flow_8524",
    "operation": "VERIFY_DATA_FLOW_DISABLED",
    "state": "DISABLED",
    "evidence_id": ""
  }
]
```

### case_31 (STATUS_MISMATCH)

Predicted: INCOMPLETE; expected: COMPLETE.

Warnings: No identity-linked primary account state

Expected:
```json
[
  {
    "step_no": 1,
    "phase": "VERIFICATION",
    "system_id": "account_service",
    "resource_id": "account_4857",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": "evidence_51"
  },
  {
    "step_no": 2,
    "phase": "VERIFICATION",
    "system_id": "security_service",
    "resource_id": "audit_record_6909",
    "operation": "VERIFY_RECORD_PRESENT",
    "state": "PRESENT",
    "evidence_id": "evidence_51"
  },
  {
    "step_no": 3,
    "phase": "VERIFICATION",
    "system_id": "identity_service",
    "resource_id": "tombstone_440",
    "operation": "VERIFY_RECORD_REDACTED",
    "state": "REDACTED",
    "evidence_id": "evidence_51"
  }
]
```

Predicted:
```json
[
  {
    "step_no": 1,
    "phase": "VERIFICATION",
    "system_id": "security_service",
    "resource_id": "audit_record_6909",
    "operation": "VERIFY_RECORD_PRESENT",
    "state": "PRESENT",
    "evidence_id": ""
  },
  {
    "step_no": 2,
    "phase": "VERIFICATION",
    "system_id": "identity_service",
    "resource_id": "tombstone_440",
    "operation": "VERIFY_RECORD_REDACTED",
    "state": "REDACTED",
    "evidence_id": ""
  }
]
```

### case_32 (STEPS_ONLY_MISMATCH)

Predicted: INCOMPLETE; expected: INCOMPLETE.

Warnings: No identity-linked primary account state

Expected:
```json
[
  {
    "step_no": 1,
    "phase": "FINDING",
    "system_id": "identity_service",
    "resource_id": "tombstone_9178",
    "operation": "REPORT_EXPOSED_PII",
    "state": "PRESENT",
    "evidence_id": "evidence_51"
  },
  {
    "step_no": 2,
    "phase": "REMEDIATION",
    "system_id": "identity_service",
    "resource_id": "tombstone_9178",
    "operation": "REDACT_RECORD",
    "state": "REDACTED",
    "evidence_id": ""
  },
  {
    "step_no": 3,
    "phase": "VERIFICATION",
    "system_id": "account_service",
    "resource_id": "account_8858",
    "operation": "VERIFY_RECORD_ABSENT",
    "state": "ABSENT",
    "evidence_id": ""
  },
  {
    "step_no": 4,
    "phase": "VERIFICATION",
    "system_id": "security_service",
    "resource_id": "audit_record_7068",
    "operation": "VERIFY_RECORD_PRESENT",
    "state": "PRESENT",
    "evidence_id": ""
  },
  {
    "step_no": 5,
    "phase": "VERIFICATION",
    "system_id": "identity_service",
    "resource_id": "tombstone_9178",
    "operation": "VERIFY_RECORD_REDACTED",
    "state": "REDACTED",
    "evidence_id": ""
  }
]
```

Predicted:
```json
[
  {
    "step_no": 1,
    "phase": "FINDING",
    "system_id": "identity_service",
    "resource_id": "tombstone_9178",
    "operation": "REPORT_EXPOSED_PII",
    "state": "PRESENT",
    "evidence_id": "evidence_51"
  },
  {
    "step_no": 2,
    "phase": "REMEDIATION",
    "system_id": "identity_service",
    "resource_id": "tombstone_9178",
    "operation": "REDACT_RECORD",
    "state": "REDACTED",
    "evidence_id": ""
  },
  {
    "step_no": 3,
    "phase": "VERIFICATION",
    "system_id": "security_service",
    "resource_id": "audit_record_7068",
    "operation": "VERIFY_RECORD_PRESENT",
    "state": "PRESENT",
    "evidence_id": ""
  },
  {
    "step_no": 4,
    "phase": "VERIFICATION",
    "system_id": "identity_service",
    "resource_id": "tombstone_9178",
    "operation": "VERIFY_RECORD_REDACTED",
    "state": "REDACTED",
    "evidence_id": ""
  }
]
```

## Limits

Mismatch categories and warnings describe observed behavior, not proven root causes. Each reference-cited source still requires inspection within the audit cutoff before a general solver change is justified. No case-specific label patch or synthetic resource mapping is warranted. case_55 is a full-dataset request, not one of these public sample IDs. Its unresolved status is not proven the uniquely correct answer merely because output is reproducible.
