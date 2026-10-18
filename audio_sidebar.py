# -*- coding: utf-8 -*-
"""
audio_sidebar  v1.8.1
=====================
Windows 11 のクイック設定「音声出力」フライアウトを真似た自作ツール。

できること:
  1. 出力デバイスをリスト表示し、クリックで切り替え（選択中は左に青いバー）
  2. 既定デバイス全体の音量とミュート
  3. 起動中アプリごとの音量ミキサー（ミュート表示つき）

トレイアイコンをクリックすると画面右下にパネルが出ます。

依存:  py -m pip install pycaw comtypes pystray Pillow
注意:  Windows 専用。Python 3.x / pycaw 20251023 で動作確認。

-------------------------------------------------------------------
変更履歴 (CHANGELOG)
-------------------------------------------------------------------
v1.8.1
  - トレイメニューの「停止中（右端ホバー）」を「停止」に短縮。
  - スタートアップ登録/解除と停止オン/オフ時の Windows 通知を削除。
    フィードバックはコマンドプロンプトへの print のみに変更。
    （pythonw 起動時は表示されない点に注意）

v1.8.0
  - 「停止」機能を追加。トレイメニューの「停止中（右端ホバー）」で、
    右端ホバーによる自動表示だけを止められる（トレイ常駐は維持）。
    停止中もメニューの「パネルを開く」で手動表示は可能で、開いた後の
    閉じ判定（離脱/外側クリック）も通常どおり動く。

v1.7.3
  - 画面端にカーソルを置きっぱなしにすると表示/非表示が高速で繰り返される
    不具合を修正。閉じる条件に「右端トリガー領域にいないこと」を追加し、
    表示条件と閉じ条件の矛盾によるループを解消。

v1.7.2
  - スタートアップ登録の失敗を修正。comtypes の WScript.Shell が
    'Save' を持たない(IDispatch展開の不具合)ため登録できなかった。
    pywin32 があればそれを使い、無ければ PowerShell でショートカットを
    作る二段構えに変更（pywin32 未導入でも動く）。

v1.7.1
  - スタートアップ登録/解除の結果を Windows 通知で画面に表示。
    pythonw 起動でも成功/失敗とエラー内容が見えるようになった。
  - スタートアップ登録処理を強化（各ステップを個別にチェックして
    どこで失敗したか分かるエラーメッセージを返す）。
    別スレッドからの呼び出しで起きる COM 初期化漏れも対策。

v1.7.0
  - 描画方式を刷新。ウィンドウを毎回 表示/非表示(deiconify/withdraw)
    する方式をやめ、画面外に常駐させて位置だけスライドさせる方式に変更。
    出だしのカクつきが減り、アニメがより滑らかに。
  - フルスクリーンゲーム等への影響を避けるため、最前面(topmost)は
    パネルを見せている間だけ ON にし、隠れている間は OFF にする。

v1.6.0
  - 音量の数値表示を追加。
    「デバイス全体の音量 (xx%)」のように見出しに％を表示。
    ミキサーも各アプリ名の横に (yy%) を表示。スライダー操作に追従。
  - パネルの高さを表示項目数に合わせて自動調整（内容を実測して決定）。
    アプリが増減してもピッタリのサイズで表示。空白の間延びも解消。
    画面の高さを超える場合は頭打ち（必要なら将来スクロール化）。
    調整用: MIN_HEIGHT / MARGIN_BOTTOM。

v1.5.1
  - 出現アニメと消失アニメを共通処理(_slide)に統一。コマ数・間隔・
    イージングを揃え、出入りが対称でなめらかに。
  - 出現時の1コマ目のカクつき(画面外からのワープ)を修正
    （開始位置で一度描画してからアニメ開始）。
  - アニメ速度は SLIDE_FRAMES / SLIDE_INTERVAL で調整可能。

v1.5.0
  - マウスがパネルから離れたら自動で閉じる方式を追加（設定 CLOSE_ON_LEAVE）。
    パネルの周囲にパネルサイズの一定割合(既定10%)の余白を設け、
    そこを超えて離れたら閉じる（CLOSE_MARGIN_RATIO で調整可）。
    False にすると従来の「外側クリックで閉じる」に戻せる。
  - 閉じるときも右へスライドして消えるアニメを追加（設定 CLOSE_ANIMATE）。

v1.4.0
  - スタートアップ登録機能を追加。トレイの右クリックメニューの
    「スタートアップに登録」で、Windows起動時の自動起動をオン/オフできる
    （チェックマークで現在の状態を表示）。
    スタートアップフォルダに pythonw 起動のショートカットを置く方式。
  - pythonw（黒窓なし）で起動しても落ちないよう stdout/stderr を保護。

v1.3.0
  - 高DPI対応を追加。拡大表示(125%等)でも文字がにじまず鮮明に。
  - パネルの外をクリックすると閉じるように修正（枠なし窓でFocusOutが
    効かない問題に対応。マウスのクリックを監視して判定）。
  - ミキサーのレイアウト変更: アプリ名を各音量バーの上に表示し、行間を確保。
  - 上記に合わせてパネルの高さを拡大。

v1.2.0
  - 右端ホバーを全モニタ対応に（EDGE_SCREEN="any" を既定に）。
    ctypes で全モニタの矩形を取得し、触れたモニタの右端にパネルを出す。
  - 「即出す」モードを追加（設定 EDGE_INSTANT）。
    False=一瞬留まったら出す（既定）/ True=触れたら即出す。

v1.1.0
  - 画面右端にマウスを当てるとパネルが右からスライド表示される機能を追加。
    （誤爆防止のため、右端に少し留まると反応／既定はメインモニタのみ）
    調整用の設定はファイル上部 EDGE_* にまとめてあります。
  - ライトテーマに戻した。

v1.0.2
  - 起動診断を強化。起動時にコンソールへ案内を表示。
  - トレイ起動を try で囲み、失敗時はエラーを表示。
  - トレイが出ない環境でも操作できるよう、起動直後にパネルを1度表示。
  - 起動時エラーで黒い窓が即閉じしないようガードを追加。

v1.0.1
  - 既定デバイス取得と全体音量の修正（その2）。
    GetSpeakers() は AudioDevice を返すと判明したため、
    .id / .EndpointVolume プロパティを使う正しい呼び方に変更。
  - 未使用 import を整理。

v1.0.0
  - 初の安定版。デバイス切り替え／全体音量／アプリごとミキサーが動作。
  - 最新 pycaw(20251023) に対応（既定デバイス取得・全体音量の呼び方を修正）。
  - 出力デバイスのみ列挙（マイク等の入力を除外）。
  - 本家フライアウト風UI（ダークテーマ）。
  - 表示直後の誤クローズを防ぐフォーカスガードを追加。
  - 自己診断モード( --check )を搭載。
  - pycaw の警告メッセージを抑制。
-------------------------------------------------------------------
"""

