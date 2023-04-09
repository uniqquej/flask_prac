FROM python:3.8

# root권한
# 패스워드를 입력하지 않아도 유저추가해줄거야 그리고 홈디렉토리도 자동생성할거야
RUN adduser --disabled-password python

# 위에서 생성해준 유저로 전환
USER python

# 의존성 패키지 복사
COPY ./requirements.txt /tmp/requirements.txt

# 의존성 패키지 설치
RUN pip install --user -r /tmp/requirements.txt
RUN pip install --user gunicorn==20.1.0

# 프로젝트 복사 & 오너설정
COPY --chown=python:python ./ /var/www/gogglekaap

#복사한 프로젝트 경로로 이동
WORKDIR /var/www/gogglekaap

# 설치한 패키지 명령어를 사용하기 위해 환경변수를 등록
ENV PATH="/home/python/.local/bin:${PATH}"

# 엔트리포인트 쉘 실행권한 추가
RUN chmod +x ./etc/docker-entrypoint.sh

#8080 포트 노출
EXPOSE 8080

# gunicorn 실행
# CMD gunicorn --bind :8080 --workers 2 --threads 8 'gogglekaap:create_app()'

