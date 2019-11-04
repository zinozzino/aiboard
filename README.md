# aiboard
2019년 졸업작품


## wordpress 실행방법

1. Docker 설치

2. Docker 설정

```
$ docker swarm init
$ openssl rand -base64 20 | docker secret create db_password - 
$ docker stack deploy -c ./docker-compose.yml aiboard

$ # 서버가 http://CURRENT_IP:80 에 열립니다.

$ # 내리고 싶을 땐
$ docker stack rm aiboard
```