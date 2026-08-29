import tkinter as tk

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

        # 再生ボタンを作成する
        self.play_button = tk.Button(
            self.root,
            text="再生",
            command=self.drum_machine.start
        )

        # 停止ボタンを作成する
        self.stop_button = tk.Button(
            self.root,
            text="停止"
        )

        # 停止ボタンを作成する
        self.stop_button = tk.Button(
            self.root,
            text="停止",
            command=self.drum_machine.stop
        )