from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute
from utils import DEV_PROD_VALUE

class TeamModel(Model):

    class Meta:
        table_name = DEV_PROD_VALUE('dev_esf_team', 'prod_esf_team')
        region = 'us-west-1'
    address = UnicodeAttribute(hash_key=True)
    total_staked_ether = NumberAttribute(range_key=True, default=0)
    name = UnicodeAttribute(null=True)
    description = UnicodeAttribute(null=True)
    logo_url = UnicodeAttribute(null=True)
    total_accounts_staked = NumberAttribute(null=True)
