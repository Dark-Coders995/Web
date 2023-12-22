from imports import *


def create_app():
    app_create = Flask(__name__)
    if os.getenv('ENV', "development") == "production":
        raise Exception("Currently no production config is setup.")
    else:
        print("Staring Local Development")
        app_create.config.update(
            CELERY_BROKER_URL='redis://localhost:6379',
            CELERY_RESULT_BACKEND='redis://localhost:6379'
        )
        celery_app = make_celery(app_create)
        app_create.config.from_object(LocalDevelopmentConfig)
        CORS(app_create, resources={r"/api/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE"]}})
    db.init_app(app_create)
    api_create = Api(app_create)
    api_create.init_app(app_create)
    JWTManager(app_create)
    security.init_app(app_create, user_datastore)
    cache.init_app(app_create)
    app_create.app_context().push()
    return app_create, api_create, celery_app


app, api, celery = create_app()








##______________________________________CELERY TASKS----ALL TASKS OF CELERY____________________________________________##

           ######_______________________EXPORT CSV TASK - USER TRIGGERED_______________________######
@celery.task()
def add_together(a, b):
    time.sleep(5)
    return a + b

@celery.task
def generate_csv_file(category_id):
    import csv
    import os
    import time

    #time.sleep(6)
    category = Category.query.get(category_id)
    if not category:
        return None

    products_data = []
    for product in category.products:
        total_product_bought = db.session.query(func.sum(Cart.quantity)).filter(Cart.product_id == product.id).scalar()
        total_cost = db.session.query(func.sum(Cart.total)).filter(Cart.product_id == product.id).scalar()
        products_data.append([
            product.name,
            total_product_bought or 0,
            total_cost or 0
        ])

    with open("static/details.csv", 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Product Name', 'Number of Products Sold', 'Total Cost'])
        for product_data in products_data:
            writer.writerow(product_data)

    return "Export Job Started.."



class Trigger(Resource):
    def get(self, category_id):
        a=generate_csv_file.delay(category_id)
        return {
            "Task_ID": a.id,
            "Task_State": a.state,
            "Task_Result": a.result  
        }
        
class Download(Resource):
    def get(self):
        return send_file('static/details.csv', as_attachment=True)
               



         ###__________________________CELERY TASK SCHEDULAR - DAILY REMINDER______________________________###


URL = "https://chat.googleapis.com/v1/spaces/AAAAqavgIj0/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=keu9Kc39kJ0mY45y0DjSUCXgy_aRCYp9cGnDlnzaba4"

@celery.on_after_finalize.connect
def daily_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=20, minute=47), SendDailyReminder.s(), name = "Daily Evening")
    sender.add_periodic_task(crontab(hour=20, minute=55), send_Daily_mail.s(), name = "Daily Evening")
    sender.add_periodic_task(crontab(hour=16, minute=39, day_of_month=2), SendMonthlyReport.s(), name = "2nd of every month")
    sender.add_periodic_task(30 , add_together.s(1,2), name = "Add Together")


@celery.task()
def add_together(a, b):
    time.sleep(5)
    return a + b


@celery.task
def send_Daily_mail():
    send_email(
        to_address="dummy@gmail.com",
        subject="Not Buying Today",
        message="Please buy today ",

    )
    return "Email should aarive in inbox shortly"

@celery.task
def SendDailyReminder():
    """
    Google
    Chat
    incoming
    webhook
    quickstart.
    """
    url = URL
    app_message = {
        'text': 'Reminder to Login to Grocery Store'}
    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}
    http_obj = Http()
    response = http_obj.request(
        uri=url,
        method='POST',
        headers=message_headers,
        body=dumps(app_message),
    )
    print(response)
    return "Reminder will send soon"


      ###_______________________CELERY TASK SCHEDULAR - MONTHLY Buy REPORT______________________###



SMTP_SERVER_HOST = "localhost"
SMTP_SERVER_PORT = 1025
SENDER_ADDRESS = "support@mygrocery.com"
SENDER_PASSWORD = ""

