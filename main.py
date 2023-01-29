from datetime import datetime,timedelta,date
import telebot
import firebase_admin
from firebase_admin import credentials,db,firestore
import asyncio
from flask import Flask,request
cred = firebase_admin.credentials.Certificate("niyuktibot-firebase-adminsdk-hhm5t-7465ecf440.json")
default_app = firebase_admin.initialize_app(cred, {
	'databaseURL': "https://niyuktibot-default-rtdb.asia-southeast1.firebasedatabase.app/"
	})
firestore_client = firebase_admin.firestore.client()
ref_for_material_table = firebase_admin.db.reference("/Material database")
ref_for_user_table = firebase_admin.db.reference("/User")
ref_for_orders_table = firebase_admin.db.reference("/Orders")
API_TOKEN = "5884244973:AAFuFD8QCOhInWHnViHWHWmRpa9nfA7vLPg"
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)
@app.route('/')
@bot.message_handler(commands=['start', 'Start','help','I want to place an order'])
def Send_Welcome(message):
    global msg,chat_id,ref_for_reminder_individual,user_id,user_info,bot_graph
    chat_id = message.chat.id
    user_info_including_key = ref_for_user_table.get()
    for key in user_info_including_key:

        user_info = user_info_including_key[key]
        print(user_info['chatId'])
        if user_info['chatId']==chat_id:
            msg = bot.reply_to(message,'Hi ' + user_info['DisplayName']+ '\n\nWhat would like to place :'+ "  \n\n1. /Custom  \n\n2. /Tshirt \n\n3. /Shorts   \n\n4./Status \n\n5./Help \n\n6./Exit")
            break
    else:
        msg = bot.reply_to(message, 'Hello, Welcome to the Bot.\n\n Pls Enter a Username: ')
        bot.register_next_step_handler(msg, Register_User)
def Register_User(message):
    value = message.text
    user_information = {'chatId':chat_id,'DisplayName':value}
    ref_for_user_table.push(user_information)
    bot.send_message(chat_id, 'Registered user succesfully \n /Exit')
    bot.register_next_step_handler(msg, Send_Welcome)
@bot.message_handler(commands=['Exit'])
def Exit(message):
   msg = bot.reply_to(message, 'Well then, Good Bye.')
   bot.register_next_step_handler(msg, Send_Welcome)
@bot.message_handler(commands=['Custom'])
def Run_asyncio_func(message):
    asyncio.run(CustomOrder(message))
async def CustomOrder(message):
    global orderdetails

    orderdetails = {'Item':'Custom Tshirt','chatId':message.chat.id,'Date':str( date.today())}
    bot.reply_to(message,"price:500")
    print(message.chat.id)
    """await bot.send_photo("C:/Apps/SampleTshirt.jpg")"""
    msg = bot.reply_to(message, "Mention color")
    bot.register_next_step_handler(msg, Color)
def Color(message):
    color_text = message.text
    if('black' in color_text or 'Black' in color_text ):
        color = 'Black'

    elif ('red' in color_text or 'Red' in color_text  ):
        color = 'Red'

    elif ('yellow' in color_text or 'Yellow' in color_text):
        color = 'Yellow'

    elif ('blue' in color_text or 'Blue' in color_text):
        color = 'Blue'

    elif ('pink' in color_text or 'Pink' in color_text ):
        color = 'Pink'

    else:
        color = 'Black'

    orderdetails['Color']=color

    msg = bot.reply_to(message,"Mention size(S,M,L) Tshirts ")
    bot.register_next_step_handler(msg, Size)
@bot.message_handler(commands=['I want to order a black Tshirt','I want to order a yellow Tshirt','I want to order a red Tshirt','I want to order a pink Tshirt','I want to order a blue Tshirt','Tshirt'])
def orderTshirt(message):
    global orderdetails
    orderdetails = {'Item':'Tshirt','chatId':message.chat.id,'Date':str( date.today())}
    bot.reply_to(message,"price:300")
    msg = bot.reply_to(message, "Mention color ")
    bot.register_next_step_handler(msg, Color)
def Size(message):
    Size_input = message.text
    if ('s' not in Size_input and 'm' not in Size_input and 'l' not in Size_input):
        msg = bot.reply_to(message, "You entered wrong size.Try again")
        bot.register_next_step_handler(msg, Send_Welcome)
    else:
        orderdetails['Size']=Size_input
        msg = bot.reply_to(message, "Mention quantity ")
        bot.register_next_step_handler(msg,Quantity)
def Quantity(message):
    Quantity_input = message.text
    if (Quantity_input.isalpha()):
        msg = bot.reply_to(message, "You entered wrong Quantity.Try again ")
        bot.register_next_step_handler(msg, Send_Welcome)
    else:
        orderdetails['Quantity'] = Quantity_input
        msg = bot.reply_to(message, "Please tell mode of Payment(Card/Paytm/upi/google pay/COD)??")
        bot.register_next_step_handler(msg, Payment)
    """data = ref_for_material_table.get()"""
    """ Quantity = int(Quantity_input)
    elif(data['Custom Tshirt'] >= Quantity): """


