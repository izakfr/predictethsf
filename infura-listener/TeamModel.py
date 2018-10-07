from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, BooleanAttribute
import os

def DEV_PROD_VALUE(dev_value, prod_value):
    stage = os.environ.get('stage')
    if stage == 'prod':
        return prod_value
    return dev_value

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
    total_bets_made = NumberAttribute(default=0)
    mined = BooleanAttribute(default=False)

    def __iter__(self):
        for name, attr in self._get_attributes().items():
            yield name, attr.serialize(getattr(self, name))
    