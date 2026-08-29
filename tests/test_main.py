# main.pyからDrumMachineクラスを読み込む
# ※まだmain.pyにはDrumMachineが存在しないため、
#   最初のテストでは失敗する想定
from main import DrumMachine
import pytest


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