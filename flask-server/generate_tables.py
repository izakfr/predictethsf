from teams.TeamModel import TeamModel

if not TeamModel.exists():
    TeamModel.create_table(read_capacity_units=1, write_capacity_units=1)