def Payment(message):
    payment_input = message.text
    if('card' in payment_input):
        orderdetails['Payment Method']='Card'
        ref_for_orders_table.push(orderdetails)
        msg = bot.reply_to(message, "\U0001F929 \U0001F973 Order Placed \U0001F929 \U0001F973 \n /Exit")
        bot.register_next_step_handler(msg, Send_Welcome)
    elif ('upi' in payment_input or 'paytm' in payment_input or 'google pay' in payment_input):
        orderdetails['Payment Method'] = 'Payment App'
        ref_for_orders_table.push(orderdetails)
        msg = bot.reply_to(message, "\U0001F929 \U0001F973 Order Placed \U0001F929 \U0001F973 \n /Exit")
        bot.register_next_step_handler(msg, Send_Welcome)
    elif ('cash on delivery' in payment_input or'cod' in payment_input):
        orderdetails['Payment Method'] = 'COD'
        ref_for_orders_table.push(orderdetails)
        msg = bot.reply_to(message, "\U0001F929 \U0001F973 Order Placed \U0001F929 \U0001F973 \n /Exit")
        bot.register_next_step_handler(msg, Send_Welcome)
    else:
        msg = bot.reply_to(message, "Wrong payment method\n Try again!!!!")
        bot.register_next_step_handler(msg, Send_Welcome)


@bot.message_handler(commands=['Shorts'])
def order_Shorts(message):
    global orderdetails
    msg = bot.reply_to(message,"price:300")
    orderdetails = {'Item': 'Shorts','chatId':message.chat.id, 'Date':str(date.today())}
    msg = bot.reply_to(message, "Mention color ")
    bot.register_next_step_handler(msg, Color)

@bot.message_handler(commands=['Status'])
def view_order(message):
    global keydict,order_informations
    order_informations = ref_for_orders_table.get()
    integer =0
    keydict={}
    for key in order_informations:
        integer = integer+1
        keydict[integer]= key
        order_information = order_informations[key]
        print(order_information)
        if order_information["chatId"]==message.chat.id:
            order_information = str(order_information)
            order_information =order_information.replace('{','')
            order_information = order_information.replace('}', '')
            order_information = order_information.replace("'", "")
            msg = bot.reply_to(message,"/"+str(integer)+" " +order_information)
    msg = bot.reply_to(message,'Choose the order whose status you wish to see')
    bot.reply_to(message,'/Exit')
    bot.register_next_step_handler(msg,status)
def status(message):
    order_code = message.text
    order_code = int(order_code.replace('/',''))
    key = keydict[order_code]

    order_date = datetime(int(order_informations[key]['Date'][0:4]),int(order_informations[key]['Date'][5:7]),int(order_informations[key]['Date'][8:]),23,59,59)

    if (datetime.now()>=order_date):
        print('hello')
        msg = bot.reply_to(message,"Order shall be delivered in 2 days")
        bot.register_next_step_handler(msg, Send_Welcome)
    elif (datetime.now()>=(order_date+timedelta(days=2))):
        print('hi')
        msg = bot.reply_to(message,"Order is delivered or it shall come today")
        bot.register_next_step_handler(msg, Send_Welcome)
    elif (datetime.now()>=(order_date+timedelta(days=1))):
        print('hola')
        msg = bot.reply_to(message,"Order shall be delivered within a day")
        bot.register_next_step_handler(msg, Send_Welcome)
    else:
        msg = bot.reply_to(message, "Order shall be delivered in 2 days")
        bot.register_next_step_handler(msg, Send_Welcome)

@bot.message_handler(commands=['Help','help','Inquiry','Enquiry'])
def Enquiry(message):
    msg = bot.reply_to(message, "What query do you have??")
    bot.register_next_step_handler(msg,Answer)
def Answer(message):
    Query = message.text
    if 'delivery' in Query:
        msg = bot.reply_to(message, "We deliver in 2 days.You can even check delivery status")
    elif 'Fabric' in Query or 'Quality' in Query:
        msg = bot.reply_to(message,"All clothes are made from 100% pure cotton.")
    elif 'Cost' in Query or 'Price' in Query:
        msg = bot.reply_to(message,"We have clothes starting from 500 rupees to 1000 rupees")
    elif 'Return'in Query or 'Replacement' in Query:
        msg = bot.reply_to(message, "We have 15 days of replacement policy.")
    elif 'Transaction failure'in Query or 'money debited from my bank account' in Query:
        msg = bot.reply_to(message, "sometime We have some transaction failure.Don't worry.Your money will be credited to your account in 4-5 working daysBut you need to place the order again.")
    elif 'sizes'in Query or 'Size' in Query:
        msg = bot.reply_to(message,'We are available in Small,Medium and Large.Small-32.Medium-38.Large-42')
    elif 'colors'in Query or 'Colour' in Query:
        msg = bot.reply_to(message,'All products are available in Black,Blue,pink,red,yellow')
    else:
        msg = bot.reply_to("I am learning right now.")
    bot.register_next_step_handler(msg, Send_Welcome)
bot.polling()
if __name__ == '__main__':
    app.run(debug=True)