def send_email(to_address, subject, message):
    msg = MIMEMultipart()
    msg["From"] = SENDER_ADDRESS
    msg["To"] = to_address
    msg["Subject"] = subject

    msg.attach(MIMEText(message, "html"))

    s = smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()

def format_message(template_file, data={}, bookings=[]):

    months = ["Jan", "Feb", "March", "Apr", "May", "jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    currentMonth = datetime.now().month - 1
    currentYear = datetime.now().year
    lastmonth = months[currentMonth - 1]+ "-" + str(currentYear)

    with open(template_file) as file_:
        template = Template(file_.read())
        return template.render(data=data, bookings=bookings)

def get_user_bookings(user_id):

    today = datetime.utcnow()
    currentmonth= today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    bookings = Cart.query \
        .join(Product) \
        .filter(Cart.user_id == user_id, Cart.quantity > 0 ) \
        .all()


    user_bookings = []
    for booking in bookings:
        category_name = booking.Product.Category.name
        product_name = booking.Product.name
        cost = booking.quantity * booking.Product.price

        booking_info = {
            'category_name': category_name,
            'product_name': product_name,
            'cost': cost,
        }
        user_bookings.append(booking_info)

    return user_bookings

def send_monthly_report_email(data, lastmonth):
    user_id = data.id  
    bookings = get_user_bookings(user_id, lastmonth)


    message = format_message("monthly_report.html", lastmonth=lastmonth, data=data, bookings=bookings)
    send_email(data.email, subject="Monthly Report", message=message)


@celery.task()
def SendMonthlyReport():
    print("Starting SendMonthlyReport Task")

    users = db.session.query(User).filter_by(is_admin=False).all()

    today = datetime.utcnow()
    first_day_of_current_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
    first_day_of_previous_month = last_day_of_previous_month.replace(day=1)

    last_month = first_day_of_previous_month

    for user in users:
        send_monthly_report_email(data=user, lastmonth=last_month)


#-------------------------------------------------------------------------------------------------------------------------



api.add_resource(LoginAPI, '/api/login')
api.add_resource(SignupAPI, '/api/signup')
api.add_resource(AdminSignupAPI, '/api/adminsignup')
api.add_resource(AdminLoginAPI, '/api/admin/login')
api.add_resource(AdminAddCategoryAPI, '/api/admin/category')
api.add_resource(AdminGetCategoryAPI, '/api/admin/category')
api.add_resource(AdminEditCategoryAPI, '/api/admin/category/<int:category_id>')
api.add_resource(AdminAddProductAPI, '/api/admin/product/<int:category_id>')
api.add_resource(AdminGetProductAPI, '/api/admin/product/<int:category_id>')
api.add_resource(AdminEditProductAPI, '/api/admin/product/<int:category_id>/<int:product_id>')

api.add_resource(AdminDeleteCategoryAPI, '/api/admin/category/<int:category_id>')
api.add_resource(AdminDeleteProductAPI, '/api/admin/product/<int:category_id>/<int:product_id>')

api.add_resource(PostedCategoriesAPI, '/api/user/categories')
api.add_resource(PostedProductsAPI, '/api/user/category/<int:category_id>/products')

api.add_resource(CategoryDetailAPI, '/api/buy/category/<int:category_id>')
api.add_resource(ProductDetailAPI, '/api/buy/category/<int:category_id>/product/<int:product_id>')
api.add_resource(BuyDashAPI, '/api/user/cart')
api.add_resource(GetProductAPI, '/api/buy/product/<int:product_id>')
api.add_resource(BuyProductAPI, '/api/user/category/<int:category_id>/product/<int:product_id>/buy')
api.add_resource(SearchCategoryAPI, '/api/user/category/search')
api.add_resource(SearchProductAPI, '/api/user/product/search')



api.add_resource(Trigger, '/api/trigger/<int:category_id>')
api.add_resource(Download, '/api/download')
api.add_resource(SummaryAPI, '/api/admin/summary')

if __name__ == '__main__':
    app.run(debug=True)
