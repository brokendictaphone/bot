# создание экземпляра бота
from aiogram import Bot
from configure import config
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage #хранилище для данных в оперативной памяти
storage = MemoryStorage()# экземпляр хранилища

bot = Bot(token = config)# экземпляр бота
dp = Dispatcher(bot, storage = storage)# экземпляр диспетчера