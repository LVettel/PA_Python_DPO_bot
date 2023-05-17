from aiogram import executor, types
from create_bot import dp
from project import main_handlers, lowprice_highprice, search

main_handlers.register_handlers_main(dp)
lowprice_highprice.register_handlers_lowprice(dp)



if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=False)
	print('бот начал работать ')
