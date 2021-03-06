import os
from teams.TeamModel import TeamModel
import random

stage = os.environ.get('stage')

assert(stage != 'prod')

with TeamModel.batch_write() as batch:
    for i in range(10):
        new_team = TeamModel(
            f'tx{i}',
            team_id=i,
            address=f'0x{i}',
            total_staked_ether=random.randrange(0, 20) + random.random(),
            name=f'Team{i}',
            description=f'Putting the number {i} on the blockchain',
            picture_url='https://i.imgur.com/ksZnH0k.jpg',
            project_link='https://stably.io',
            total_bets_made=random.randint(0, 100),
            mined=True,
        )

        batch.save(new_team)
