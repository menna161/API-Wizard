


def parse_file(self, year):
    '\n        Will parse the file respective for one year.\n        - It will first look for the file in current directory\n        - Else, it will take from the web (without making a copy)\n        '
    event = Event()
    filename = '{0}eve{1}'.format(year, self.extension)
    try:
        zipfile = ZipFile(filename)
        self.log.debug('Found locally')
    except:
        resp = urlopen((self.endpoint + filename))
        zipfile = ZipFile(BytesIO(resp.read()))
        self.log.debug('Donwloading from the web')
    (infos, starting, plays, er, subs, comments, rosters, teams, metadata) = ([] for i in range(9))
    for file in zipfile.namelist():
        metadata.append([file, datetime.datetime.now(), __version__])
        if (file[:4] == 'TEAM'):
            for row in zipfile.open(file).readlines():
                row = row.decode('utf-8')
                team_piece = []
                for i in range(4):
                    team_piece.append(row.rstrip('\n').split(',')[i].replace('\r', ''))
                teams.append(([year] + team_piece))
        elif (file[(- 3):] == 'ROS'):
            for row in zipfile.open(file, 'r').readlines():
                row = row.decode('utf-8')
                roster_piece = []
                for i in range(7):
                    roster_piece.append(row.rstrip('\n').split(',')[i].replace('\r', ''))
                rosters.append(([year] + roster_piece))
        else:
            (order, game_id, version, runs) = (0 for i in range(4))
            inning = '1'
            team = '0'
            file_lines = zipfile.open(file, 'r').readlines()
            for (loop, row) in enumerate(file_lines):
                row = row.decode('utf-8')
                row_type = row.rstrip('\n').split(',')[0]
                if (row_type == 'id'):
                    order = 0
                    game_id = row.rstrip('\n').split(',')[1].strip('\r')
                    event.play = {'B': 1, '1': 0, '2': 0, '3': 0, 'H': 0, 'out': 3, 'run': 0}
                    home_team_score = 0
                    away_team_score = 0
                    infos.append([game_id, '__version__', __version__])
                    infos.append([game_id, 'file', file])
                if (row_type == 'version'):
                    version = row.rstrip('\n').split(',')[1].strip('\r')
                if (row_type == 'info'):
                    var = row.rstrip('\n').split(',')[1]
                    value = row.rstrip('\n').split(',')[2].replace('\r', '').replace('"', '')
                    value = (None if (value == 'unknown') else value)
                    value = (None if ((value == 0) and (var == 'temp')) else value)
                    value = (None if ((value == (- 1)) and (var == 'windspeed')) else value)
                    infos.append([game_id, var, value])
                if (row_type == 'start'):
                    if (row.rstrip('\n').split(',')[5].strip('\r') == '1'):
                        if (row.rstrip('\n').split(',')[3] == '1'):
                            home_pitcher_id = row.rstrip('\n').split(',')[1]
                            home_pitch_count = 0
                        else:
                            away_pitcher_id = row.rstrip('\n').split(',')[1]
                            away_pitch_count = 0
                    start_piece = []
                    for i in range(1, 6, 1):
                        start_piece.append(row.rstrip('\n').split(',')[i].replace('"', '').replace('\r', ''))
                    '\n                        start_piece = [\n                            row.rstrip(\'\n\').split(\',\')[1],\n                            row.rstrip(\'\n\').split(\',\')[2].strip(\'"\'),\n                            row.rstrip(\'\n\').split(\',\')[3],\n                            row.rstrip(\'\n\').split(\',\')[4],\n                            row.rstrip(\'\n\').split(\',\')[5].strip(\'\r\')\n                        ]\n                        '
                    starting.append(([game_id, version] + start_piece))
                if (row_type == 'play'):
                    if (team != row.rstrip('\n').split(',')[2]):
                        runs = 0
                        if ((not (row.rstrip('\n').split(',')[2] == '0')) and (not (row.rstrip('\n').split(',')[1] == '1'))):
                            if (event.play['out'] != 3):
                                self.errors.append('Game: {3} Inning {0} team {4} ended with {1} outs [{2}]'.format(inning, event.play['out'], event.str, game_id, team))
                                event.play['out'] = 0
                    event.str = row.rstrip('\n').split(',')[6].strip('\r')
                    event.decipher()
                    if (row.rstrip('\n').split(',')[2] == '0'):
                        pitcher_id = home_pitcher_id
                        home_pitch_count = self._pitch_count(row.rstrip('\n').split(',')[5], home_pitch_count)
                        pitch_count = home_pitch_count
                        away_team_score = ((away_team_score + event.play['run']) - runs)
                    elif (row.rstrip('\n').split(',')[2] == '1'):
                        pitcher_id = away_pitcher_id
                        away_pitch_count = self._pitch_count(row.rstrip('\n').split(',')[5], away_pitch_count)
                        pitch_count = away_pitch_count
                        home_team_score = ((home_team_score + event.play['run']) - runs)
                    inning = row.rstrip('\n').split(',')[1]
                    team = row.rstrip('\n').split(',')[2]
                    runs = event.play['run']
                    play_piece = [inning, team, pitcher_id, pitch_count, row.rstrip('\n').split(',')[3], row.rstrip('\n').split(',')[4], row.rstrip('\n').split(',')[5], row.rstrip('\n').split(',')[6].strip('\r'), event.play['B'], event.play['1'], event.play['2'], event.play['3'], event.play['H'], event.play['run'], event.play['out'], away_team_score, home_team_score]
                    plays.append(([order, game_id, version] + play_piece))
                    order += 1
                if (row_type == 'sub'):
                    if (row.rstrip('\n').split(',')[5].strip('\r') == '1'):
                        if (row.rstrip('\n').split(',')[3] == '1'):
                            home_pitcher_id = row.rstrip('\n').split(',')[1]
                            home_pitch_count = 0
                        else:
                            away_pitcher_id = row.rstrip('\n').split(',')[1]
                            away_pitch_count = 0
                    sub_piece = [row.rstrip('\n').split(',')[1], row.rstrip('\n').split(',')[2].strip('"'), row.rstrip('\n').split(',')[3], row.rstrip('\n').split(',')[4], row.rstrip('\n').split(',')[5].strip('\r')]
                    subs.append(([order, game_id, version] + sub_piece))
                    order += 1
                if (row_type == 'com'):
                    com_piece = [row.rstrip('\n').split('"')[1]]
                    comments.append(([order, game_id, version] + com_piece))
                if (row_type == 'data'):
                    infos.append([game_id, 'hometeam_score', home_team_score])
                    infos.append([game_id, 'awayteam_score', away_team_score])
                    data_piece = [row.rstrip('\n').split(',')[1], row.rstrip('\n').split(',')[2], row.rstrip('\n').split(',')[3].strip('\r')]
                    er.append(([game_id, version] + data_piece))
    rosters_df = pd.DataFrame(rosters, columns=['year', 'player_id', 'last_name', 'first_name', 'batting_hand', 'throwing_hand', 'team_abbr_1', 'position'])
    teams_df = pd.DataFrame(teams, columns=['year', 'team_abbr', 'league', 'city', 'name'])
    info = pd.DataFrame(infos, columns=['game_id', 'var', 'value'])
    games = info[(~ info.duplicated(subset=['game_id', 'var'], keep='last'))].pivot('game_id', 'var', 'value').reset_index()
    starting_df = pd.DataFrame(starting, columns=['game_id', 'version', 'player_id', 'player_name', 'home_team', 'batting_position', 'fielding_position'])
    subs_df = pd.DataFrame(subs, columns=['order', 'game_id', 'version', 'player_id', 'player_name', 'home_team', 'batting_position', 'position'])
    plays_df = pd.DataFrame(plays, columns=['order', 'game_id', 'version', 'inning', 'home_team', 'pitcher_id', 'pitch_count', 'batter_id', 'count_on_batter', 'pitches', 'play', 'B', '1', '2', '3', 'H', 'run', 'out', 'away_score', 'home_score'])
    comments_df = pd.DataFrame(comments, columns=['order', 'game_id', 'version', 'comment'])
    er_df = pd.DataFrame(er, columns=['game_id', 'version', 'earned_run', 'player_id', 'variable'])
    metadata_df = pd.DataFrame(metadata, columns=['file', 'datetime', 'version'])
    return (games, starting_df, plays_df, er_df, subs_df, comments_df, rosters_df, teams_df, metadata_df)