__version__ = "1.8.1"


import os
import sys
import threading
import warnings
import tkinter as tk
from tkinter import ttk

# --- 高DPI対応（ぼやけ防止）-------------------------------------------------
# Windowsのディスプレイ拡大(125%等)でも文字がにじまないようにする。
def _enable_dpi_awareness():
    try:
        import ctypes
        # まず Per-Monitor v2 を試す（一番きれい）。だめなら System DPI Aware。
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(2)  # PROCESS_PER_MONITOR_DPI_AWARE
        except Exception:
            ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

_enable_dpi_awareness()

# pythonw.exe で起動された場合 stdout/stderr が None になり print が失敗するため、
# 無害なダミーに差し替えておく（黒窓なし起動でも落ちないように）。
if sys.stdout is None or sys.stderr is None:
    import io
    if sys.stdout is None:
        sys.stdout = io.StringIO()
    if sys.stderr is None:
        sys.stderr = io.StringIO()

# pycaw が一部デバイスのプロパティ取得に失敗したとき出す警告を抑制（動作に影響なし）
warnings.filterwarnings("ignore", category=UserWarning, module="pycaw")

from pycaw.pycaw import (
    AudioUtilities,
    ISimpleAudioVolume,
    AudioDeviceState,
)
from pycaw.constants import ERole, EDataFlow

import pystray
from PIL import Image, ImageDraw

import ctypes
from ctypes import wintypes


# ===========================================================================
#  モニタ情報の取得（全モニタの矩形を得る／追加ライブラリ不要）
# ===========================================================================
def get_all_monitors():
    """全モニタの矩形を [(left, top, right, bottom), ...] で返す。
    取得に失敗した場合はプライマリのみのリストを返す。"""
    monitors = []

    # MONITORINFO 構造体（rcMonitor を取り出すのに使う）
    class RECT(ctypes.Structure):
        _fields_ = [("left", ctypes.c_long), ("top", ctypes.c_long),
                    ("right", ctypes.c_long), ("bottom", ctypes.c_long)]

    class MONITORINFO(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.c_ulong), ("rcMonitor", RECT),
                    ("rcWork", RECT), ("dwFlags", ctypes.c_ulong)]

    try:
        user32 = ctypes.windll.user32

        # コールバックの型: (HMONITOR, HDC, LPRECT, LPARAM) -> BOOL
        MonitorEnumProc = ctypes.WINFUNCTYPE(
            ctypes.c_int, ctypes.c_ulonglong, ctypes.c_ulonglong,
            ctypes.POINTER(RECT), ctypes.c_longlong
        )

        def _callback(hmon, hdc, lprc, lparam):
            mi = MONITORINFO()
            mi.cbSize = ctypes.sizeof(MONITORINFO)
            if user32.GetMonitorInfoW(hmon, ctypes.byref(mi)):
                r = mi.rcMonitor
                monitors.append((r.left, r.top, r.right, r.bottom))
            return 1

        user32.EnumDisplayMonitors(0, 0, MonitorEnumProc(_callback), 0)
    except Exception:
        pass

    if not monitors:
        # 失敗時のフォールバック: プライマリだけ（tk から取得）
        try:
            root = tk._default_root
            if root is not None:
                w = root.winfo_screenwidth()
                h = root.winfo_screenheight()
                monitors.append((0, 0, w, h))
        except Exception:
            pass
    return monitors


# ===========================================================================
#  スタートアップ登録の管理（スタートアップフォルダにショートカットを置く方式）
# ===========================================================================
SHORTCUT_NAME = "AudioSidebar.lnk"

def _startup_dir():
    """現在のユーザーのスタートアップフォルダのパス。"""
    return os.path.join(
        os.environ["APPDATA"],
        r"Microsoft\Windows\Start Menu\Programs\Startup",
    )

def _shortcut_path():
    return os.path.join(_startup_dir(), SHORTCUT_NAME)

def _pythonw_path():
    """黒窓を出さない pythonw.exe のパスを返す。見つからなければ python.exe。"""
    # python.exe と同じ場所に pythonw.exe があるのが普通
    exe = sys.executable  # 今動いている python のパス
    cand = exe.replace("python.exe", "pythonw.exe")
    if os.path.exists(cand):
        return cand
    # 念のため同じフォルダを探す
    folder = os.path.dirname(exe)
    cand2 = os.path.join(folder, "pythonw.exe")
    if os.path.exists(cand2):
        return cand2
    return exe  # 最後の手段（黒窓が出る可能性あり）

def is_startup_enabled():
    return os.path.exists(_shortcut_path())

def _make_shortcut_pywin32(path, target, args, workdir, desc):
    """pywin32 でショートカット作成。成功すれば True。pywin32 が無ければ ImportError。"""
    import win32com.client  # pywin32
    shell = win32com.client.Dispatch("WScript.Shell")
    sc = shell.CreateShortcut(path)
    sc.TargetPath = target
    sc.Arguments = args
    sc.WorkingDirectory = workdir
    sc.WindowStyle = 7
    sc.Description = desc
    sc.Save()
    return True

