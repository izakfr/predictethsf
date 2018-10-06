from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute
from utils import DEV_PROD_VALUE

class TeamModel(Model):

    class Meta:
        table_name = DEV_PROD_VALUE('dev_esf_team', 'prod_esf_team')
        region = 'us-west-1'
    team_index = NumberAttribute(hash_key=True)
    address = UnicodeAttribute(null=True)
    total_staked_ether = NumberAttribute(default=0)
    name = UnicodeAttribute(null=True)
    description = UnicodeAttribute(null=True)
    picture_url = UnicodeAttribute(null=True)
    project_link = UnicodeAttribute(null=True)
    total_accounts_staked = NumberAttribute(default=0)

    def __iter__(self):
        for name, attr in self._get_attributes().items():
            yield name, attr.serialize(getattr(self, name))