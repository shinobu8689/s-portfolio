**※日本語は英語の後にあります。／Japanese version below.**


# **Personal Development Projects**

### 🔸 StormworksPC (Lua / Stormworks Engine)

* **Purpose:** Built as a hobby project — I thought it could be created, so I decided to try.

* **Overview:**

  * Built an OS within the game *Stormworks*.
  * Modularized UI components and implemented their logic.
  * Since it relies on Stormworks’ unique game engine, it does not run outside the game.

* **Steam Workshop:** [https://steamcommunity.com/sharedfiles/filedetails/?id=3484118636](https://steamcommunity.com/sharedfiles/filedetails/?id=3484118636)

* **Live Demo Video:** [https://youtu.be/XJbS73MIA1s](https://youtu.be/XJbS73MIA1s)

* **Diagram & Code Walkthrough:** [https://youtu.be/BwLiGuqUqoo](https://youtu.be/BwLiGuqUqoo)

* **System Features:**

  * **Taskbar:** Launch applications by tapping app icons. Long press to open the Task Manager.
  * **Notification Menu:** Located on the right side of the taskbar. Doubles as a clock button. Shows module, chat, and battery notifications.
  * **Notification Pop-ups:** Incoming notifications highlight the menu button with the app’s icon and an “!” mark.
  * **Quick Settings:** Located on the left side of the taskbar. Doubles as a battery indicator. Provides brightness, music, and on-screen keyboard controls.
  * **Keyboard:** Includes an on-screen keyboard.
  * **Desktop Background:** Choose from 9 built-in wallpapers or set custom colors using hex codes with gradient mode.
  * **Animations:** Designed with smooth, eye-friendly transitions.
  * **Window Engine:** Each app window can be resized. The UI adapts depending on the window size.
  * **Window Snap:** While selecting an app window, use the “<” or “>” buttons to snap it to the left or right half of the screen.
  * **Fullscreen Mode:** Display the in-game PC screen directly to a monitor using goggles. Touch controls are disabled — navigation is via WASD keys, and Space acts as click.
  * **Code Optimisation:** Stormworks’ code blocks have strict character limits, so the system balances readability with compact code.
  * **Modularity:** Modules can be installed independently on other machines, saving space.

* **Built-in Apps:**

  * **Weather:** Displays temperature, humidity, and wind speed.
  * **Map:** Satellite map with navigation, search, and zoom functions.
  * **Camera:** Supports wired/wireless switching, zoom, infrared, and directional control.
  * **Notes:** Input via keyboard, supports text formatting and color per character, up to 9 pages.
  * **Settings:** Handles module connections, system info, Steam QR code, and credits.
  * **Extensions:** Supports third-party programs. If compatible with the OS API, hardware access is also possible.
  * **Chat:** Developed a custom in-game chat communication protocol.

---

### 🔸 MinecraftOnAWS (AWS / Linux)

* **Overview:** As part of my AWS learning, I built a Minecraft server on an EC2 instance.

* **Challenges & Solutions:**

  1. EC2 instance memory was insufficient, causing frequent crashes.

     * **Solution:** Use a high-memory instance. However, due to cost, this remained only as a proof of concept.
  2. Tasks were being killed due to automatic resource optimization.

     * **Solution:** Not yet resolved — still under study.

* **Demo Video:** https://youtu.be/ha2loaA-Qfk

---

### 🔸 3D Modeling (Blender / Unity)

* **Overview:**

  * Created 3D models using meshes, shape keys, and other techniques.
  * Experimented with implementation in Unity-based games.
* **Demo Video:** [In preparation]




# **個人開発プロジェクト**

### 🔸 StormworksPC（Lua / Stormworks Engine）

- 目的：趣味で、作られそうなので試しに実際作ってみた
- 概要：
  - ゲーム「Stormworks」内でOSを構築しました。
  - 各UI要素をモジュール化し、ロジックを実装した。
  - Stormworks内の独特なゲームエンジン使っているのでゲームの外は動作しません。
- Steamワークショップ：https://steamcommunity.com/sharedfiles/filedetails/?id=3484118636
- 実機デモ動画：https://youtu.be/XJbS73MIA1s
- ダイヤグラムとコート動画：https://youtu.be/BwLiGuqUqoo

- システム要素：
  - タスクバー：アプリを起動する場所。アプリアイコンをタップ➜アプリが開きます。長押しでタスクマネージャー。
  - 通知メニュー：タスクバーの右側、ボタンは時計も兼ねます。モジュール・チャット・バッテリーの通知一覧。
  - 通知ポップアップ：通知が来るときに通知メニューのボタンがアプリアイコンと「！」のマークでのお知らせします。
  - クイック設定：タスクバーの左側、ボタンはバッテリー表示も兼ねます。明るさ、音楽、画面上のキーボードのコントロールパネルです。
  - キーボード：画面上のキーボードもあります。
  - デスクトップ背景：内蔵の９種類から選べます。グラデーションモードでカラーコードを入力すれば自分の好みで設定できます。
  - アニメーション：目に優しいと滑らかなアニメーションがこだわったポイントです。
  - ウィンドーズエンジン：各アプリのウィンドーズのサイズが調整できます。サイズによって適したUIに変化します。
  - ウィンドーズスナップ：アプリの枠を選択している時、画面左右の「＜」「＞」ボタンで画面左／右半分にスナップするの仕組みになっています。
  - 全画面モード：ゴーグルを使ってゲームPCの画面を直接にモニター表示、全画面で体験できます。タッチ操作は無効になっているため、WASDで上下左右、スペースでクリックします。
  - コード最適化：ゲームのコードブロックは文字数制限があり、読めるコードと同時に文字数を省きを両立できるシステムデザインとなっています。
  - モジュール化：モジュール化によって他の機械にシステムを必要にモジュールだけをインストールしてサイズが省けられます。

- アプリ紹介：
  - 天気：温度・湿度・風速表示
  - マップ：衛星マップ、ナビ・検索・ズーム搭載
  - カメラ：無線/有線切替、ズーム、赤外線・方向コントロール対応
  - ノート：キーボードで入力、文字ごと色やフォーマトできます。最大９ページまで対応。
  - 設定：モジュール接続・システム情報、転載防止の、Steam QRコードとクレジット
  - エクステンション：外部プログラム対応、サードパーティーから機能追加できます。OSのAPIの対応すればシステムのハードもアクセスできます。
  - チャット：独自のゲーム内のチャットコミュニケーションプロトコルを開発しました。


### 🔸 MinecraftOnAWS（AWS / Linux）
- 概要：AWS学習の一環としてMinecraftサーバーをEC2上に構築しました。
- 課題と対策：
  1. EC2インスタンスのメモリーが足りなくって、よくクラッシュする。
      - 解決策：高メモリーのインスタンスを選ぶ。だたし、値段があげるため、概念実証だけにしました。
  2. リソース自動最適化によってタスクがキルされる。　
      - 解決策：未解決、まだ勉強している。

- デモ動画：https://youtu.be/ha2loaA-Qfk

### 🔸 3Dモデリング（Blender / Unity）
- 概要：
  - メッシュ、シェイプキーなどを用いて3Dモデルを作成。
  - Unityベースのゲームで実装を試行。
- デモ動画：【準備中】