def _make_shortcut_powershell(path, target, args, workdir, desc):
    """PowerShell を呼んでショートカット作成（追加ライブラリ不要）。"""
    import subprocess
    # PowerShell のシングルクォート文字列用に ' を '' へエスケープ
    def q(s):
        return s.replace("'", "''")
    ps = (
        "$ws = New-Object -ComObject WScript.Shell; "
        f"$s = $ws.CreateShortcut('{q(path)}'); "
        f"$s.TargetPath = '{q(target)}'; "
        f"$s.Arguments = '{q(args)}'; "
        f"$s.WorkingDirectory = '{q(workdir)}'; "
        "$s.WindowStyle = 7; "
        f"$s.Description = '{q(desc)}'; "
        "$s.Save()"
    )
    # 黒窓を出さずに実行
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    result = subprocess.run(
        ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps],
        capture_output=True, text=True, startupinfo=si,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "PowerShell 実行に失敗")
    return True

def enable_startup():
    """スタートアップフォルダに、このスクリプトを pythonw で起動する
    ショートカットを作る。pywin32 → PowerShell の順で試す。"""
    import traceback
    try:
        # 1) ファイルパスを確実に絶対パス化
        script = os.path.abspath(__file__)
        if not os.path.exists(script):
            return False, f"スクリプト本体が見つかりません: {script}"

        # 2) pythonw.exe のパス
        target = _pythonw_path()
        if not target or not os.path.exists(target):
            return False, f"pythonw.exe が見つかりません (target={target})"

        # 3) スタートアップフォルダの確認・作成
        startup_dir = _startup_dir()
        if not os.path.isdir(startup_dir):
            os.makedirs(startup_dir, exist_ok=True)

        path = _shortcut_path()
        args = f'"{script}"'
        workdir = os.path.dirname(script)
        desc = "Audio Sidebar 自動起動"

        # 4) まず pywin32、ダメなら PowerShell の順で試す
        errors = []
        for method in (_make_shortcut_pywin32, _make_shortcut_powershell):
            try:
                method(path, target, args, workdir, desc)
                if os.path.exists(path):
                    return True, None
                errors.append(f"{method.__name__}: 実行後にファイルが見つからない")
            except ImportError:
                errors.append(f"{method.__name__}: ライブラリ未導入のためスキップ")
            except Exception as e:
                errors.append(f"{method.__name__}: {type(e).__name__}: {e}")

        return False, "すべての方法が失敗:\n" + "\n".join(errors)
    except Exception as e:
        return False, f"{type(e).__name__}: {e}\n{traceback.format_exc()}"

def disable_startup():
    try:
        p = _shortcut_path()
        if os.path.exists(p):
            os.remove(p)
        return True, None
    except Exception as e:
        return False, str(e)


# ===========================================================================
#  オーディオ操作ロジック（UIから分離）
# ===========================================================================
class AudioController:

    # --- 出力デバイス一覧 ---------------------------------------------------
    @staticmethod
    def list_output_devices():
        """有効な出力デバイス [(id, name), ...] を返す。"""
        result = []
        # eRender を指定して出力デバイスだけ列挙（マイク等の入力を除外）
        for d in AudioUtilities.GetAllDevices(data_flow=EDataFlow.eRender.value):
            try:
                if d.state == AudioDeviceState.Active:
                    result.append((d.id, d.FriendlyName))
            except Exception:
                continue
        return result

    @staticmethod
    def get_default_device_id():
        # GetSpeakers() は AudioDevice を返すので .id プロパティを使う
        spk = AudioUtilities.GetSpeakers()
        return spk.id

    # --- 既定デバイス切り替え ----------------------------------------------
    @staticmethod
    def set_default_device(device_id):
        """device_id を既定の出力デバイスにする。"""
        try:
            # 最新pycawの公式メソッド。3つのロール全部に設定する。
            AudioUtilities.SetDefaultDevice(
                device_id,
                roles=[ERole.eConsole, ERole.eMultimedia, ERole.eCommunications],
            )
            return True, None
        except Exception as e:
            return False, f"SetDefaultDevice: {e}"

    # --- マスター音量 -------------------------------------------------------
    @staticmethod
    def _endpoint_volume():
        # GetSpeakers() は AudioDevice。 .EndpointVolume が音量制御インターフェース。
        spk = AudioUtilities.GetSpeakers()
        return spk.EndpointVolume

    @classmethod
    def get_master_volume(cls):
        return cls._endpoint_volume().GetMasterVolumeLevelScalar()

    @classmethod
    def set_master_volume(cls, scalar):
        cls._endpoint_volume().SetMasterVolumeLevelScalar(float(scalar), None)

    @classmethod
    def get_master_mute(cls):
        return bool(cls._endpoint_volume().GetMute())

    @classmethod
    def set_master_mute(cls, mute):
        cls._endpoint_volume().SetMute(1 if mute else 0, None)

    # --- アプリごとセッション ----------------------------------------------
    @staticmethod
    def list_sessions():
        """[(name, iface, scalar, muted), ...]"""
        result = []
        for s in AudioUtilities.GetAllSessions():
            try:
                vol = s._ctl.QueryInterface(ISimpleAudioVolume)
                name = s.Process.name() if s.Process else "システム音"
                result.append((name, vol, vol.GetMasterVolume(), bool(vol.GetMute())))
            except Exception:
                continue
        return result


# ===========================================================================
#  色・フォント（ライトテーマ）
# ===========================================================================
BG      = "#f3f3f3"   # パネル背景
CARD    = "#fbfbfb"   # 行の背景
TEXT    = "#1a1a1a"
SUBTEXT = "#555555"
ACCENT  = "#0067c0"   # Windowsの青
SEL_BG  = "#eaeaea"   # 選択中デバイスの背景
TROUGH  = "#d0d0d0"   # スライダーの溝の色
FONT    = ("Yu Gothic UI", 10)
FONT_B  = ("Yu Gothic UI", 11, "bold")

