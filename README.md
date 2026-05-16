## sample

# スーパーユーザー
docker compose run --rm backend python manage.py createsuperuser

# 使い方
一度 
docker compose down -v
で落としてから
再度
docker compose up --build
で再構築してから別ターミナルで
docker compose run --rm backend python manage.py createsuperuser
すると
localhost/8000/admin
で管理画面が見れるようになります。