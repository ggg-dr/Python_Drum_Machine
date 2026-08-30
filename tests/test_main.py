# main.pyからDrumMachineクラスを読み込む
# ※まだmain.pyにはDrumMachineが存在しないため、
#   最初のテストでは失敗する想定
from main import DrumMachine, DrumMachineGUI
import pytest
import tkinter as tk

@pytest.fixture(scope="module")
def tk_root():
    """
    GUIテストで共通して使用する
    Tkinterのrootを作成する。
    """

    # Tkinterのメインウィンドウを1回だけ作成する
    root = tk.Tk()

    # テスト中はウィンドウを画面に表示しない
    root.withdraw()

    # 各テストでrootを使用できるように渡す
    yield root

    # すべてのGUIテスト終了後にrootを破棄する
    root.destroy()


def test_drum_patterns_are_initialized():
    """
    ドラムパターンの初期状態を確認するテスト。

    KICK・SNARE・HI-HATにはそれぞれ16ステップがあり、
    アプリ起動時はすべてOFF(False)になっていることを確認する。
    """

    # ドラムマシンを作成する
    drum_machine = DrumMachine()

    # 使用する3種類のドラムが存在することを確認する
    assert "kick" in drum_machine.patterns
    assert "snare" in drum_machine.patterns
    assert "hihat" in drum_machine.patterns

    # 各ドラムに16ステップ用意されていることを確認する
    assert len(drum_machine.patterns["kick"]) == 16
    assert len(drum_machine.patterns["snare"]) == 16
    assert len(drum_machine.patterns["hihat"]) == 16

    # 初期状態では、すべてのステップがOFF(False)であることを確認する
    assert all(step is False for step in drum_machine.patterns["kick"])
    assert all(step is False for step in drum_machine.patterns["snare"])
    assert all(step is False for step in drum_machine.patterns["hihat"])

def test_bpm_is_initialized_to_120():
    """
    BPMの初期値を確認するテスト。

    アプリ起動時のテンポは、
    要件定義で決めた120 BPMになっていることを確認する。
    """

    # ドラムマシンを作成する
    drum_machine = DrumMachine()

    # BPMの初期値が120であることを確認する
    assert drum_machine.bpm == 120

def test_toggle_step_turns_kick_step_on():
    """
    ステップをONに切り替えられることを確認するテスト。

    初期状態ではすべてFalse(OFF)だが、
    KICKの1番目のステップを切り替えると
    True(ON)になることを確認する。
    """

    # ドラムマシンを作成する
    drum_machine = DrumMachine()

    # KICKの1番目のステップを切り替える
    # リストは0から始まるため、1番目のステップは「0」で指定する
    drum_machine.toggle_step("kick", 0)

    # KICKの1番目がON(True)になったことを確認する
    assert drum_machine.patterns["kick"][0] is True

def test_toggle_step_turns_kick_step_off_again():
    """
    ONになっているステップを、
    もう一度切り替えるとOFFに戻ることを確認するテスト。
    """

    # ドラムマシンを作成する
    drum_machine = DrumMachine()

    # KICKの1番目を1回切り替えてONにする
    drum_machine.toggle_step("kick", 0)

    # 同じステップをもう一度切り替える
    drum_machine.toggle_step("kick", 0)

    # KICKの1番目がOFF(False)に戻ったことを確認する
    assert drum_machine.patterns["kick"][0] is False

def test_step_interval_is_calculated_from_bpm():
    """
    BPMから1ステップ分の再生間隔を
    正しく計算できることを確認するテスト。

    1ステップは16分音符なので、
    120 BPMの場合は125ミリ秒になる。
    """

    # ドラムマシンを作成する
    drum_machine = DrumMachine()

    # 120 BPMでの1ステップの再生間隔を取得する
    interval = drum_machine.get_step_interval()

    # 1ステップが125ミリ秒になることを確認する
    assert interval == 125

def test_current_step_is_initialized_to_zero():
    """
    再生開始位置の初期値を確認するテスト。

    ドラムマシンを作成した直後は、
    1番目のステップから開始できるように
    current_step が0になっていることを確認する。
    """

    # ドラムマシンを作成する
    drum_machine = DrumMachine()

    # 再生位置の初期値が0であることを確認する
    assert drum_machine.current_step == 0

