import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram_function import *

#Enable Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

import warnings
warnings.filterwarnings("ignore")

updater = Updater(token=os.environ['API_key'],use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler('start', start))

dp.add_handler(CommandHandler('track',track))

dp.add_handler(CommandHandler('stoptrack',stoptrack))
 
dp.add_handler(CommandHandler('get_csv', getcsv))

dp.add_handler(CommandHandler('get_qr', getQR))

dp.add_handler(CommandHandler('get_analytics', getAnalytics))

dp.add_handler(CommandHandler('view',view))

dp.add_handler(CommandHandler('adminlocal', admin_local_query))

dp.add_handler(MessageHandler(Filters.command, unknown))

if __name__ == '__main__':
    updater.start_polling()
    updater.idle()