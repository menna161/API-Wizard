import os
import time
import argparse
import random
import shogi.Ayane as ayane


def AyaneruGate():
    parser = argparse.ArgumentParser('ayaneru-gate.py')
    parser.add_argument('--time', type=str, default='byoyomi 100', help='持ち時間設定 AyaneruServer.set_time_setting()の引数と同じ。')
    parser.add_argument('--home', type=str, default='AyaneruGate', help='home folder')
    parser.add_argument('--iteration', type=int, default=10, help='number of iterations')
    parser.add_argument('--loop', type=int, default=10, help='number of games')
    parser.add_argument('--cores', type=int, default=8, help='cpu cores(number of logical threads)')
    parser.add_argument('--flip_turn', type=bool, default=True, help='flip turn every game')
    parser.add_argument('--book_file', type=str, default='book/records2016_10818.sfen', help='book filepath')
    parser.add_argument('--start_gameply', type=int, default=24, help='start game ply in the book')
    args = parser.parse_args()
    print('home           : {0}'.format(args.home))
    print('iteration      : {0}'.format(args.iteration))
    print('loop           : {0}'.format(args.loop))
    print('cores          : {0}'.format(args.cores))
    print('time           : {0}'.format(args.time))
    print('flip_turn      : {0}'.format(args.flip_turn))
    print('book file      : {0}'.format(args.book_file))
    print('start_gameply  : {0}'.format(args.start_gameply))
    home = args.home
    log = ayane.Log(os.path.join(home, 'log'))
    log.print('iteration start', output_datetime=True)
    engines_folder = os.path.join(home, 'engines')
    if (not os.path.exists(engines_folder)):
        print('Error : {0} folder is not exist.'.format(engines_folder))
        return
    engine_infos = []
    for engine_rel_path in os.listdir(engines_folder):
        info = EngineInfo()
        info.engine_folder = engine_rel_path
        info.read_engine_define(home)
        engine_infos.append(info)
    if False:
        print('engines        :')
        for (i, engine_info) in enumerate(engine_infos):
            print('== Engine {0} =='.format(i))
            engine_info.print()
    non_fixed_rating_engines = 0
    for info in engine_infos:
        if (not info.rating_fix):
            non_fixed_rating_engines += 1
    if (non_fixed_rating_engines < 2):
        print('Error! : non fixed rating engine < 2')
        raise ValueError()

    def output_engine_rating():
        nonlocal log, engine_infos
        log.print('== engine rating list ==', also_print=True)
        for info in engine_infos:
            log.print('engine : {0} , rating = {1} , rating_fix = {2} , threads = {3}'.format(info.engine_display_name, info.rating, info.rating_fix, info.engine_threads), also_print=True)
    output_engine_rating()
    for it in range(args.iteration):
        log.print('iteration : {0}'.format(it), output_datetime=True)
        server = ayane.MultiAyaneruServer()
        info1 = None
        info2 = None
        while True:
            num_of_engines = len(engine_infos)
            p1 = random.randint(0, (num_of_engines - 1))
            p2 = random.randint(0, (num_of_engines - 1))
            if (p1 == p2):
                continue
            if (p1 > p2):
                (p1, p2) = (p2, p1)
            info1 = engine_infos[p1]
            info2 = engine_infos[p2]
            if (info1.rating_fix and info2.rating_fix):
                continue
            break
        log.print('engine : {0} vs {1}'.format(info1.engine_display_name, info2.engine_display_name), also_print=True)
        engine1 = info1.engine_exe_fullpath(home)
        engine2 = info2.engine_exe_fullpath(home)
        thread1 = info1.engine_threads
        thread2 = info2.engine_threads
        thread_total = max(thread1, thread2)
        cores = max((args.cores - 2), 1)
        game_server_num = int((cores / thread_total))
        server.init_server(game_server_num)
        options_common = {'NetworkDelay': '0', 'NetworkDelay2': '0', 'MaxMovesToDraw': '320', 'MinimumThinkingTime': '0', 'BookFile': 'no_book'}
        server.init_engine(0, engine1, options_common)
        server.init_engine(1, engine2, options_common)
        server.set_time_setting(args.time)
        server.flip_turn_every_game = args.flip_turn
        if (args.book_file is None):
            start_sfens = ['startpos']
        else:
            book_filepath = os.path.join(home, args.book_file)
            with open(book_filepath) as f:
                start_sfens = f.readlines()
        server.start_sfens = start_sfens
        server.start_gameply = args.start_gameply
        if (thread1 == thread2):
            game_setting_str = 't{0}'.format(thread1)
        else:
            game_setting_str = 't{0},{1}'.format(thread1, thread2)
        game_setting_str += args.time.replace('byoyomi', 'b').replace('time', 't').replace('inc', 'i').replace(' ', '')
        last_total_games = 0
        loop = args.loop

        def output_info():
            nonlocal last_total_games, server, log
            if (last_total_games != server.total_games):
                last_total_games = server.total_games
                log.print(((game_setting_str + '.') + server.game_info()))
        server.game_start()
        while (server.total_games < loop):
            output_info()
            time.sleep(1)
        output_info()
        server.game_stop()
        for kifu in server.game_kifus:
            log.print('game sfen = {0} , flip_turn = {1} , game_result = {2}'.format(kifu.sfen, kifu.flip_turn, str(kifu.game_result)), also_print=False)
        elo = server.game_rating()
        rating_diff = elo.rating
        rating_diff = min(max(rating_diff, (- loop)), loop)
        player1_add = 0
        player2_add = 0
        if info1.rating_fix:
            player2_add = (- rating_diff)
        elif info2.rating_fix:
            player1_add = (+ rating_diff)
        else:
            player1_add = (+ int((rating_diff / 2)))
            player2_add = (- int((rating_diff / 2)))
        log.print('Player1 : {0} , rating {1} -> {2}'.format(info1.engine_display_name, info1.rating, (info1.rating + player1_add)), also_print=True)
        log.print('Player2 : {0} , rating {1} -> {2}'.format(info2.engine_display_name, info2.rating, (info2.rating + player2_add)), also_print=True)
        info1.rating += player1_add
        info2.rating += player2_add
        if (player1_add != 0):
            info1.write_engine_define(home)
        if (player2_add != 0):
            info2.write_engine_define(home)
    output_engine_rating()
    log.print('iteration end', also_print=True, output_datetime=True)
    server.terminate()
    log.close()