def test_is_playing_is_initialized_to_false():
    """
    再生状態の初期値を確認するテスト。

    アプリを起動した直後はまだ再生していないため、
    is_playing がFalseになっていることを確認する。
    """

    # ドラムマシンを作成する
    drum_machine = DrumMachine()

    # 起動直後は停止状態(False)であることを確認する
    assert drum_machine.is_playing is False

def test_start_changes_is_playing_to_true():
    """
    再生開始処理を確認するテスト。

    start()を実行すると、
    再生状態を表すis_playingが
    Trueになることを確認する。
    """

    # ドラムマシンを作成する
    drum_machine = DrumMachine()

    # 再生を開始する
    drum_machine.start()

    # 再生中(True)になったことを確認する
    assert drum_machine.is_playing is True

def test_stop_changes_is_playing_to_false():
    """
    再生停止処理を確認するテスト。

    再生中にstop()を実行すると、
    再生状態を表すis_playingが
    Falseになることを確認する。
    """

    # ドラムマシンを作成する
    drum_machine = DrumMachine()

    # まず再生を開始する
    drum_machine.start()

    # 再生を停止する
    drum_machine.stop()

    # 停止中(False)になったことを確認する
    assert drum_machine.is_playing is False

def test_advance_step_moves_to_next_step():
    """
    再生位置を次のステップへ進められることを確認するテスト。

    初期状態ではcurrent_stepは0なので、
    advance_step()を実行すると
    1になることを確認する。
    """

    # ドラムマシンを作成する
    drum_machine = DrumMachine()

    # 再生位置を1ステップ進める
    drum_machine.advance_step()

    # current_stepが1になったことを確認する
    assert drum_machine.current_step == 1

def test_advance_step_returns_to_zero_after_last_step():
    """
    最後のステップの次は、
    最初のステップに戻ることを確認するテスト。
    """

    # ドラムマシンを作成する
    drum_machine = DrumMachine()

    # 最後のステップに移動する
    drum_machine.current_step = 15

    # 再生位置を1ステップ進める
    drum_machine.advance_step()

    # 最初のステップ0に戻ることを確認する
    assert drum_machine.current_step == 0

def test_get_active_instruments_returns_instruments_on_current_step():
    """
    現在のステップでONになっている楽器を
    取得できることを確認するテスト。
    """

    # ドラムマシンを作成する
    drum_machine = DrumMachine()

    # 現在のステップ0でKICKとHI-HATをONにする
    drum_machine.patterns["kick"][0] = True
    drum_machine.patterns["hihat"][0] = True

    # 現在のステップで鳴らす楽器を取得する
    active_instruments = drum_machine.get_active_instruments()

    # KICKとHI-HATが取得できることを確認する
    assert active_instruments == ["kick", "hihat"]


def test_get_active_instruments_returns_empty_list_when_all_steps_are_off():
    """
    現在のステップですべての楽器がOFFの場合、
    空のリストが返ることを確認するテスト。
    """

    # ドラムマシンを作成する
    drum_machine = DrumMachine()

    # 現在のステップで鳴らす楽器を取得する
    active_instruments = drum_machine.get_active_instruments()

    # すべてOFFなので空のリストになることを確認する
    assert active_instruments == []

def test_set_bpm_changes_bpm():
    """
    BPMを変更できることを確認するテスト。

    初期値は120 BPMだが、
    set_bpm()を実行すると指定したBPMに
    変更されることを確認する。
    """

    # ドラムマシンを作成する
    drum_machine = DrumMachine()

    # BPMを140に変更する
    drum_machine.set_bpm(140)

    # BPMが140に変更されたことを確認する
    assert drum_machine.bpm == 140

def test_set_bpm_rejects_zero_or_negative_value():
    """
    0以下のBPMを設定できないことを確認するテスト。
    """

    drum_machine = DrumMachine()

    with pytest.raises(ValueError):
        drum_machine.set_bpm(0)

