# Reviewed image observations

Literal resource fields transcribed after visually inspecting all 11 supplied screenshots. These are source observations, not deletion verdicts. The solver checks each source SHA-256 before using them, and applies the manifest cutoff. No case identifiers or expected answers are stored here. A missing restore setting is not interpreted as restore permission. The reference-registry screenshot shows links but does not prove hidden PII fields are empty.

```json
[
  {
    "file_path": "evidence/images/account_admin_console_20260926.png",
    "sha256": "d5c32ca5b6e1a2b4bbe9f5d41835ef1fd5d4f7061dab9067a4f9f88cea3c1861",
    "records": [
      {
        "system": "account_service",
        "resource_id": "account_5762",
        "category": "USER_PROFILE",
        "record": {
          "user_id": "user_11",
          "email": "haruka.s1838@zoho.com",
          "phone": "+81 90 7610 2507"
        }
      }
    ]
  },
  {
    "file_path": "evidence/images/search_index_inspector_20260901.png",
    "sha256": "75afdb0ae53a4510c83399a70d88073cb4fb2747454095756e4ddad1a8c70605",
    "records": [
      {
        "system": "search_service",
        "resource_id": "search_428",
        "category": "SEARCH_INDEX_ENTRY",
        "record": {
          "user_id": "user_13",
          "email": "g.silva76@gmail.com"
        }
      },
      {
        "system": "search_service",
        "resource_id": "search_1874",
        "category": "SEARCH_INDEX_ENTRY",
        "record": {
          "email": "g.silva76.jr@gmail.com"
        }
      }
    ]
  },
  {
    "file_path": "evidence/images/connector_management_console_20260807.png",
    "sha256": "e81fabc93ea1b5f4c918d934cdb2bea05d61737adfcc29f281494f5d8ec46355",
    "records": [
      {
        "system": "integration_service",
        "resource_id": "data_flow_1121",
        "category": "DATA_FLOW",
        "record": {
          "subject_selector": "jain.aditi@gmail.com",
          "enabled": true
        }
      },
      {
        "system": "integration_service",
        "resource_id": "data_flow_9846",
        "category": "DATA_FLOW",
        "record": {
          "subject_selector": "lucia-torres@gmail.com",
          "enabled": true
        }
      }
    ]
  },
  {
    "file_path": "evidence/images/analytics_profile_view_20260713.png",
    "sha256": "4e4cb259bc2010b622b0c53fe5872258f994fefc23452a83bb27473758693484",
    "records": [
      {
        "system": "analytics_platform",
        "resource_id": "analytics_7438",
        "category": "ANALYTICS_PROFILE",
        "record": {
          "user_id": "user_20",
          "email": "darwish.omar@icloud.com"
        }
      }
    ]
  },
  {
    "file_path": "evidence/images/customer_export_console_20260618.png",
    "sha256": "18b95c1bd8b8956e40216df935498a9f3c181ea2a69b5cd6d3c0841a816d5557",
    "records": [
      {
        "system": "export_service",
        "resource_id": "export_1260",
        "category": "USER_EXPORT",
        "record": {
          "owner_email": "ingrid.dahl@outlook.com",
          "download_available": true
        }
      }
    ]
  },
  {
    "file_path": "evidence/images/support_ticket_console_20260524.png",
    "sha256": "542b7aec17e6b2f38827896e7eb52c70e4bfaaca22433621be1f80f54884e944",
    "records": [
      {
        "system": "support_platform",
        "resource_id": "support_1034",
        "category": "SUPPORT_MESSAGE",
        "record": {
          "requester_email": "kagyeman8947@fastmail.com",
          "requester_name": "Kofi Agyeman"
        }
      }
    ]
  },
  {
    "file_path": "evidence/images/backup_restore_console_20260429.png",
    "sha256": "2c246aa5843bec609b9ddfdf1154cd81e0fd61996f83954735e9856e48c18bf3",
    "records": [
      {
        "system": "backup_service",
        "resource_id": "backup_9287",
        "category": "BACKUP_ARCHIVE",
        "record": {
          "customer_email": "areed1433@gmail.com",
          "archive_present": true
        }
      }
    ]
  },
  {
    "file_path": "evidence/images/security_audit_explorer_20260905.png",
    "sha256": "ca59f693f4e7002466b3fdeaf1bb6763618770963dd811b60003772d07b4b03b",
    "records": [
      {
        "system": "security_service",
        "resource_id": "audit_record_003",
        "category": "SECURITY_AUDIT_LOG",
        "record": {
          "subject_reference": "user_03"
        }
      }
    ]
  },
  {
    "file_path": "evidence/images/deleted_account_reference_20260310.png",
    "sha256": "68c28a72afd6ed184d5990d15c543f8a516face204f0360f732755a8a63c28be",
    "records": [
      {
        "system": "identity_service",
        "resource_id": "tombstone_17",
        "category": "ACCOUNT_TOMBSTONE",
        "record": {
          "subject_reference": "user_17",
          "linked_records": [
            "ORD-20263245",
            "CS-3245",
            "CS-3378",
            "FIN-7742"
          ]
        }
      }
    ]
  },
  {
    "file_path": "evidence/images/object_storage_browser_20260213.png",
    "sha256": "96e9a191380c29b9e0ab997007268c4cd6353cb6721ebd1ed4a32599d8d37e04",
    "records": [
      {
        "system": "object_storage",
        "resource_id": "object_19",
        "category": "SUPPORT_ATTACHMENT",
        "record": {
          "file_name": "delivery_confirmation_19.pdf",
          "storage_class": "Standard"
        }
      }
    ]
  },
  {
    "file_path": "evidence/images/marketing_profile_console.png",
    "sha256": "51fa0e6a38f8fa3629ba1b0d0b90b4ed139715956b97bfd09a6f1a6232c15df5",
    "records": [
      {
        "system": "marketing_platform",
        "resource_id": "marketing_001",
        "category": "MARKETING_PROFILE",
        "record": {
          "email": "sj.park@naver.com",
          "phone": "+82 10-5837-9451",
          "name": "Soo-jin Park"
        }
      }
    ]
  }
]
```
