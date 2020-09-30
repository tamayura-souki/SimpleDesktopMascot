# SimpleDesktopMascot
imageフォルダ内の画像を表示するだけのソフト。
画面端に置いて、作業のお供にどうぞ。

## 使い方
image フォルダ内に画像をぶちこんで起動するだけ。

左クリックで表示されるメニューから終了できます。

config.json
- "app_name"
  - タスクマネージャ等で表示される名前を変えられます。
- "image_folder"
  - 表示したい画像の入ったフォルダを指定してください。
  - .png と .jpg ファイルのみ読み込めます。
- "image_change_interval"
  - 画像がランダムで切り替わる時間を秒(s)単位で入力してください。

# requirements
- PySide2 (https://pypi.org/project/PySide2/)

# LICENSE
MIT

(ソースコードのみに適応されます。配布ソフト内の画像データ等にはライセンスは付与されません)