def test_play_step_returns_active_instruments_and_advances_step():
    """
    現在のステップで鳴らす楽器を取得し、
    そのあと再生位置が次のステップへ進むことを確認する。
    """

    # ドラムマシンを作成する
    drum_machine = DrumMachine()

    # 現在のステップ0でKICKをONにする
    drum_machine.patterns["kick"][0] = True

    # 1ステップ分の再生処理を実行する
    active_instruments = drum_machine.play_step()

    # 現在のステップでONの楽器が取得できることを確認する
    assert active_instruments == ["kick"]

    # 再生位置が次のステップへ進んでいることを確認する
    assert drum_machine.current_step == 1

def test_play_step_returns_active_instruments_and_returns_to_zero_after_last_step():
    """
    最後のステップを再生した場合でも、
    ONになっている楽器を取得したあと、
    再生位置が最初のステップ0に戻ることを確認する。
    """

    # ドラムマシンを作成する
    drum_machine = DrumMachine()

    # 再生位置を最後のステップ15にする
    drum_machine.current_step = 15

    # 最後のステップでSNAREをONにする
    drum_machine.patterns["snare"][15] = True

    # 1ステップ分の再生処理を実行する
    active_instruments = drum_machine.play_step()

    # 最後のステップでONのSNAREが取得できることを確認する
    assert active_instruments == ["snare"]

    # 最後まで進んだので最初のステップ0に戻ることを確認する
    assert drum_machine.current_step == 0

def test_update_playback_does_not_advance_when_stopped():
    """
    停止中は再生位置が進まないことを確認するテスト。
    """

    # ドラムマシンを作成する
    drum_machine = DrumMachine()

    # 停止中のまま再生処理を更新する
    drum_machine.update_playback()

    # 停止中なので再生位置が進まないことを確認する
    assert drum_machine.current_step == 0

def test_update_playback_advances_when_playing():
    """
    再生中は再生位置が1ステップ進むことを確認するテスト。
    """

    # ドラムマシンを作成する
    drum_machine = DrumMachine()

    # 再生を開始する
    drum_machine.start()

    # 再生処理を更新する
    drum_machine.update_playback()

    # 再生位置が1ステップ進んだことを確認する
    assert drum_machine.current_step == 1

def test_update_playback_returns_active_instruments_when_playing():
    """
    再生中は現在のステップでONになっている楽器を
    取得できることを確認するテスト。
    """

    # ドラムマシンを作成する
    drum_machine = DrumMachine()

    # 現在のステップ0でKICKをONにする
    drum_machine.patterns["kick"][0] = True

    # 再生を開始する
    drum_machine.start()

    # 再生処理を更新する
    active_instruments = drum_machine.update_playback()

    # 現在のステップでONの楽器が返ることを確認する
    assert active_instruments == ["kick"]

def test_update_playback_returns_none_when_stopped():
    """
    停止中は楽器を再生せず、
    Noneが返ることを確認するテスト。
    """

    # ドラムマシンを作成する
    drum_machine = DrumMachine()

    # 停止中のまま再生処理を更新する
    active_instruments = drum_machine.update_playback()

    # 停止中なので何も返らないことを確認する
    assert active_instruments is None


def test_drum_machine_gui_stores_root(tk_root):
    """
    GUIが渡されたTkinterのrootを
    保持できることを確認するテスト。
    """

    # 共通のTkinter rootを使ってGUIを作成する
    gui = DrumMachineGUI(tk_root)

    # GUIが渡されたrootを保持していることを確認する
    assert gui.root is tk_root

def test_drum_machine_gui_can_be_created(tk_root):
    """
    ドラムマシンのGUIを作成できることを確認するテスト。
    """

    # 共通のTkinter rootを使ってGUIを作成する
    gui = DrumMachineGUI(tk_root)

    # GUIが正常に作成されたことを確認する
    assert gui is not None



def test_drum_machine_gui_sets_window_title(tk_root):
    """
    GUI作成時にウィンドウタイトルが
    設定されることを確認するテスト。
    """

    # 共通のTkinter rootを使ってGUIを作成する
    DrumMachineGUI(tk_root)

    # ウィンドウタイトルを確認する
    assert tk_root.title() == "Python Drum Machine"

