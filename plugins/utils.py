
import time as tm
from database import Db, db
from .test import parse_buttons

STATUS = {}


class STS:
    def __init__(self, id):
        self.id = id
        self.data = STATUS

    def verify(self):
        return self.data.get(self.id)

    def store(self, From, to,  skip, limit):
        self.data[self.id] = {"FROM": From, 'TO': to, 'total_files': 0, 'skip': skip, 'limit': limit,
                      'fetched': skip, 'filtered': 0, 'deleted': 0, 'duplicate': 0, 'total': limit, 'start': 0}
        self.get(full=True)
        return STS(self.id)

    def get(self, value=None, full=False):
        values = self.data.get(self.id)
        if not full:
           return values.get(value)
        for k, v in values.items():
            setattr(self, k, v)
        return self

    def add(self, key=None, value=1, time=False, start_time=None):
        if time:
          return self.data[self.id].update({'start': tm.time() if start_time is None else start_time})
        self.data[self.id].update({key: self.get(key) + value}) 

    def divide(self, no, by):
       by = 1 if int(by) == 0 else by 
       return int(no) / by 

    async def get_data(self, user_id):
        bot = await db.get_bot(user_id)
        if bot is None:
            bot = await db.get_userbot(user_id)
        k, filters = self, await db.get_filters(user_id)
        size, configs = None, await db.get_configs(user_id)
        if configs['duplicate']:
           duplicate = True
        else:
           duplicate = False
        try:
           min = configs['min_size']
           max = configs['max_size']
        except:
           min = 0
           max = 0
        button = parse_buttons(configs['button'] if configs['button'] else '')
        return bot, configs['caption'], configs['forward_tag'], {'filters': filters,
                'keywords': configs['keywords'], 'min_size': min, 'max_size': max, 'extensions': configs['extension'], 'skip_duplicate': duplicate, 'db_uri': configs['db_uri']}, configs['protect'], button

