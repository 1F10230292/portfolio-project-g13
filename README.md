# project-g13-t4
# CS4-2024-class5-team5-project
チーム開発

リアルタイム投票アプリの作成

venv環境に入るためのコマンド
python -m venv venv
source venv/bin/activate

サイト閲覧時
python manage.py runserver

コード変更する前に必ず
git pull origin main
誰も作業していないかの確認をする

変更したら連絡をして
git add .
git commit -m '○○の追加'
git push origin main

編集して動かなかった場合
git add .
git commit -m ''
git reset --hard HEAD~1
これをすることで動かなかったコードをgitに保存しつつ追加したコードの削除を行ってくれる

create_poll => 投票作成ページ
poll_created => 作成され、リンクが発行されるページ
poll_detail => 過去に作った投票も表示される

残りのやること（必須）
・ログインしているユーザーによってホームページの投票履歴が変わるようにする
・投票作成に複数の入力場所、選択できるようにする。（できれば写真を入れられるようにする）
<!-- ・ヘッダーのリンク貼り付け -->
・作成した投票ページのリンクをふむと投票内容が出てくる。
・全体のデザイン、クリックしたときなどの色変化や動き

写真を追加するにあたって
pip install Pillow
インストールできたかの確認コマンド
pip show Pillow
Name: pillowがでたらOK！