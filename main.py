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