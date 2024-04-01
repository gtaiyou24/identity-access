from dataclasses import dataclass


@dataclass(init=True, unsafe_hash=True, frozen=True)
class ProvisionTenantCommand:
    tenant_name: str
    tenant_description: str
    administor_first_name: str
    administor_last_name: str
    email_address: str
    primary_telephone: str
    secondary_telephone: str
    address_street_address: str
    address_city: str
    address_state_province: str
    address_postal_code: str
    address_country_code: str