def test_drum_machine_gui_has_drum_machine(tk_root):
    """
    GUIがDrumMachineを持っていることを確認するテスト。
    """

    # 共通のTkinter rootを使ってGUIを作成する
    gui = DrumMachineGUI(tk_root)

    # GUIがDrumMachineを持っていることを確認する
    assert isinstance(gui.drum_machine, DrumMachine)


def test_play_button_text_is_play(tk_root):
    """
    再生ボタンに「再生」と表示されることを確認するテスト。
    """

    # 共通のTkinter rootを使ってGUIを作成する
    gui = DrumMachineGUI(tk_root)

    # 再生ボタンの文字を確認する
    assert gui.play_button["text"] == "再生"

def test_play_button_starts_drum_machine(tk_root):
    """
    再生ボタンを押すと、
    ドラムマシンが再生状態になることを確認するテスト。
    """

    # 共通のTkinter rootを使ってGUIを作成する
    gui = DrumMachineGUI(tk_root)

    # 再生ボタンを押す
    gui.play_button.invoke()

    # 再生状態になっていることを確認する
    assert gui.drum_machine.is_playing is True

def test_drum_machine_gui_has_stop_button(tk_root):
    """
    GUIに停止ボタンがあることを確認するテスト。
    """

    # 共通のTkinter rootを使ってGUIを作成する
    gui = DrumMachineGUI(tk_root)

    # 停止ボタンが作成されていることを確認する
    assert gui.stop_button is not None

def test_stop_button_stops_drum_machine(tk_root):
    """
    停止ボタンを押すと、
    ドラムマシンが停止状態になることを確認するテスト。
    """

    # 共通のTkinter rootを使ってGUIを作成する
    gui = DrumMachineGUI(tk_root)

    # まず再生状態にする
    gui.drum_machine.start()

    # 停止ボタンを押す
    gui.stop_button.invoke()

    # 停止状態になっていることを確認する
    assert gui.drum_machine.is_playing is False

def test_play_button_is_managed_by_layout(tk_root):
    """
    再生ボタンがGUI上に配置されていることを確認するテスト。
    """

    # 共通のTkinter rootを使ってGUIを作成する
    gui = DrumMachineGUI(tk_root)

    # 再生ボタンがレイアウト管理されていることを確認する
    assert gui.play_button.winfo_manager() != ""

def test_stop_button_is_managed_by_layout(tk_root):
    """
    停止ボタンがGUI上に配置されていることを確認するテスト。
    """

    # 共通のTkinter rootを使ってGUIを作成する
    gui = DrumMachineGUI(tk_root)

    # 停止ボタンがレイアウト管理されていることを確認する
    assert gui.stop_button.winfo_manager() != ""

def test_drum_machine_gui_has_16_kick_step_buttons(tk_root):
    """
    GUIにKICK用の16ステップボタンが
    作成されていることを確認するテスト。
    """

    # 共通のTkinter rootを使ってGUIを作成する
    gui = DrumMachineGUI(tk_root)

    # KICK用のステップボタンが16個あることを確認する
    assert len(gui.kick_buttons) == 16

def test_kick_step_buttons_are_managed_by_layout(tk_root):
    """
    KICK用の16ステップボタンが
    GUI上に配置されていることを確認するテスト。
    """

    # 共通のTkinter rootを使ってGUIを作成する
    gui = DrumMachineGUI(tk_root)

    # すべてのKICKボタンがレイアウト管理されていることを確認する
    assert all(
        button.winfo_manager() != ""
        for button in gui.kick_buttons
    )

def test_kick_step_button_toggles_kick_pattern(tk_root):
    """
    KICKのステップボタンを押すと、
    対応するステップがONになることを確認するテスト。
    """

    # 共通のTkinter rootを使ってGUIを作成する
    gui = DrumMachineGUI(tk_root)

    # KICKの1番目のボタンを押す
    gui.kick_buttons[0].invoke()

    # KICKの1番目のステップがONになっていることを確認する
    assert gui.drum_machine.patterns["kick"][0] is True

