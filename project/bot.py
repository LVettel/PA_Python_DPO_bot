from aiogram import executor
from create_bot import dp
from project import main_handlers, lowprice_highprice_bestdeal
from loguru import logger

main_handlers.register_handlers_main(dp)
lowprice_highprice_bestdeal.register_handlers_lowprice(dp)

if __name__ == '__main__':
    logger.info('бот начал работать')
    executor.start_polling(dp, skip_updates=False)
    logger.info('бот закончил работать ')