# ===========================================================================
#  エッジ・スワイプ（右端ホバーで表示）の設定 — 数字を変えて調整できます
# ===========================================================================
EDGE_ENABLED   = True   # 右端ホバー機能のオン/オフ
EDGE_INSTANT   = False  # True にすると「即出す」。False は「一瞬留まったら出す」
EDGE_TRIGGER_PX = 3     # 画面右端から何ピクセル以内をトリガー領域とするか
EDGE_DWELL_MS  = 300    # 右端に何ミリ秒留まったら表示するか（EDGE_INSTANT=Falseのとき有効）
EDGE_POLL_MS   = 60     # マウス位置を監視する間隔（ミリ秒）
# 反応させる右端: "any"=全モニタの右端 / "primary"=メインモニタの右端だけ
EDGE_SCREEN    = "any"

# 閉じ方の設定
# CLOSE_ON_LEAVE=True: マウスがパネル(＋余白)の外に出たら自動で閉じる
# False の場合は従来どおり「パネル外をクリックしたら閉じる」
CLOSE_ON_LEAVE = True
# 余白の割合。パネルサイズに対する比率で、この分だけ外側まで離れても閉じない。
# 例: 0.10 なら 幅の10%・高さの10% 外側まで猶予。
CLOSE_MARGIN_RATIO = 0.10
# 閉じるときに右へスライドして消すアニメをするか
CLOSE_ANIMATE = True

# --- 閉じ方の設定 ---
# マウスがパネルの外に出たら閉じる（True）/ 外側クリックで閉じる（False）
CLOSE_ON_LEAVE = True
# パネル外に出たと判定するまでの「余裕」。ウィンドウ幅・高さに対する割合。
# 0.10 ならウィンドウサイズの10%ぶん外側まではみ出しても閉じない。
CLOSE_MARGIN_RATIO = 0.10
# パネルを出した直後、この時間(ms)は「枠外に出た」判定をしない（出した瞬間の誤爆防止）
CLOSE_LEAVE_GRACE_MS = 500