def test_kick_step_button_toggles_kick_pattern_off_again(tk_root):
    """
    KICKのステップボタンを2回押すと、
    対応するステップがOFFに戻ることを確認するテスト。
    """

    # 共通のTkinter rootを使ってGUIを作成する
    gui = DrumMachineGUI(tk_root)

    # KICKの1番目のボタンを1回押してONにする
    gui.kick_buttons[0].invoke()

    # 同じボタンをもう一度押してOFFに戻す
    gui.kick_buttons[0].invoke()

    # KICKの1番目のステップがOFFに戻っていることを確認する
    assert gui.drum_machine.patterns["kick"][0] is False

def test_drum_machine_gui_has_16_snare_step_buttons(tk_root):
    """
    GUIにSNARE用の16ステップボタンが
    作成されていることを確認するテスト。
    """

    # 共通のTkinter rootを使ってGUIを作成する
    gui = DrumMachineGUI(tk_root)

    # SNARE用のステップボタンが16個あることを確認する
    assert len(gui.snare_buttons) == 16

def test_snare_step_button_toggles_snare_pattern(tk_root):
    """
    SNAREのステップボタンを押すと、
    対応するステップがONになることを確認するテスト。
    """

    # 共通のTkinter rootを使ってGUIを作成する
    gui = DrumMachineGUI(tk_root)

    # SNAREの1番目のボタンを押す
    gui.snare_buttons[0].invoke()

    # SNAREの1番目のステップがONになっていることを確認する
    assert gui.drum_machine.patterns["snare"][0] is True

def test_drum_machine_gui_has_16_hihat_step_buttons(tk_root):
    """
    GUIにHI-HAT用の16ステップボタンが
    作成されていることを確認するテスト。
    """

    # 共通のTkinter rootを使ってGUIを作成する
    gui = DrumMachineGUI(tk_root)

    # HI-HAT用のステップボタンが16個あることを確認する
    assert len(gui.hihat_buttons) == 16

def test_hihat_step_button_toggles_hihat_pattern(tk_root):
    """
    HI-HATのステップボタンを押すと、
    対応するステップがONになることを確認するテスト。
    """

    # 共通のTkinter rootを使ってGUIを作成する
    gui = DrumMachineGUI(tk_root)

    # HI-HATの1番目のボタンを押す
    gui.hihat_buttons[0].invoke()

    # HI-HATの1番目のステップがONになっていることを確認する
    assert gui.drum_machine.patterns["hihat"][0] is True

def test_kick_step_buttons_use_grid_layout(tk_root):
    """
    KICK用のステップボタンが
    gridレイアウトで配置されることを確認するテスト。
    """

    # 共通のTkinter rootを使ってGUIを作成する
    gui = DrumMachineGUI(tk_root)

    # KICKの1番目のボタンがgridで配置されていることを確認する
    assert gui.kick_buttons[0].winfo_manager() == "grid"

def test_snare_step_buttons_use_grid_layout(tk_root):
    """
    SNARE用のステップボタンが
    gridレイアウトで配置されることを確認するテスト。
    """

    # 共通のTkinter rootを使ってGUIを作成する
    gui = DrumMachineGUI(tk_root)

    # SNAREの1番目のボタンがgridで配置されていることを確認する
    assert gui.snare_buttons[0].winfo_manager() == "grid"

def test_hihat_step_buttons_use_grid_layout(tk_root):
    """
    HI-HAT用のステップボタンが
    gridレイアウトで配置されることを確認するテスト。
    """

    # 共通のTkinter rootを使ってGUIを作成する
    gui = DrumMachineGUI(tk_root)

    # HI-HATの1番目のボタンがgridで配置されていることを確認する
    assert gui.hihat_buttons[0].winfo_manager() == "grid"

def test_kick_step_button_text_changes_to_on(tk_root):
    """
    KICKのステップボタンを押すと、
    ボタンの表示がONに変わることを確認するテスト。
    """

    # 共通のTkinter rootを使ってGUIを作成する
    gui = DrumMachineGUI(tk_root)

    # KICKの1番目のボタンを押す
    gui.kick_buttons[0].invoke()

    # ボタンの表示がONになっていることを確認する
    assert gui.kick_buttons[0]["text"] == "ON"

