import sys
import datetime
import shutil
from tkinter import Tk, _tkinter, StringVar, Label, Menu, Toplevel, messagebox
import visu
import g_eng
import score
import replay
import keybuf
import rate


def updater(self):
    draw_rate = rate.Rate((1 / 25.0))
    game_rate = rate.Rate((1 / 2.0))
    update_rate = rate.Rate((1 / 50.0))
    replay_rate = rate.Rate((1 / 2.0))
    self.replay.reset_replay_file()
    while True:
        if replay_rate.is_time():
            self.replay.play_frames()
        if draw_rate.is_time():
            self.draw()
        if game_rate.is_time():
            if (self.paused or (self.game.state == g_eng.GameEngine.gamestate_game_over)):
                pass
            else:
                self.areas[0].clear_text()
                next_dir = self.key_buffer.get_key()
                if next_dir:
                    self.game.snake.change_dir(next_dir)
                self.game.routine()
                self.replay.save_replay_frame(self.game)
                self.score_str.set(('Score: ' + str(self.game.score)))
                if (self.game.state == g_eng.GameEngine.gamestate_game_over):
                    self.areas[0].add_text('Game Over\nPress space for new game')
                    curr_score = score.Score(datetime.datetime.now(), self.game.score)
                    self.score_board.add_score(curr_score)
                    self.score_board.render_scores()
                    self.paused = True
        if update_rate.is_time():
            self.root.update_idletasks()
            self.root.update()
            self.replay.replay_settings.read_state()
