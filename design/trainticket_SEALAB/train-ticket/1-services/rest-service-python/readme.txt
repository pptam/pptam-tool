
install:
pip install tornado


git:
https://github.com/tornadoweb/tornado



run:
docker run -d -p 16101:16101 --name web_tornado erkekin/tornado