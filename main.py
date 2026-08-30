import tkinter as tk
import pygame
class DrumMachine:
    """
    ドラムマシンのデータや処理を管理するクラス。

    KICK・SNARE・HI-HATのドラムパターンや、
    BPMなどの演奏に必要な情報を管理する。
    """

    def __init__(self):
        """
        ドラムマシンの初期状態を作成する。

        各ドラムは16ステップで構成し、
        Falseを「音を鳴らさない（OFF）」として扱う。
        """

        # 各ドラムの16ステップをすべてOFF(False)で初期化する
        self.patterns = {
            "kick": [False] * 16,
            "snare": [False] * 16,
            "hihat": [False] * 16
        }

        # アプリ起動時のテンポを120 BPMに設定する
        self.bpm = 120

        # 現在再生しているステップの位置を管理する
        # Pythonのリストは0から始まるため、0が画面上の1番目に対応する
        self.current_step = 0

        # 現在ドラムパターンを再生しているかどうかを管理する
        # Falseは停止中、Trueは再生中を表す
        self.is_playing = False

    def toggle_step(self, instrument, step):
        """
        指定した楽器のステップのON/OFFを切り替える。

        Trueの場合はFalseに、
        Falseの場合はTrueに変更する。
        """

        # 現在の状態を反転させて、ON/OFFを切り替える
        self.patterns[instrument][step] = not self.patterns[instrument][step]

    def get_step_interval(self):
        """
        BPMから1ステップ分の再生間隔を計算する。

        今回は1ステップを16分音符としているため、
        4分音符の長さを4で割って計算する。

        戻り値はミリ秒単位。
        """

        # 1分は60000ミリ秒。
        # BPMで割ると4分音符1つ分の時間になり、
        # さらに4で割ると16分音符1つ分の時間になる。
        interval = 60000 / self.bpm / 4

        return interval

    def start(self):
        """
        ドラムパターンの再生を開始する。

        再生状態を表すis_playingをTrueに変更する。
        """

        # 再生中の状態に変更する
        self.is_playing = True

    def stop(self):
        """
        ドラムパターンの再生を停止する。

        再生状態を表すis_playingをFalseに変更する。
        """

        # 停止中の状態に変更する
        self.is_playing = False

    def advance_step(self):
        """
        再生位置を次のステップへ進める。

        最後のステップまで進んだ場合は、
        最初のステップ0に戻る。
        """

        # 現在の再生位置を1つ進める
        self.current_step += 1

        #16ステップ目を超えたら最初に戻す
        if self.current_step >= 16:
            self.current_step = 0

        #短く書くにはこう
        #def advance_step(self):
        #    self.current_step = (self.current_step + 1) % 16

    def get_active_instruments(self):
        """
        現在のステップでONになっている楽器を取得する。
        """

        active_instruments = []

        # 各楽器について、現在のステップがONか確認する
        for instrument in self.patterns:
            if self.patterns[instrument][self.current_step]:
                active_instruments.append(instrument)

        return active_instruments

    def set_bpm(self, bpm):
        """
        BPMを指定した値に変更する。

        0以下の値が指定された場合は、
        ValueErrorを発生させる。
        """

        # 0以下のBPMは使用できないためエラーにする
        if bpm <= 0:
            raise ValueError("BPMは1以上にしてください")

        # BPMを指定された値に変更する
        self.bpm = bpm

    def play_step(self):
        """
        現在のステップで鳴らす楽器を取得し、
        再生位置を次のステップへ進める。
        """

        # 現在のステップでONになっている楽器を取得する
        active_instruments = self.get_active_instruments()

        # 再生位置を次のステップへ進める
        self.advance_step()

        # 鳴らす楽器の一覧を返す
        return active_instruments

    def update_playback(self):
        """
        再生状態に応じて1ステップ分の処理を実行する。

        停止中の場合は何もしない。
        再生中の場合は、現在のステップで
        ONになっている楽器を返す。
        """

        # 停止中の場合は再生位置を進めない
        if not self.is_playing:
            return

        # 再生中なら1ステップ分の処理を実行し、
        # ONになっている楽器を返す
        return self.play_step()

