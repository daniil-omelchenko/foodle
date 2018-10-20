import requests
from domain.company import CompanySettings


def get_company_settings(account, token):
    # type: (str) -> CompanySettings
    r = requests.post('https://{}.joinposter.com/api/settings.getAllSettings?token'.format(account, token))
    settings = r.json().get('response')
    company_settings = CompanySettings.deserialize(settings, account)
    return company_settings

