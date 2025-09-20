# project-g13-t4
チーム開発


venv環境に入るためのコマンド
python -m venv venv
source venv/bin/activate

（ubuntuの場合）python3 -m venv venv　source venv/bin/activate


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