class DrumMachineGUI:
    """
    ドラムマシンのGUIを管理するクラス。
    """

    def __init__(self, root=None):
        """
        GUIの初期状態を作成する。
        """

        # GUIで使用するrootを保持する
        self.root = root

        # ウィンドウタイトルを設定する
        self.root.title("Python Drum Machine")

        # GUIから操作するドラムマシン本体を作成する
        self.drum_machine = DrumMachine()

        # 音声再生機能を初期化する
        pygame.mixer.init()

        # 各楽器の音声ファイルを管理する
        self.sound_files = {
            "kick": "sounds/kick.wav",
            "snare": "sounds/snare.wav",
            "hihat": "sounds/hihat.wav"
        }

        # pygameの音声機能を初期化する
        pygame.mixer.init()

        # 各楽器の音声ファイルを読み込む
        self.sounds = {
            "kick": pygame.mixer.Sound(self.sound_files["kick"]),
            "snare": pygame.mixer.Sound(self.sound_files["snare"]),
            "hihat": pygame.mixer.Sound(self.sound_files["hihat"])
        }

        # 再生ボタンを作成する
        self.play_button = tk.Button(
            self.root,
            text="再生",
            command=self.start_playback
        )

        # 再生ボタンをウィンドウ上に配置する
        self.play_button.pack()

        # 停止ボタンを作成する
        self.stop_button = tk.Button(
            self.root,
            text="停止",
            command=self.drum_machine.stop
        )

        # 停止ボタンをウィンドウ上に配置する
        self.stop_button.pack()

        # BPM入力欄を作成する
        self.bpm_entry = tk.Entry(
            self.root
        )

        # 初期BPMを入力欄に表示する
        self.bpm_entry.insert(
            0,
            str(self.drum_machine.bpm)
        )

        # BPM更新ボタンを作成する
        self.bpm_update_button = tk.Button(
            self.root,
            text="BPM更新",
            command=self.update_bpm
        )

        # BPM入力欄をウィンドウ上に配置する
        self.bpm_entry.pack()

        # ステップボタンをまとめて配置するためのフレームを作成する
        self.pattern_frame = tk.Frame(self.root)

        # フレーム自体はrootにpackで配置する
        self.pattern_frame.pack()

        # 楽器名のラベルを作成する
        self.kick_label = tk.Label(
            self.pattern_frame,
            text="KICK"
        )
        self.kick_label.grid(
            row=0,
            column=0
        )

        self.snare_label = tk.Label(
            self.pattern_frame,
            text="SNARE"
        )
        self.snare_label.grid(
            row=1,
            column=0
        )

        self.hihat_label = tk.Label(
            self.pattern_frame,
            text="HI-HAT"
        )
        self.hihat_label.grid(
            row=2,
            column=0
        )

        # KICK用のステップボタンを入れるリストを作成する
        self.kick_buttons = []

        # KICK用の16ステップボタンを作成する
        for step in range(16):
            button = tk.Button(
                self.pattern_frame,
                text=str(step + 1),
                command=lambda step=step: self.toggle_kick_step(step))

            # 作成したボタンをリストに追加する
            self.kick_buttons.append(button)

            # KICK用のボタンを横16列に配置する
            button.grid(
                row=0,
                column=step + 1
            )

        # SNARE用のステップボタンを入れるリストを作成する
        self.snare_buttons = []

        # SNARE用の16ステップボタンを作成する
        for step in range(16):
            button = tk.Button(
                self.pattern_frame,
                text=str(step + 1),
                command=lambda step=step: self.toggle_snare_step(step))

            # 作成したボタンをリストに追加する
            self.snare_buttons.append(button)

            # SNARE用のボタンを横16列に配置する
            button.grid(
                row=1,
                column=step + 1
            )

        # HI-HAT用のステップボタンを入れるリストを作成する
        self.hihat_buttons = []

        # HI-HAT用の16ステップボタンを作成する
        for step in range(16):
            button = tk.Button(
                self.pattern_frame,
                text=str(step + 1),
                command=lambda step=step: self.toggle_hihat_step(step))

            # 作成したボタンをリストに追加する
            self.hihat_buttons.append(button)

            # HI-HAT用のボタンを横16列に配置する
            button.grid(
                row=2,
                column=step + 1
            )

    def toggle_kick_step(self, step):
        # KICKのON・OFFを切り替える
        self.drum_machine.toggle_step("kick", step)

        # ONの場合
        if self.drum_machine.patterns["kick"][step]:
            self.kick_buttons[step]["text"] = "ON"
            self.kick_buttons[step]["bg"] = "orange"

        # OFFの場合
        else:
            self.kick_buttons[step]["text"] = str(step + 1)
            self.kick_buttons[step]["bg"] = "SystemButtonFace"

    def toggle_snare_step(self, step):
        # SNAREのON・OFFを切り替える
        self.drum_machine.toggle_step("snare", step)

        # ONの場合
        if self.drum_machine.patterns["snare"][step]:
            self.snare_buttons[step]["text"] = "ON"
            self.snare_buttons[step]["bg"] = "orange"

        # OFFの場合
        else:
            self.snare_buttons[step]["text"] = str(step + 1)
            self.snare_buttons[step]["bg"] = "SystemButtonFace"

    def toggle_hihat_step(self, step):
        # HI-HATのON・OFFを切り替える
        self.drum_machine.toggle_step("hihat", step)

        # ONの場合
        if self.drum_machine.patterns["hihat"][step]:
            self.hihat_buttons[step]["text"] = "ON"
            self.hihat_buttons[step]["bg"] = "orange"

        # OFFの場合
        else:
            self.hihat_buttons[step]["text"] = str(step + 1)
            self.hihat_buttons[step]["bg"] = "SystemButtonFace"

    def update_bpm(self):
        """
        BPM入力欄の値を取得して、
        ドラムマシンのBPMを変更する。
        """

        try:
            # BPM入力欄に入力されている文字を取得する
            bpm_text = self.bpm_entry.get()

            # 入力された文字を整数に変換する
            bpm = int(bpm_text)

            # ドラムマシンのBPMを変更する
            self.drum_machine.set_bpm(bpm)

        except ValueError:
            # 数字以外や0以下の値が入力された場合は何もしない
            pass

    def start_playback(self):
        """
        ドラムマシンの再生を開始し、
        最初のステップをすぐに実行する。
        """

        # すでに再生中の場合は、
        # 再生処理を重複して開始しない
        if self.drum_machine.is_playing:
            return

        # ドラムマシンを再生状態にする
        self.drum_machine.start()

        # 最初の1ステップをすぐに実行する
        self.run_playback_step()

    def run_playback_step(self):
        """
        再生中の1ステップ分の処理を行い、
        現在位置の表示を更新して、
        次のステップ処理を予約する。
        """

        # 停止中の場合は何もしない
        if not self.drum_machine.is_playing:
            return

        # 現在のステップでONになっている楽器を取得する
        active_instruments = self.drum_machine.update_playback()

        # ONになっている楽器を1つずつ再生する
        for instrument in active_instruments:
            self.play_instrument(instrument)

        # 現在の再生位置の表示を更新する
        self.update_current_step_display()

        # BPMから1ステップ分の待ち時間を取得する
        interval = int(self.drum_machine.get_step_interval())

        # 一定時間後に次のステップ処理を実行する
        self.root.after(
            interval,
            self.run_playback_step
        )

        # ONになっている楽器の一覧を返す
        return active_instruments

    def update_current_step_display(self):
        """
        現在の再生位置の表示を更新する。
        """

        # すべてのKICKボタンを通常表示に戻す
        for button in self.kick_buttons:
            button["relief"] = "raised"

        # すべてのSNAREボタンを通常表示に戻す
        for button in self.snare_buttons:
            button["relief"] = "raised"

        # すべてのHI-HATボタンを通常表示に戻す
        for button in self.hihat_buttons:
            button["relief"] = "raised"

        # 現在の再生位置を取得する
        current_step = self.drum_machine.current_step

        # 現在位置の3つの楽器ボタンをへこんだ表示にする
        self.kick_buttons[current_step]["relief"] = "sunken"
        self.snare_buttons[current_step]["relief"] = "sunken"
        self.hihat_buttons[current_step]["relief"] = "sunken"

    def play_instrument(self, instrument):
        """
        指定された楽器の音声を再生する。
        """

        # 指定された楽器のSoundオブジェクトを取得する
        sound = self.sounds[instrument]

        # 音声を再生する
        sound.play()

if __name__ == "__main__":
    # Tkinterのメインウィンドウを作成する
    root = tk.Tk()

    # ドラムマシンGUIを作成する
    gui = DrumMachineGUI(root)

    # GUIの処理を開始する
    root.mainloop()