def test_kick_step_button_text_returns_to_number(tk_root):
    """
    KICKのステップボタンを2回押すと、
    ボタンの表示が元の番号に戻ることを確認するテスト。
    """

    # 共通のTkinter rootを使ってGUIを作成する
    gui = DrumMachineGUI(tk_root)

    # KICKの1番目のボタンを2回押す
    gui.kick_buttons[0].invoke()
    gui.kick_buttons[0].invoke()

    # ボタンの表示が元の番号に戻っていることを確認する
    assert gui.kick_buttons[0]["text"] == "1"

def test_snare_step_button_text_changes_to_on(tk_root):
    """
    SNAREのステップボタンを押すと、
    ボタンの表示がONに変わることを確認するテスト。
    """

    # 共通のTkinter rootを使ってGUIを作成する
    gui = DrumMachineGUI(tk_root)

    # SNAREの1番目のボタンを押す
    gui.snare_buttons[0].invoke()

    # ボタンの表示がONになっていることを確認する
    assert gui.snare_buttons[0]["text"] == "ON"

def test_hihat_step_button_text_changes_to_on(tk_root):
    """
    HI-HATのステップボタンを押すと、
    ボタンの表示がONに変わることを確認するテスト。
    """

    # 共通のTkinter rootを使ってGUIを作成する
    gui = DrumMachineGUI(tk_root)

    # HI-HATの1番目のボタンを押す
    gui.hihat_buttons[0].invoke()

    # ボタンの表示がONになっていることを確認する
    assert gui.hihat_buttons[0]["text"] == "ON"

def test_snare_step_button_text_returns_to_number(tk_root):
    """
    SNAREのステップボタンを2回押すと、
    ボタンの表示が元の番号に戻ることを確認するテスト。
    """

    # 共通のTkinter rootを使ってGUIを作成する
    gui = DrumMachineGUI(tk_root)

    # SNAREの1番目のボタンを2回押す
    gui.snare_buttons[0].invoke()
    gui.snare_buttons[0].invoke()

    # ボタンの表示が元の番号に戻っていることを確認する
    assert gui.snare_buttons[0]["text"] == "1"

def test_hihat_step_button_text_returns_to_number(tk_root):
    """
    HI-HATのステップボタンを2回押すと、
    ボタンの表示が元の番号に戻ることを確認するテスト。
    """

    # 共通のTkinter rootを使ってGUIを作成する
    gui = DrumMachineGUI(tk_root)

    # HI-HATの1番目のボタンを2回押す
    gui.hihat_buttons[0].invoke()
    gui.hihat_buttons[0].invoke()

    # ボタンの表示が元の番号に戻っていることを確認する
    assert gui.hihat_buttons[0]["text"] == "1"

def test_drum_machine_gui_has_bpm_entry(tk_root):
    """
    GUIにBPM入力欄が
    作成されていることを確認するテスト。
    """

    # 共通のTkinter rootを使ってGUIを作成する
    gui = DrumMachineGUI(tk_root)

    # BPM入力欄があることを確認する
    assert gui.bpm_entry is not None

def test_bpm_entry_has_initial_bpm(tk_root):
    """
    BPM入力欄に初期BPMの120が
    表示されていることを確認するテスト。
    """

    # 共通のTkinter rootを使ってGUIを作成する
    gui = DrumMachineGUI(tk_root)

    # BPM入力欄に120が表示されていることを確認する
    assert gui.bpm_entry.get() == "120"

def test_bpm_entry_updates_drum_machine_bpm(tk_root):
    """
    BPM入力欄の値を使って、
    ドラムマシンのBPMを変更できることを確認するテスト。
    """

    # 共通のTkinter rootを使ってGUIを作成する
    gui = DrumMachineGUI(tk_root)

    # BPM入力欄の内容を削除する
    gui.bpm_entry.delete(0, tk.END)

    # 新しいBPMを入力する
    gui.bpm_entry.insert(0, "140")

    # BPMを反映する処理を実行する
    gui.update_bpm()

    # ドラムマシンのBPMが140になっていることを確認する
    assert gui.drum_machine.bpm == 140

