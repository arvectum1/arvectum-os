from datetime import datetime, timezone
import unittest

from arvectum_os_ref.canonical import AuthorityMode
from arvectum_os_ref.organizational_asset_admission import (
    ORGANIZATIONAL_ASSET_DESIGNATION_AUTHORITY_SCOPE,
    ORGANIZATIONAL_ASSET_DESIGNATION_SEMANTIC_TYPE,
)
from arvectum_os_ref.product_contract import CanonicalAccessMode
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.identity import Identity
from p10_03_company_asset_ref.contract import build_p10_03_product_contract_projection


class P1003AssetDesignationContractBoundaryTests(unittest.TestCase):
    def test_both_admission_operations_declare_separate_designation_write(self) -> None:
        scope = "p10-03-designation-boundary"
        organization = OrganizationScope(Identity("organization", scope, "platform"))
        actor = ActorContext(
            Principal(Identity("principal", "owner", scope)),
            organization,
        )
        contract = build_p10_03_product_contract_projection(
            actor=actor,
            created_at=datetime(2026, 8, 28, 9, 30, tzinfo=timezone.utc),
        )
        for operation in contract.operations:
            matches = [
                access
                for access in operation.canonical_accesses
                if access.semantic_type == ORGANIZATIONAL_ASSET_DESIGNATION_SEMANTIC_TYPE
                and access.authority_mode is AuthorityMode.NATIVE
                and access.authority_scope == ORGANIZATIONAL_ASSET_DESIGNATION_AUTHORITY_SCOPE
                and CanonicalAccessMode.WRITE in access.access_modes
            ]
            self.assertEqual(
                len(matches),
                1,
                f"{operation.operation_name} must declare exactly one designation write boundary",
            )


if __name__ == "__main__":
    unittest.main()
