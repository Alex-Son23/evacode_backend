Для запуска требуется выполнить команду:

`docker compose -f docker-compose.dev.yml up --build -d`

Если не сработало:

`docker ps -a`

`docker stop <id контейнеров которые используют порт 5432 через пробел>`