def test_drum_machine_gui_has_bpm_update_button(tk_root):
    """
    GUIにBPM更新ボタンが
    作成されていることを確認するテスト。
    """

    # 共通のTkinter rootを使ってGUIを作成する
    gui = DrumMachineGUI(tk_root)

    # BPM更新ボタンがあることを確認する
    assert gui.bpm_update_button is not None

def test_bpm_update_button_updates_drum_machine_bpm(tk_root):
    """
    BPM更新ボタンを押すと、
    ドラムマシンのBPMが変更されることを確認するテスト。
    """

    # 共通のTkinter rootを使ってGUIを作成する
    gui = DrumMachineGUI(tk_root)

    # BPM入力欄の内容を削除する
    gui.bpm_entry.delete(0, tk.END)

    # 新しいBPMを入力する
    gui.bpm_entry.insert(0, "140")

    # BPM更新ボタンを押す
    gui.bpm_update_button.invoke()

    # ドラムマシンのBPMが140になっていることを確認する
    assert gui.drum_machine.bpm == 140

def test_update_bpm_with_zero_does_not_change_bpm(tk_root):
    """
    BPM入力欄に0を入力した場合、
    BPMが変更されないことを確認するテスト。
    """

    # 共通のTkinter rootを使ってGUIを作成する
    gui = DrumMachineGUI(tk_root)

    # BPM入力欄の内容を削除する
    gui.bpm_entry.delete(0, tk.END)

    # 0を入力する
    gui.bpm_entry.insert(0, "0")

    # BPM更新処理を実行する
    gui.update_bpm()

    # BPMが初期値120のままであることを確認する
    assert gui.drum_machine.bpm == 120

def test_update_bpm_with_text_does_not_change_bpm(tk_root):
    """
    BPM入力欄に数字以外を入力した場合、
    BPMが変更されないことを確認するテスト。
    """

    # 共通のTkinter rootを使ってGUIを作成する
    gui = DrumMachineGUI(tk_root)

    # BPM入力欄の内容を削除する
    gui.bpm_entry.delete(0, tk.END)

    # 数字ではない文字を入力する
    gui.bpm_entry.insert(0, "abc")

    # BPM更新処理を実行する
    gui.update_bpm()

    # BPMが初期値120のままであることを確認する
    assert gui.drum_machine.bpm == 120

def test_drum_machine_gui_has_start_playback(tk_root):
    """
    GUIに再生ループを開始する処理が
    あることを確認するテスト。
    """

    # 共通のTkinter rootを使ってGUIを作成する
    gui = DrumMachineGUI(tk_root)

    # 再生ループを開始するメソッドがあることを確認する
    assert callable(gui.start_playback)

def test_play_button_calls_start_playback(tk_root):
    """
    再生ボタンを押すと、
    GUIの再生開始処理が実行されることを確認するテスト。
    """

    # 共通のTkinter rootを使ってGUIを作成する
    gui = DrumMachineGUI(tk_root)

    # 再生ボタンを押す
    gui.play_button.invoke()

    # ドラムマシンが再生状態になっていることを確認する
    assert gui.drum_machine.is_playing is True

def test_start_playback_schedules_next_step(tk_root):
    """
    再生を開始すると、
    次のステップ処理が予約されることを確認するテスト。
    """

    # 共通のTkinter rootを使ってGUIを作成する
    gui = DrumMachineGUI(tk_root)

    # afterが呼ばれたか確認するための記録用リスト
    called = []

    # 本物のafterの代わりに使うテスト用関数
    def fake_after(interval, callback):
        called.append((interval, callback))

    # root.afterをテスト用関数に置き換える
    original_after = gui.root.after
    gui.root.after = fake_after

    try:
        # 再生を開始する
        gui.start_playback()

        # afterが1回呼ばれたことを確認する
        assert len(called) == 1

    finally:
        # テスト後に元のafterへ戻す
        gui.root.after = original_after

