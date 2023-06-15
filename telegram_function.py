from telegram import Update
from telegram.ext import CallbackContext

from telegram_msg import *
from db import *
import subprocess
import psutil

pro=0

def stop_process(pid):
    # Terminate the process based on its PID
    process = psutil.Process(pid)
    for child in process.children(recursive=True):
        child.kill()
    process.kill()

def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello")

def track(update: Update, context: CallbackContext):
    msg = update.message.text
    msg = msg.split(" ",1)

    env_admin = int(os.environ['admin'])
    user_id = update.message.chat_id
    
    if user_id == env_admin:

        if len(msg)== 2:
            try :
                command = ['python', 'functions.py', f'{msg[-1]}']
                p = subprocess.Popen(command)
                context.bot.send_message(chat_id=update.effective_chat.id, text="Tracking Started")
                global pro
                pro = p.pid
            except:
                context.bot.send_message(chat_id=update.effective_chat.id, text="Tracking Failure")

        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Use Proper Format")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="You dont have admin rights")


def getcsv(update: Update, context: CallbackContext):
    user_id = update.message.chat_id
    env_admin = int(os.environ['admin'])
    if user_id == env_admin:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Sending CSV")
            send_csv(user_id)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="You dont have admin rights")

def getQR(update: Update, context: CallbackContext):
    user_id = update.message.chat_id
    env_admin = int(os.environ['admin'])
    if user_id == env_admin:
            try:
                send_qr(user_id)
            except:
                 context.bot.send_message(chat_id=update.effective_chat.id, text="No QR found Start Tracking First")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="You dont have admin rights")

def getAnalytics(update: Update, context: CallbackContext):
    user_id = update.message.chat_id
    env_admin = int(os.environ['admin'])
    if user_id == env_admin:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Creating and Sending Analytics")
            send_analytics_report(user_id)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="You dont have admin rights")


def view(update: Update, context: CallbackContext):
    user_id = update.message.chat_id
    env_admin = int(os.environ['admin'])
    if user_id == env_admin:
            result = local_mysql_query("SELECT * FROM info")[-10:]
            context.bot.send_message(chat_id=update.effective_chat.id, text=result)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="You dont have admin rights")

def stoptrack(update: Update, context: CallbackContext):
    user_id = update.message.chat_id
    env_admin = int(os.environ['admin'])
    if user_id == env_admin:
            try:
                stop_process(pro)
                context.bot.send_message(chat_id=update.effective_chat.id, text="Tracking Stopped Sucessfully")
            except:
                context.bot.send_message(chat_id=update.effective_chat.id, text="Stopping Failed")
    else:   
        context.bot.send_message(chat_id=update.effective_chat.id, text="You dont have admin rights")



def admin_local_query(update: Update, context: CallbackContext):
    user_id = update.message.chat_id
    env_admin = int(os.environ['admin'])
    msg = update.message.text
    msg = msg.split(" ",1)
    if user_id == env_admin:
        if len(msg)==2:
            query_sent = msg[1]
            try:
                data_ret = local_mysql_query(query_sent)
                context.bot.send_message(chat_id=update.effective_chat.id, text=data_ret)
            except:        
                context.bot.send_message(chat_id=update.effective_chat.id, text="Error execution")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="No Query passed")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="You dont have admin rights")


def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")