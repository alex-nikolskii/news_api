from aiohttp.web import Application, run_app
from server_api import RestResource


app = Application()
news_resource = RestResource('news').register(app.router)

if __name__ == '__main__':
    run_app(app)

