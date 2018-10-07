from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
from pynamodb.attributes import NumberAttribute

class TeamIdIndex(GlobalSecondaryIndex):

    class Meta:
        projection = AllProjection()
        read_capacity_units=1 
        write_capacity_units=1

    team_id = NumberAttribute(hash_key=True)
