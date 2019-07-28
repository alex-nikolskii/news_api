# import unittest
# from app import app
# from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
#

# В обоих случаях получаю ошибку с loop. Пожалуйста, расскажите, как ее исправить.
#
# class MyAppTestCase(AioHTTPTestCase):
#
#     async def get_application(self):
#         return app()
#
#     @unittest_run_loop
#     async def test_get_all_news(self):
#         resp = await self.client.request('GET', '/')
#         assert resp.status == 200
#         text = await resp.text()
#         assert '"news_count": 4' in text
#
#     @unittest_run_loop
#     async def test_get_first_id_news(self):
#         resp = await self.client.request('GET', '/news/1')
#         assert resp.status == 200
#         text = await resp.text()
#         assert '"title": "first"' in text


# if __name__ == '__main__':
#     unittest.main()


# with loop_context() as loop:
#     _app = app()
#     client = TestClient(TestServer(_app), loop=loop)
#     loop.run_until_complete(client.start_server())
#
#     async def test_get_all_news():
#         resp = await client.get('/')
#         assert resp.status == 200
#         text = await resp.text()
#         assert '"news_count": 4' in text
#
#     async def test_get_first_id_news():
#         resp = await client.get('/news/1')
#         assert resp.status == 200
#         text = await resp.text()
#         assert '"title": "first"' in text
#
#     loop.run_until_complete(test_get_all_news())
#     loop.run_until_complete(test_get_first_id_news())
#     loop.run_until_complete(client.close())
