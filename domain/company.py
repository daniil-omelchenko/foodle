from domain.serializable import Serializable


class CompanySettings(Serializable):
    def __init__(self, company_name, currency_code_iso, logo, address, phone):
        self.company_name = company_name
        self.currency = currency_code_iso
        self.logo_url = logo
        self.address = address
        self.phone = phone

    def serialize(self):
        return {
            'company_name': self.company_name,
            'currency': self.currency,
            'logo_url': self.logo_url,
            'address': self.address,
            'phone': self.phone
        }

    @classmethod
    def deserialize(cls, data, account=None):
        return CompanySettings(
            company_name=data['company_name'],
            currency_code_iso=data['currency_code_iso'],
            logo='https://{}.joinposter.com{}'.format(account, data['logo']) if account else data['logo'],
            address=data['FIZ_ADRESS_CITY'],
            phone=data['FIZ_ADRESS_PHONE']
        )