def test_run_playback_step_advances_current_step(tk_root):
    """
    再生中の1ステップ処理を実行すると、
    再生位置が1つ進むことを確認するテスト。
    """

    # 共通のTkinter rootを使ってGUIを作成する
    gui = DrumMachineGUI(tk_root)

    # ドラムマシンを再生状態にする
    gui.drum_machine.start()

    # 1ステップ分の再生処理を実行する
    gui.run_playback_step()

    # 再生位置が1に進んでいることを確認する
    assert gui.drum_machine.current_step == 1

def test_run_playback_step_schedules_next_step(tk_root):
    """
    1ステップ分の再生処理を実行すると、
    次のステップ処理が予約されることを確認するテスト。
    """

    # 共通のTkinter rootを使ってGUIを作成する
    gui = DrumMachineGUI(tk_root)

    # ドラムマシンを再生状態にする
    gui.drum_machine.start()

    # afterが呼ばれたか確認するための記録用リスト
    called = []

    # 本物のafterの代わりに使うテスト用関数
    def fake_after(interval, callback):
        called.append((interval, callback))

    # root.afterをテスト用関数に置き換える
    original_after = gui.root.after
    gui.root.after = fake_after

    try:
        # 1ステップ分の再生処理を実行する
        gui.run_playback_step()

        # 次のステップ処理が1回予約されたことを確認する
        assert len(called) == 1

    finally:
        # テスト後に元のafterへ戻す
        gui.root.after = original_after

def test_run_playback_step_does_not_schedule_when_stopped(tk_root):
    """
    停止中に再生処理を実行しても、
    次のステップ処理が予約されないことを確認するテスト。
    """

    # 共通のTkinter rootを使ってGUIを作成する
    gui = DrumMachineGUI(tk_root)

    # 停止状態にしておく
    gui.drum_machine.stop()

    # afterが呼ばれたか確認するための記録用リスト
    called = []

    # 本物のafterの代わりに使うテスト用関数
    def fake_after(interval, callback):
        called.append((interval, callback))

    # root.afterをテスト用関数に置き換える
    original_after = gui.root.after
    gui.root.after = fake_after

    try:
        # 停止中に1ステップ分の再生処理を実行する
        gui.run_playback_step()

        # 次の処理が予約されていないことを確認する
        assert len(called) == 0

    finally:
        # テスト後に元のafterへ戻す
        gui.root.after = original_after


def test_run_playback_step_does_not_advance_when_stopped(tk_root):
    """
    停止中に再生処理が呼ばれても、
    再生位置が進まないことを確認するテスト。
    """

    # 共通のTkinter rootを使ってGUIを作成する
    gui = DrumMachineGUI(tk_root)

    # 停止状態にしておく
    gui.drum_machine.stop()

    # 停止中に再生処理を実行する
    gui.run_playback_step()

    # 再生位置が0のままであることを確認する
    assert gui.drum_machine.current_step == 0

def test_start_playback_advances_first_step_immediately(tk_root):
    """
    再生を開始すると、
    最初のステップがすぐに1つ進むことを確認するテスト。
    """

    # 共通のTkinter rootを使ってGUIを作成する
    gui = DrumMachineGUI(tk_root)

    # 本物のafterが動かないようにテスト用関数へ置き換える
    original_after = gui.root.after
    gui.root.after = lambda interval, callback: None

    try:
        # 再生を開始する
        gui.start_playback()

        # 再生位置が1に進んでいることを確認する
        assert gui.drum_machine.current_step == 1

    finally:
        # テスト後に元のafterへ戻す
        gui.root.after = original_after

def test_start_playback_does_not_start_twice(tk_root):
    """
    すでに再生中の場合は、
    再生処理を重複して開始しないことを確認するテスト。
    """

    gui = DrumMachineGUI(tk_root)

    called = []

    # 本物のafterの代わりに使うテスト用関数
    def fake_after(interval, callback):
        called.append((interval, callback))

    original_after = gui.root.after
    gui.root.after = fake_after

    try:
        # 1回目の再生開始
        gui.start_playback()

        # 2回目の再生開始
        gui.start_playback()

        # afterの予約は1回だけであることを確認する
        assert len(called) == 1

    finally:
        gui.root.after = original_after