# ===========================================================================
#  ポップアップパネル
# ===========================================================================
class ControlPanel(tk.Toplevel):
    WIDTH = 360
    HEIGHT = 640          # 初期値（実際の高さは内容に合わせて毎回計算する）
    MIN_HEIGHT = 200      # これより低くはしない
    MARGIN_BOTTOM = 60    # 画面下端から空ける余白（タスクバー等）

    def __init__(self, master):
        super().__init__(master)
        self.overrideredirect(True)
        # 既定では最前面にしない（フルスクリーンゲーム等への影響を避ける）。
        # 表示する瞬間だけ topmost を ON にする。
        self.attributes("-topmost", False)
        self.configure(bg=BG)
        self._height = self.HEIGHT     # 実際に使う高さ（内容に応じて変わる）
        self._visible = False          # 論理的な表示状態（画面内にいるか）
        self._offscreen_x = 0          # 画面外の待機X座標
        # 表示直後の誤クローズを防ぐためのガードフラグ
        self._ignore_focus_out = True
        self._closing = False          # 閉じるアニメ実行中フラグ
        self._cur_x = 0                # 現在位置（閉じるアニメ用）
        self._cur_y = 0
        self._cur_edge_right = 0
        # 表示中の所属モニタ情報（閉じアニメで使う）
        self._mon_top = 0
        self._mon_bottom = 0
        # パネルが隠れたときに呼ぶコールバック（TrayApp が設定）
        self.on_hide = None
        self._build_ui()
        self.bind("<FocusOut>", self._on_focus_out)
        self.bind("<Escape>", lambda e: self.hide())
        # 起動時に画面外へ逃がして常駐させる（deiconify/withdraw を使わない）
        self._park_offscreen()

    def _park_offscreen(self):
        """ウィンドウを画面の右外に置いて見えなくする（常駐）。"""
        self.update_idletasks()
        sw = self.winfo_screenwidth()
        self._offscreen_x = sw + 50          # 右端のさらに外
        self.geometry(f"{self.WIDTH}x{self._height}+{self._offscreen_x}+100")
        self.attributes("-topmost", False)
        self._visible = False

    # ---- レイアウト構築 ----------------------------------------------------
    def _build_ui(self):
        # ttk スタイル（スライダーを細く青く）
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except Exception:
            pass
        style.configure("Vol.Horizontal.TScale", background=CARD,
                        troughcolor=TROUGH)

        # 見出し: 出力デバイス
        self._heading("出力デバイス")

        # デバイスリストの入れ物
        self.device_box = tk.Frame(self, bg=BG)
        self.device_box.pack(fill="x", padx=10)

        # 見出し: デバイス全体の音量（数値も表示するので参照を保持）
        self.master_heading = self._heading("デバイス全体の音量")
        master_row = tk.Frame(self, bg=BG)
        master_row.pack(fill="x", padx=14, pady=(0, 4))
        self.master_mute_btn = tk.Label(master_row, text="🔊", bg=BG,
                                        font=("Segoe UI Emoji", 13), cursor="hand2")
        self.master_mute_btn.pack(side="left", padx=(0, 8))
        self.master_mute_btn.bind("<Button-1>", lambda e: self._toggle_master_mute())
        self.master_scale = ttk.Scale(master_row, from_=0, to=100,
                                      orient="horizontal",
                                      style="Vol.Horizontal.TScale",
                                      command=self._on_master_change)
        self.master_scale.pack(side="left", fill="x", expand=True)

        # 見出し: 音量ミキサー
        self._heading("音量ミキサー")
        self.mixer_box = tk.Frame(self, bg=BG)
        self.mixer_box.pack(fill="x", padx=10)

        # 下部の更新ボタン
        bottom = tk.Frame(self, bg=BG)
        bottom.pack(fill="x", side="bottom", pady=6)
        tk.Button(bottom, text="🔄 更新", relief="flat", bg=BG, fg=SUBTEXT,
                  cursor="hand2", command=self.refresh).pack()

    def _heading(self, text):
        lbl = tk.Label(self, text=text, bg=BG, fg=TEXT, font=FONT_B,
                       anchor="w")
        lbl.pack(fill="x", padx=14, pady=(12, 4))
        return lbl

    # ---- 配置 --------------------------------------------------------------
    def _place_bottom_right(self):
        # トレイクリック時の従来配置（右下）
        self.update_idletasks()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self._measure_height(sh)
        x = sw - self.WIDTH - 12
        y = sh - self._height - 56
        self.geometry(f"{self.WIDTH}x{self._height}+{x}+{y}")

    # ---- 状態反映 ----------------------------------------------------------
    def refresh(self):
        self._build_device_list()
        self._build_master()
        self._build_mixer()

    def _build_device_list(self):
        for w in self.device_box.winfo_children():
            w.destroy()
        self._devices = AudioController.list_output_devices()
        try:
            cur_id = AudioController.get_default_device_id()
        except Exception:
            cur_id = None

        for (did, name) in self._devices:
            selected = (did == cur_id)
            row = tk.Frame(self.device_box, bg=SEL_BG if selected else BG,
                           cursor="hand2")
            row.pack(fill="x", pady=1)
            # 選択中を示す左の青バー
            bar = tk.Frame(row, bg=ACCENT if selected else (SEL_BG if selected else BG),
                           width=3)
            bar.pack(side="left", fill="y")
            tk.Label(row, text="🎧", bg=row["bg"],
                     font=("Segoe UI Emoji", 11)).pack(side="left", padx=(8, 6), pady=8)
            tk.Label(row, text=name, bg=row["bg"], fg=TEXT, font=FONT,
                     anchor="w").pack(side="left", fill="x", expand=True)

            # 行クリックで切り替え（子ウィジェットにも同じ動作を割り当て）
            def make_handler(device_id=did):
                return lambda e: self._switch_device(device_id)
            for widget in (row, *row.winfo_children()):
                widget.bind("<Button-1>", make_handler())

    def _build_master(self):
        try:
            v = AudioController.get_master_volume()
            self.master_scale.set(v * 100)
            self._set_master_icon(AudioController.get_master_mute())
            self._update_master_heading(v * 100)
        except Exception as e:
            print("master read failed:", e)

    def _update_master_heading(self, percent):
        try:
            self.master_heading.config(
                text=f"デバイス全体の音量 ({int(round(percent))}%)"
            )
        except Exception:
            pass

    def _measure_height(self, screen_h=None):
        """中身が必要とする高さを測って self._height に設定する。
        画面高さを超えそうなときは画面に収まるよう上限を掛ける。"""
        self.update_idletasks()
        req = self.winfo_reqheight()      # 中身が要求する高さ
        h = max(self.MIN_HEIGHT, req)
        if screen_h:
            limit = screen_h - self.MARGIN_BOTTOM
            if h > limit:
                h = limit                 # 画面に収まらない分は頭打ち（将来スクロール化候補）
        self._height = int(h)
        return self._height

    def _build_mixer(self):
        for w in self.mixer_box.winfo_children():
            w.destroy()
        try:
            sessions = AudioController.list_sessions()
        except Exception as e:
            print("session list failed:", e)
            sessions = []
        for (name, vol, scalar, muted) in sessions:
            self._add_session_row(name, vol, scalar, muted)

    def _add_session_row(self, name, iface, scalar, muted):
        # 行全体（上にアプリ名、下にミュート+スライダーの2段）。行間を空ける。
        row = tk.Frame(self.mixer_box, bg=BG)
        row.pack(fill="x", pady=(8, 2))

        # 上段: アプリ名 + 音量％
        name_lbl = tk.Label(row, bg=BG, fg=TEXT, font=FONT, anchor="w")
        name_lbl.pack(fill="x", padx=2)

        def set_name(percent, n=name, lbl=name_lbl):
            lbl.config(text=f"{n}  ({int(round(percent))}%)")
        set_name(scalar * 100)

        # 下段: ミュートアイコン + スライダー
        bar = tk.Frame(row, bg=BG)
        bar.pack(fill="x", pady=(1, 0))

        mute_lbl = tk.Label(bar, text="🔇" if muted else "🔊", bg=BG,
                            font=("Segoe UI Emoji", 11), cursor="hand2", width=2)
        mute_lbl.pack(side="left", padx=(2, 6))

        scale = ttk.Scale(bar, from_=0, to=100, orient="horizontal",
                          style="Vol.Horizontal.TScale")
        scale.set(scalar * 100)
        scale.pack(side="left", fill="x", expand=True, padx=(0, 6))
        if muted:
            scale.state(["disabled"])

        def on_move(value, i=iface, upd=set_name):
            i.SetMasterVolume(float(value) / 100.0, None)
            upd(float(value))   # 名前横の％を追従
        scale.config(command=on_move)

        def toggle_mute(e, i=iface, lbl=mute_lbl, sc=scale):
            new = not bool(i.GetMute())
            i.SetMute(1 if new else 0, None)
            lbl.config(text="🔇" if new else "🔊")
            if new:
                sc.state(["disabled"])
            else:
                sc.state(["!disabled"])
        mute_lbl.bind("<Button-1>", toggle_mute)

    # ---- イベント ----------------------------------------------------------
    def _switch_device(self, device_id):
        ok, err = AudioController.set_default_device(device_id)
        if not ok:
            print("device switch failed:", err)
        self.refresh()

    def _on_master_change(self, value):
        AudioController.set_master_volume(float(value) / 100.0)
        self._update_master_heading(float(value))

    def _toggle_master_mute(self):
        new = not AudioController.get_master_mute()
        AudioController.set_master_mute(new)
        self._set_master_icon(new)

    def _set_master_icon(self, muted):
        self.master_mute_btn.config(text="🔇" if muted else "🔊")

    # ---- 表示制御 ----------------------------------------------------------
    def _on_focus_out(self, event=None):
        # 表示直後はフォーカスが不安定なので一定時間は閉じない
        if self._ignore_focus_out:
            return
        self.hide()

    def hide(self):
        """右へスライドして画面外へ退避して閉じる。"""
        # 表示していない、またはアニメ中なら何もしない
        if not self._visible or getattr(self, "_closing", False):
            return
        if not CLOSE_ANIMATE:
            self.hide_now()
            return
        self._closing = True
        self._ignore_focus_out = True  # アニメ中の誤判定を防ぐ
        x_from = getattr(self, "_cur_x", self.winfo_x())
        y = getattr(self, "_cur_y", self.winfo_y())
        edge_right = getattr(self, "_cur_edge_right", self.winfo_screenwidth())
        # 画面外（右端の外）まで滑らせる
        off = edge_right + 50
        self._slide(x_from, off, y, on_done=self._after_slide_out)

    def _animate_slide_out(self, x_from, edge_right, y, step):
        # 後方互換のため残置（現在は hide から直接 _slide を呼ぶ）
        self._slide(x_from, edge_right + 50, y, on_done=self._after_slide_out)

    def _after_slide_out(self):
        self._closing = False
        self._visible = False
        self.attributes("-topmost", False)   # 隠れたら最前面を解除
        self._offscreen_x = self.winfo_x()
        if self.on_hide:
            self.on_hide()

    def hide_now(self):
        """アニメなしで即座に画面外へ退避（終了処理などで使用）。"""
        self._closing = False
        self._park_offscreen()
        if self.on_hide:
            self.on_hide()

    def _refresh_guarded(self):
        """refresh が失敗しても固まらないように保護して呼ぶ。"""
        try:
            self.refresh()
        except Exception as e:
            import traceback
            traceback.print_exc()
            err = tk.Label(self, text=f"エラー:\n{e}", bg=BG, fg="#c00000",
                           font=FONT, justify="left", wraplength=self.WIDTH - 30)
            err.pack(padx=14, pady=14)

    def _after_present(self):
        """表示後に共通で行う処理（最前面化とフォーカスガード）。"""
        self._ignore_focus_out = True
        self._visible = True
        self.attributes("-topmost", True)   # 見せる瞬間だけ最前面
        self.lift()
        self.focus_force()
        self.after(400, self._enable_focus_out)

    def show(self):
        """トレイクリック用: 右下に即表示。"""
        self._refresh_guarded()
        self._place_bottom_right()    # 中身を測ってサイズと位置を決める
        self.update_idletasks()
        # 閉じるアニメ用に現在位置と所属モニタ右端を記録
        self._cur_x = self.winfo_x()
        self._cur_y = self.winfo_y()
        self._cur_edge_right = self.winfo_screenwidth()
        self._after_present()

    def slide_in(self, edge_right=None, top=None, bottom=None):
        """右端ホバー用: 指定モニタの右外から横にスライドして表示する。
        edge_right: 出すモニタの右端X。top/bottom: そのモニタの上下端Y。
        いずれも None ならプライマリ基準にフォールバック。"""
        # すでに表示中、または閉じアニメ中なら無視（二重起動防止）
        if self._visible or getattr(self, "_closing", False):
            return
        self._refresh_guarded()
        self.update_idletasks()

        if edge_right is None:
            # フォールバック（プライマリの右端、縦中央）
            sw = self.winfo_screenwidth()
            sh = self.winfo_screenheight()
            edge_right, top, bottom = sw, 0, sh

        # 中身に合わせて高さを測る（モニタ高さを上限に）
        mon_h = bottom - top
        self._measure_height(mon_h)

        x_end = edge_right - self.WIDTH - 8        # 着地点（右端から少し内側）
        # そのモニタの縦中央あたりに合わせる
        y = top + max(20, (mon_h - self._height) // 2)
        x_start = edge_right                       # 開始は右端の外側

        # 閉じるアニメ用に記録
        self._cur_x = x_end
        self._cur_y = y
        self._cur_edge_right = edge_right

        self.geometry(f"{self.WIDTH}x{self._height}+{x_start}+{y}")
        self._ignore_focus_out = True
        self._visible = True
        self.attributes("-topmost", True)   # 見せる瞬間だけ最前面
        self.lift()
        # 開始位置(画面外)で確実に一度描画させてからアニメ開始（1コマ目の飛び防止）
        self.update_idletasks()
        self._slide(x_start, x_end, y, on_done=self._after_slide_in)

    def _animate_slide(self, x_start, x_end, y, step):
        # 出現も共通アニメ(_slide)を使う。互換のため引数は残す。
        self._slide(x_start, x_end, y, on_done=self._after_slide_in)

    def _after_slide_in(self):
        self.focus_force()
        self.after(400, self._enable_focus_out)

    # ---- 共通スライドアニメ（出現・消失で同じ方式） -----------------------
    SLIDE_FRAMES = 12     # コマ数（多いほどゆっくり滑らか）
    SLIDE_INTERVAL = 12   # コマ間隔ミリ秒

    def _slide(self, x_from, x_to, y, on_done=None, step=0):
        """x_from → x_to へ一定方式でスライドさせる共通処理。
        出現・消失の両方がこれを使うので、見た目が必ず揃う。"""
        frames = self.SLIDE_FRAMES
        if step > frames:
            # 着地点に正確に合わせて終了
            self.geometry(f"{self.WIDTH}x{self._height}+{int(x_to)}+{y}")
            if on_done:
                on_done()
            return
        t = step / frames
        # イーズイン・アウト（両端がなめらか）。出現・消失とも同じカーブ。
        ease = (t * t) / (t * t + (1 - t) * (1 - t)) if 0 < t < 1 else t
        x = int(x_from + (x_to - x_from) * ease)
        self.geometry(f"{self.WIDTH}x{self._height}+{x}+{y}")
        self.after(self.SLIDE_INTERVAL,
                   lambda: self._slide(x_from, x_to, y, on_done, step + 1))

    def _enable_focus_out(self):
        self._ignore_focus_out = False


# ===========================================================================
#  トレイ常駐
# ===========================================================================
class TrayApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.panel = ControlPanel(self.root)
        # パネルは画面外に常駐させる方式（withdraw しない）
        # パネルが閉じたら右端ホバーの表示フラグを下ろす
        self.panel.on_hide = self._on_panel_hidden
        # 右端ホバー検出用の状態
        self._edge_dwell = 0          # 右端に留まっている累積ミリ秒
        self._edge_shown = False      # スワイプで表示中かどうか
        self._lmb_was_down = False    # 左クリックの前回状態（立ち上がり検出用）
        self._paused = False          # 停止中フラグ（右端ホバーを止める）
        self.icon = pystray.Icon(
            "audio_sidebar", self._icon_image(), f"Audio Control v{__version__}",
            menu=pystray.Menu(
                pystray.MenuItem("パネルを開く", self._open, default=True),
                pystray.MenuItem(
                    "停止",
                    self._toggle_pause,
                    checked=lambda item: self._paused,
                ),
                pystray.MenuItem(
                    "スタートアップに登録",
                    self._toggle_startup,
                    checked=lambda item: is_startup_enabled(),
                ),
                pystray.MenuItem("終了", self._quit),
            ),
        )

    def _toggle_pause(self, icon=None, item=None):
        """右端ホバーの監視を停止/再開する。トレイ常駐は維持。"""
        self._paused = not self._paused
        # 停止に切り替えた瞬間にパネルが出ていれば閉じる
        if self._paused and self.panel._visible:
            self.panel.hide()
        # ホバーまわりの内部状態をリセット
        self._edge_dwell = 0
        self._edge_shown = False
        # フィードバックはコマンドプロンプトのみ
        print("[停止]" if self._paused else "[再開]",
              "右端ホバーの監視を" + ("停止しました。" if self._paused else "再開しました。"))
        try:
            self.icon.update_menu()
        except Exception:
            pass

    def _toggle_startup(self, icon=None, item=None):
        """スタートアップ登録のオン/オフを切り替える。"""
        if is_startup_enabled():
            ok, err = disable_startup()
            title = "スタートアップ" if ok else "解除に失敗"
            msg = "登録を解除しました。" if ok else f"{err}"
        else:
            ok, err = enable_startup()
            title = "スタートアップ" if ok else "登録に失敗"
            if ok:
                msg = f"登録しました。\n{_shortcut_path()}"
            else:
                msg = f"{err}"
        # フィードバックはコマンドプロンプトのみ
        print(title, msg)
        # メニューのチェック表示を更新
        try:
            self.icon.update_menu()
        except Exception:
            pass

    # ---- 右端ホバー監視 ----------------------------------------------------
    def _at_right_edge(self, px, py):
        """カーソルがいずれかのモニタの右端トリガー領域にいるか判定。
        いれば (right, top, bottom)、いなければ None を返す。"""
        for (left, top, right, bottom) in get_all_monitors():
            if EDGE_SCREEN == "primary" and not (left == 0 and top == 0):
                continue
            near_right = (right - EDGE_TRIGGER_PX) <= px <= right
            in_height = top <= py <= bottom
            if near_right and in_height:
                return (right, top, bottom)
        return None

    def _edge_watch(self):
        """マウス位置を定期的に見て、いずれかのモニタの右端に来たらパネルを出す。"""
        if not EDGE_ENABLED:
            return
        try:
            px = self.root.winfo_pointerx()
            py = self.root.winfo_pointery()

            if self._paused:
                # 停止中: 右端ホバー検出は止めるが、手動で開いたパネルの
                # 閉じ判定は引き続き動かす（クリック/離脱どちらでも閉じる）。
                if CLOSE_ON_LEAVE:
                    self._check_leave(px, py, at_edge=False)
                else:
                    self._check_outside_click(px, py)
                self.root.after(EDGE_POLL_MS, self._edge_watch)
                return

            # マウスが「どれかのモニタの右端付近」にいるか
            hit = self._at_right_edge(px, py)
            at_edge = hit is not None

            if at_edge and not self._edge_shown:
                if EDGE_INSTANT:
                    # 即出す
                    self._edge_shown = True
                    self._edge_dwell = 0
                    self.panel.slide_in(edge_right=hit[0], top=hit[1], bottom=hit[2])
                else:
                    # 一瞬留まったら出す
                    self._edge_dwell += EDGE_POLL_MS
                    if self._edge_dwell >= EDGE_DWELL_MS:
                        self._edge_shown = True
                        self._edge_dwell = 0
                        self.panel.slide_in(edge_right=hit[0], top=hit[1], bottom=hit[2])
            elif not at_edge:
                self._edge_dwell = 0
                if self._edge_shown and not self._pointer_over_panel(px, py):
                    self._edge_shown = False

            # 閉じ判定: 設定に応じて「枠外に出たら」か「外側クリック」か
            if CLOSE_ON_LEAVE:
                self._check_leave(px, py, at_edge)
            else:
                self._check_outside_click(px, py)
        except Exception:
            pass
        self.root.after(EDGE_POLL_MS, self._edge_watch)

    def _check_leave(self, px, py, at_edge=False):
        """パネル表示中、マウスが余裕ゾーンの外に出たら閉じる。
        ただしカーソルが右端トリガー領域にいる間は閉じない
        （閉じ→再表示の無限ループを防ぐため）。"""
        try:
            if not self.panel._visible:
                return
            # 出した直後のガード中・閉じアニメ中は閉じない（誤爆/二重発火防止）
            if getattr(self.panel, "_ignore_focus_out", False):
                return
            if getattr(self.panel, "_closing", False):
                return
            # 右端トリガー領域にいる間は閉じない（表示条件を満たしているため）
            if at_edge:
                return
            x = self.panel.winfo_rootx()
            y = self.panel.winfo_rooty()
            w = self.panel.winfo_width()
            h = self.panel.winfo_height()
            mx = int(w * CLOSE_MARGIN_RATIO)   # 横の余裕
            my = int(h * CLOSE_MARGIN_RATIO)   # 縦の余裕
            inside = (x - mx) <= px <= (x + w + mx) and (y - my) <= py <= (y + h + my)
            if not inside:
                self.panel.hide()
        except Exception:
            pass

    def _check_outside_click(self, px, py):
        """パネル表示中に、パネルの外で左クリックされたら閉じる。"""
        try:
            import ctypes
            # 表示直後のガード中は閉じない（誤クローズ防止）
            if not self.panel._visible:
                self._lmb_was_down = False
                return
            if getattr(self.panel, "_ignore_focus_out", False):
                return
            # 左マウスボタンが「今押されているか」(最上位ビット)
            lmb_down = bool(ctypes.windll.user32.GetAsyncKeyState(0x01) & 0x8000)
            # 押された瞬間(立ち上がり)だけ判定する
            if lmb_down and not getattr(self, "_lmb_was_down", False):
                if not self._pointer_over_panel(px, py):
                    self.panel.hide()
            self._lmb_was_down = lmb_down
        except Exception:
            pass

    def _pointer_over_panel(self, px, py):
        """マウスがパネルの矩形内にあるか判定。"""
        try:
            if not self.panel._visible:
                return False
            x = self.panel.winfo_rootx()
            y = self.panel.winfo_rooty()
            w = self.panel.winfo_width()
            h = self.panel.winfo_height()
            return x <= px <= x + w and y <= py <= y + h
        except Exception:
            return False

    def _icon_image(self):
        img = Image.new("RGB", (64, 64), "#ffffff")
        d = ImageDraw.Draw(img)
        d.rectangle([18, 24, 28, 40], fill="#0067c0")
        d.polygon([(28, 24), (44, 14), (44, 50), (28, 40)], fill="#0067c0")
        return img

    def _on_panel_hidden(self):
        self._edge_shown = False
        self._edge_dwell = 0

    def _open(self, icon=None, item=None):
        self.root.after(0, self.panel.show)

    def _quit(self, icon=None, item=None):
        self.icon.stop()
        self.root.after(0, self.root.destroy)

    def _run_tray(self):
        """トレイ用スレッド本体。例外が出たらコンソールに表示する。"""
        try:
            self.icon.run()
        except Exception:
            import traceback
            print("[トレイ起動エラー] トレイアイコンの表示に失敗しました:")
            traceback.print_exc()
            print("→ トレイは使えませんが、パネルは下のウィンドウから操作できます。")

    def run(self):
        print(f"audio_sidebar v{__version__} を起動しました。")
        print("・トレイアイコンのクリック、または画面右端にマウスを当てると")
        print("  パネルが開きます（右端は少し留まると反応します）。")
        print("・終了するには、この黒い窓を閉じるか Ctrl+C を押してください。")
        # トレイをワーカースレッドで起動
        threading.Thread(target=self._run_tray, daemon=True).start()
        # 右端ホバーの監視を開始
        self.root.after(EDGE_POLL_MS, self._edge_watch)
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self._quit()


def run_self_check():
    """各オーディオ機能を1つずつ試して、どこで失敗するか表示する診断モード。
    使い方:  python audio_sidebar.py --check
    """
    import traceback
    print("=" * 50)
    print(f" オーディオ機能 自己診断  (audio_sidebar v{__version__})")
    print("=" * 50)

    # 0) pycaw のバージョン
    try:
        import pycaw
        print(f"[情報] pycaw version = {getattr(pycaw, '__version__', '不明')}")
    except Exception as e:
        print(f"[情報] pycaw バージョン取得失敗: {e}")

    # 1) デバイス一覧
    print("\n--- 1) 出力デバイス一覧 ---")
    try:
        devs = AudioController.list_output_devices()
        if not devs:
            print("  [!] デバイスが0件でした（取得方法がバージョンに合っていない可能性）")
        for (did, name) in devs:
            print(f"  - {name}")
        print("  -> OK")
    except Exception:
        print("  -> 失敗:")
        traceback.print_exc()

    # 2) 既定デバイスID
    print("\n--- 2) 既定デバイスの取得 ---")
    try:
        cur = AudioController.get_default_device_id()
        print(f"  既定ID = {cur}")
        print("  -> OK")
    except Exception:
        print("  -> 失敗:")
        traceback.print_exc()

    # 3) マスター音量
    print("\n--- 3) デバイス全体の音量 ---")
    try:
        v = AudioController.get_master_volume()
        m = AudioController.get_master_mute()
        print(f"  音量 = {v:.2f} / ミュート = {m}")
        print("  -> OK")
    except Exception:
        print("  -> 失敗:")
        traceback.print_exc()

    # 4) アプリごとセッション
    print("\n--- 4) アプリごとの音量セッション ---")
    try:
        sessions = AudioController.list_sessions()
        if not sessions:
            print("  [!] セッション0件（音を鳴らしているアプリがないだけかも）")
        for (name, _i, scalar, muted) in sessions:
            print(f"  - {name}: {scalar:.2f} (mute={muted})")
        print("  -> OK")
    except Exception:
        print("  -> 失敗:")
        traceback.print_exc()

    print("\n" + "=" * 50)
    print(" 診断おわり。失敗した項目の内容を貼ってください。")
    print("=" * 50)


if __name__ == "__main__":
    import sys
    if "--check" in sys.argv:
        run_self_check()
    else:
        try:
            TrayApp().run()
        except Exception:
            import traceback
            print("[起動エラー] アプリの起動に失敗しました:")
            traceback.print_exc()
            input("\nEnterキーを押すと閉じます...")  # 窓が即閉じしないように
