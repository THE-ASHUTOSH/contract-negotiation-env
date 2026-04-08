TASK_FIXTURES = {
    "task_easy": {
        "vendor_contract": """SOFTWARE SERVICE AGREEMENT

This Software Service Agreement ("Agreement") is entered into as of the date of last signature below.

CLAUSE 1 — SCOPE OF SERVICES
The Vendor shall provide the Client with access to its cloud-based software platform ("Service"), including all standard features, maintenance updates, and technical support as described in the attached Service Level Agreement.

CLAUSE 2 — PAYMENT TERMS
All invoices shall be due and payable within thirty (30) days of the invoice date ("Net-30"). Late payments shall accrue interest at a rate of 1.5% per month. The Client shall be responsible for all applicable taxes and fees associated with the Service.

CLAUSE 3 — TERM AND RENEWAL
This Agreement shall be effective for an initial term of twelve (12) months from the Effective Date and shall automatically renew for successive twelve (12) month periods unless either party provides written notice of non-renewal at least thirty (30) days prior to the end of the then-current term.

CLAUSE 4 — LIABILITY CAP
The Vendor's total aggregate liability under this Agreement shall not exceed fifty thousand US dollars ($50,000). In no event shall either party be liable for any indirect, incidental, special, consequential, or punitive damages arising out of or related to this Agreement.

CLAUSE 5 — TERMINATION
Either party may terminate this Agreement for cause upon thirty (30) days' prior written notice to the other party if the other party materially breaches this Agreement and fails to cure such breach within the notice period.

CLAUSE 6 — CONFIDENTIALITY
Each party agrees to maintain the confidentiality of all proprietary and confidential information disclosed by the other party during the term of this Agreement. This obligation shall survive termination for a period of two (2) years.""",

        "client_contract": """SOFTWARE SERVICE AGREEMENT

This Software Service Agreement ("Agreement") is entered into as of the date of last signature below.

CLAUSE 1 — SCOPE OF SERVICES
The Vendor shall provide the Client with access to its cloud-based software platform ("Service"), including all standard features, maintenance updates, and technical support as described in the attached Service Level Agreement.

CLAUSE 2 — PAYMENT TERMS
All invoices shall be due and payable within sixty (60) days of the invoice date ("Net-60"). Late payments shall accrue interest at a rate of 1.0% per month. The Client shall be responsible for all applicable taxes and fees associated with the Service.

CLAUSE 3 — TERM AND RENEWAL
This Agreement shall be effective for an initial term of twelve (12) months from the Effective Date and shall automatically renew for successive twelve (12) month periods unless either party provides written notice of non-renewal at least thirty (30) days prior to the end of the then-current term.

CLAUSE 4 — LIABILITY CAP
The Vendor's total aggregate liability under this Agreement shall not exceed ten thousand US dollars ($10,000). In no event shall either party be liable for any indirect, incidental, special, consequential, or punitive damages arising out of or related to this Agreement.

CLAUSE 5 — TERMINATION
Either party may terminate this Agreement for cause upon ninety (90) days' prior written notice to the other party if the other party materially breaches this Agreement and fails to cure such breach within the notice period.

CLAUSE 6 — CONFIDENTIALITY
Each party agrees to maintain the confidentiality of all proprietary and confidential information disclosed by the other party during the term of this Agreement. This obligation shall survive termination for a period of two (2) years.""",

        "ground_truth_conflicts": [
            {
                "clause_id": "clause_2",
                "clause_name": "Payment Terms",
                "vendor_text": "All invoices shall be due and payable within thirty (30) days of the invoice date (\"Net-30\"). Late payments shall accrue interest at a rate of 1.5% per month.",
                "client_text": "All invoices shall be due and payable within sixty (60) days of the invoice date (\"Net-60\"). Late payments shall accrue interest at a rate of 1.0% per month.",
                "conflict_type": "payment_timeline"
            },
            {
                "clause_id": "clause_4",
                "clause_name": "Liability Cap",
                "vendor_text": "The Vendor's total aggregate liability under this Agreement shall not exceed fifty thousand US dollars ($50,000).",
                "client_text": "The Vendor's total aggregate liability under this Agreement shall not exceed ten thousand US dollars ($10,000).",
                "conflict_type": "financial_limit"
            },
            {
                "clause_id": "clause_5",
                "clause_name": "Termination",
                "vendor_text": "Either party may terminate this Agreement for cause upon thirty (30) days' prior written notice.",
                "client_text": "Either party may terminate this Agreement for cause upon ninety (90) days' prior written notice.",
                "conflict_type": "notice_period"
            }
        ],
        "non_negotiable_clauses": [],
        "max_steps": 5
    },

    "task_medium": {
        "vendor_contract": """DATA PROCESSING AGREEMENT

This Data Processing Agreement ("DPA") is entered into pursuant to and in accordance with the General Data Protection Regulation (EU) 2016/679 ("GDPR") and applicable data protection laws.

CLAUSE 1 — DEFINITIONS
"Personal Data" means any information relating to an identified or identifiable natural person. "Processing" means any operation performed on Personal Data, including collection, recording, storage, adaptation, retrieval, consultation, use, disclosure, erasure, or destruction.

CLAUSE 2 — SCOPE OF PROCESSING
The Data Processor shall process Personal Data only on documented instructions from the Data Controller, including with regard to transfers of Personal Data to a third country, unless required to do so by Union or Member State law.

CLAUSE 3 — DATA RETENTION
The Data Processor shall retain Personal Data for a maximum period of two (2) years from the date of collection, after which all Personal Data shall be securely deleted or anonymized. Retention extensions require written authorization from the Data Controller.

CLAUSE 4 — SUB-PROCESSOR APPROVAL
The Data Processor shall provide the Data Controller with thirty (30) days' advance written notice of any intended addition or replacement of sub-processors. If the Data Controller does not object within the notice period, the sub-processor engagement shall be deemed approved.

CLAUSE 5 — DATA BREACH NOTIFICATION
In the event of a Personal Data breach, the Data Processor shall notify the Data Controller without undue delay, and in any event within seventy-two (72) hours of becoming aware of the breach. The notification shall include the nature of the breach, categories of data affected, and proposed remediation measures.

CLAUSE 6 — AUDIT RIGHTS
The Data Controller shall have the right to conduct audits of the Data Processor's processing activities on an annual basis, with at least thirty (30) days' prior written notice. Audits shall be conducted during normal business hours and shall not unreasonably disrupt the Data Processor's operations.

CLAUSE 7 — DATA SECURITY
The Data Processor shall implement appropriate technical and organizational measures to ensure a level of security appropriate to the risk, including encryption of Personal Data at rest and in transit, regular security testing, access controls, and staff training.

CLAUSE 8 — INTERNATIONAL TRANSFERS
Any transfer of Personal Data to a third country shall only take place subject to appropriate safeguards as provided under Chapter V of the GDPR, including Standard Contractual Clauses or Binding Corporate Rules.""",

        "client_contract": """DATA PROCESSING AGREEMENT

This Data Processing Agreement ("DPA") is entered into pursuant to and in accordance with the General Data Protection Regulation (EU) 2016/679 ("GDPR") and applicable data protection laws.

CLAUSE 1 — DEFINITIONS
"Personal Data" means any information relating to an identified or identifiable natural person. "Processing" means any operation performed on Personal Data, including collection, recording, storage, adaptation, retrieval, consultation, use, disclosure, erasure, or destruction.

CLAUSE 2 — SCOPE OF PROCESSING
The Data Processor shall process Personal Data only on documented instructions from the Data Controller, including with regard to transfers of Personal Data to a third country, unless required to do so by Union or Member State law.

CLAUSE 3 — DATA RETENTION
The Data Processor shall retain Personal Data for a maximum period of six (6) months from the date of collection, after which all Personal Data shall be securely deleted or anonymized. No retention extensions shall be permitted without a formal amendment to this DPA signed by both parties.

CLAUSE 4 — SUB-PROCESSOR APPROVAL
The Data Processor shall not engage any sub-processor without the explicit prior written approval of the Data Controller for each specific sub-processor. The Data Controller retains the absolute right to reject any proposed sub-processor without providing reasons.

CLAUSE 5 — DATA BREACH NOTIFICATION
In the event of a Personal Data breach, the Data Processor shall notify the Data Controller without undue delay, and in any event within twenty-four (24) hours of becoming aware of the breach. The notification shall include the nature of the breach, categories of data affected, proposed remediation measures, and a preliminary impact assessment.

CLAUSE 6 — AUDIT RIGHTS
The Data Controller shall have the right to conduct audits of the Data Processor's processing activities on demand at any time, with reasonable prior notice of no less than five (5) business days. The Data Processor shall provide full cooperation and access to all relevant facilities, systems, and documentation.

CLAUSE 7 — DATA SECURITY
The Data Processor shall implement appropriate technical and organizational measures to ensure a level of security appropriate to the risk, including encryption of Personal Data at rest and in transit, regular security testing, access controls, and staff training.

CLAUSE 8 — INTERNATIONAL TRANSFERS
Any transfer of Personal Data to a third country shall only take place subject to appropriate safeguards as provided under Chapter V of the GDPR, including Standard Contractual Clauses or Binding Corporate Rules.""",

        "ground_truth_conflicts": [
            {
                "clause_id": "clause_3",
                "clause_name": "Data Retention",
                "vendor_text": "The Data Processor shall retain Personal Data for a maximum period of two (2) years from the date of collection.",
                "client_text": "The Data Processor shall retain Personal Data for a maximum period of six (6) months from the date of collection.",
                "conflict_type": "retention_period"
            },
            {
                "clause_id": "clause_4",
                "clause_name": "Sub-Processor Approval",
                "vendor_text": "The Data Processor shall provide the Data Controller with thirty (30) days' advance written notice of any intended addition or replacement of sub-processors.",
                "client_text": "The Data Processor shall not engage any sub-processor without the explicit prior written approval of the Data Controller for each specific sub-processor.",
                "conflict_type": "approval_mechanism"
            },
            {
                "clause_id": "clause_5",
                "clause_name": "Breach Notification",
                "vendor_text": "The Data Processor shall notify the Data Controller without undue delay, and in any event within seventy-two (72) hours of becoming aware of the breach.",
                "client_text": "The Data Processor shall notify the Data Controller without undue delay, and in any event within twenty-four (24) hours of becoming aware of the breach.",
                "conflict_type": "notification_window"
            },
            {
                "clause_id": "clause_6",
                "clause_name": "Audit Rights",
                "vendor_text": "The Data Controller shall have the right to conduct audits of the Data Processor's processing activities on an annual basis.",
                "client_text": "The Data Controller shall have the right to conduct audits of the Data Processor's processing activities on demand at any time.",
                "conflict_type": "audit_frequency"
            }
        ],
        "non_negotiable_clauses": ["clause_3"],
        "max_steps": 8
    },

    "task_hard": {
        "vendor_contract": """ENTERPRISE TECHNOLOGY PARTNERSHIP AGREEMENT

This Enterprise Technology Partnership Agreement ("Agreement") is entered into by and between the parties identified on the signature page hereto.

CLAUSE 1 — PARTNERSHIP SCOPE
The parties agree to collaborate on the joint development, marketing, and distribution of integrated technology solutions combining the Vendor's proprietary platform with the Client's distribution network and customer base.

CLAUSE 2 — INTELLECTUAL PROPERTY OWNERSHIP
All intellectual property created jointly during the term of this Agreement shall be jointly owned by both parties, with each party having the unrestricted right to use, license, and sublicense such joint IP independently without the consent of or accounting to the other party.

CLAUSE 3 — REVENUE SHARING
The parties shall share net revenues generated from jointly developed solutions as follows: Vendor shall receive eighty percent (80%) and Client shall receive twenty percent (20%) of net revenues, calculated quarterly and payable within forty-five (45) days of quarter end.

CLAUSE 4 — EXCLUSIVITY
During the term of this Agreement and for a period of twelve (12) months following termination, neither party shall enter into a substantially similar partnership agreement with a direct competitor of the other party within the same market segment.

CLAUSE 5 — TERM AND RENEWAL
This Agreement shall have an initial term of three (3) years from the Effective Date, with automatic renewal for successive one (1) year periods unless either party provides written notice of non-renewal at least ninety (90) days prior to expiration.

CLAUSE 6 — GOVERNING LAW
This Agreement shall be governed by and construed in accordance with the laws of the State of Delaware, without regard to its conflict of laws principles. Any disputes shall be resolved through binding arbitration in Wilmington, Delaware.

CLAUSE 7 — SERVICE LEVEL AGREEMENT
The Vendor guarantees a platform uptime of 99.9% measured monthly. In the event of failure to meet this SLA, the Client shall receive a service credit equal to five percent (5%) of the monthly fees for each full percentage point below the guaranteed uptime level.

CLAUSE 8 — CONFIDENTIALITY
All confidential information exchanged between the parties shall be protected for a period of five (5) years from the date of disclosure. Neither party shall disclose confidential information to any third party without prior written consent.

CLAUSE 9 — INDEMNIFICATION
Each party shall indemnify, defend, and hold harmless the other party from and against any third-party claims arising from the indemnifying party's negligence, willful misconduct, or breach of this Agreement.

CLAUSE 10 — FORCE MAJEURE
Neither party shall be liable for failure to perform obligations under this Agreement due to events beyond reasonable control, including acts of God, war, terrorism, government actions, natural disasters, fire, flood, or epidemic.

CLAUSE 11 — DATA PROTECTION
Both parties shall comply with all applicable data protection laws, including GDPR and CCPA, with respect to any personal data processed in connection with this Agreement.

CLAUSE 12 — LIMITATION OF LIABILITY
Except for breaches of confidentiality or IP obligations, neither party's total aggregate liability shall exceed the total fees paid or payable under this Agreement during the twelve (12) months preceding the claim.""",

        "client_contract": """ENTERPRISE TECHNOLOGY PARTNERSHIP AGREEMENT

This Enterprise Technology Partnership Agreement ("Agreement") is entered into by and between the parties identified on the signature page hereto.

CLAUSE 1 — PARTNERSHIP SCOPE
The parties agree to collaborate on the joint development, marketing, and distribution of integrated technology solutions combining the Vendor's proprietary platform with the Client's distribution network and customer base.

CLAUSE 2 — INTELLECTUAL PROPERTY OWNERSHIP
All intellectual property created during the term of this Agreement, whether jointly or independently in connection with the partnership, shall be owned exclusively by the Client. The Vendor shall retain a non-exclusive, royalty-free license to use such IP solely for the purpose of performing its obligations under this Agreement.

CLAUSE 3 — REVENUE SHARING
The parties shall share net revenues generated from jointly developed solutions as follows: Vendor shall receive ninety percent (90%) and Client shall receive ten percent (10%) of net revenues, calculated quarterly and payable within thirty (30) days of quarter end.

CLAUSE 4 — EXCLUSIVITY
During the term of this Agreement and for a period of six (6) months following termination, neither party shall enter into a substantially similar partnership agreement with a direct competitor of the other party within the same market segment.

CLAUSE 5 — TERM AND RENEWAL
This Agreement shall have an initial term of three (3) years from the Effective Date, with automatic renewal for successive one (1) year periods unless either party provides written notice of non-renewal at least ninety (90) days prior to expiration.

CLAUSE 6 — GOVERNING LAW
This Agreement shall be governed by and construed in accordance with the laws of the State of California, without regard to its conflict of laws principles. Any disputes shall be resolved through binding arbitration in San Francisco, California.

CLAUSE 7 — SERVICE LEVEL AGREEMENT
The Vendor guarantees a platform uptime of 99.9% measured monthly. In the event of failure to meet this SLA, the Client shall receive a service credit equal to fifteen percent (15%) of the monthly fees for each full percentage point below the guaranteed uptime level.

CLAUSE 8 — CONFIDENTIALITY
All confidential information exchanged between the parties shall be protected for a period of five (5) years from the date of disclosure. Neither party shall disclose confidential information to any third party without prior written consent.

CLAUSE 9 — INDEMNIFICATION
Each party shall indemnify, defend, and hold harmless the other party from and against any third-party claims arising from the indemnifying party's negligence, willful misconduct, or breach of this Agreement.

CLAUSE 10 — FORCE MAJEURE
Neither party shall be liable for failure to perform obligations under this Agreement due to events beyond reasonable control, including but not limited to acts of God, war, terrorism, government actions, natural disasters, fire, flood, epidemic, pandemic, supply chain disruptions, semiconductor shortages, critical infrastructure failures, and labor disputes or strikes.

CLAUSE 11 — DATA PROTECTION
Both parties shall comply with all applicable data protection laws, including GDPR and CCPA, with respect to any personal data processed in connection with this Agreement.

CLAUSE 12 — LIMITATION OF LIABILITY
Except for breaches of confidentiality or IP obligations, neither party's total aggregate liability shall exceed the total fees paid or payable under this Agreement during the twelve (12) months preceding the claim.""",

        "ground_truth_conflicts": [
            {
                "clause_id": "clause_2",
                "clause_name": "Intellectual Property Ownership",
                "vendor_text": "All intellectual property created jointly during the term of this Agreement shall be jointly owned by both parties, with each party having the unrestricted right to use, license, and sublicense such joint IP independently.",
                "client_text": "All intellectual property created during the term of this Agreement shall be owned exclusively by the Client. The Vendor shall retain a non-exclusive, royalty-free license.",
                "conflict_type": "ip_ownership"
            },
            {
                "clause_id": "clause_3",
                "clause_name": "Revenue Share",
                "vendor_text": "Vendor shall receive eighty percent (80%) and Client shall receive twenty percent (20%) of net revenues.",
                "client_text": "Vendor shall receive ninety percent (90%) and Client shall receive ten percent (10%) of net revenues.",
                "conflict_type": "revenue_split"
            },
            {
                "clause_id": "clause_4",
                "clause_name": "Exclusivity",
                "vendor_text": "For a period of twelve (12) months following termination.",
                "client_text": "For a period of six (6) months following termination.",
                "conflict_type": "exclusivity_window"
            },
            {
                "clause_id": "clause_6",
                "clause_name": "Governing Law",
                "vendor_text": "Governed by the laws of the State of Delaware. Arbitration in Wilmington, Delaware.",
                "client_text": "Governed by the laws of the State of California. Arbitration in San Francisco, California.",
                "conflict_type": "jurisdiction"
            },
            {
                "clause_id": "clause_7",
                "clause_name": "SLA Penalties",
                "vendor_text": "Service credit equal to five percent (5%) of the monthly fees for each full percentage point below the guaranteed uptime level.",
                "client_text": "Service credit equal to fifteen percent (15%) of the monthly fees for each full percentage point below the guaranteed uptime level.",
                "conflict_type": "penalty_rate"
            },
            {
                "clause_id": "clause_10",
                "clause_name": "Force Majeure",
                "vendor_text": "Events beyond reasonable control, including acts of God, war, terrorism, government actions, natural disasters, fire, flood, or epidemic.",
                "client_text": "Events beyond reasonable control, including but not limited to acts of God, war, terrorism, government actions, natural disasters, fire, flood, epidemic, pandemic, supply chain disruptions, semiconductor shortages, critical infrastructure failures, and labor disputes or strikes.",
                "conflict_type": "scope_definition"
            }
        ],
        "non_negotiable_clauses": ["clause_2", "clause_6"],
        "max_steps": 12
    }
}
