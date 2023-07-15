import env
from dao.store_dao import get_store_ids


def get_urls():
    stores = get_store_ids()
    urls = []
    for store in stores:
        urls.append('http://127.0.0.1:' + env.POOL_RESTAURANTS_PORT + '/' + str(store[0]))
    return urls   