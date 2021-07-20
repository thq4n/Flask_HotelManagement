from mainapp.models import *
import hashlib

def read_roomtype():
    return RoomType.query.all()

def read_rooms():
    return Room.query.all()

def read_nationality():
    return Nationality.query.all()

def read_usertype():
    return UserType.query.all()

def read_users():
    return User.query.all()

def read_status():
    return Status.query.all()

def read_coefficient():
    return Coefficient.query.all()

def read_bookroom():
    return BookRoom.query.all()

def read_bills():
    return Bill.query.all()

def read_user_room():
    return UserRoom.query.all()

def read_billdetail():
    return BillDetail.query.all()

def get_user_info(user_id):
    info = User.query.filter(User.id == user_id).first()
    return info

def get_user_booking(user_id):
    bookings = BookRoom.query.filter(BookRoom.user_id==user_id)
    return bookings

def read_products():
    return Product.query.all()

def read_categories():
    return Category.query.all()

def read_receipts():
    return Receipt.query.all()

def read_receiptdetails():
    return ReceiptDetail.query.all()

def check_active(user_id):
    user = User.query.filter(User.id == user_id).first()
    if (user.active == 1):
        return 1
    return 0

def create_user(info, login):

    existed = LoginUser.query.all()
    for u in existed:
        print(u.id)
    new_user = User(
        name = info['name'],
        sex=info['gender'],
        ic=info['idcard'],
        phone=info['phone'],
        email=info['email'],
        address=info['address'],
        nationality_id=info['nation'],
        usertype_id=info['user_type'],
        active=0
    )
    db.session.add(new_user)
    username = login['username']
    password = login['password']
    hash_password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
    for u in existed:
        if (username == u.username):
            return {'message':0}
    new_account = LoginUser(username=username, password=hash_password, user=new_user)
    db.session.add(new_account)
    db.session.commit()
    return {'message':1}

def active_user(user_email):
    user = User.query.filter(User.email==user_email).first()
    user.active = 1
    db.session.commit()

def edit_user_info(id, info):
    user = User.query.filter(User.id==id).first()
    user.name = info['name']
    user.sex = info['gender']
    user.ic = info['idcard']
    user.phone = info['phone']
    user.email = info['email']
    user.address = info['address']
    user.nationality_id = info['nation']
    db.session.commit()

def edit_user_password(id, login):
    oldpass = login['oldpass']
    newpass = login['newpass']
    hash_old = str(hashlib.md5(str(oldpass).strip().encode("utf-8")).hexdigest())
    hash_new = str(hashlib.md5(str(newpass).strip().encode("utf-8")).hexdigest())
    oldlogin = LoginUser.query.filter(LoginUser.user_id==id).first()
    if hash_old == oldlogin.password:
        oldlogin.password = hash_new
        db.session.commit()

def check_user_name(username):
    accounts = LoginUser.query.all()
    for acc in accounts:
        if acc.username == username:
            return 1
    return 0


def check_id_card(idcard):
    users = User.query.all()
    for u in users:
        if u.ic == idcard:
            return 1
    return 0

def check_email(email):
    users = User.query.all()
    for u in users:
        if u.email == email:
            return 1
    return 0

def check_role(id, role):
    roles = UserType.query.all()
    for r in roles:
        if str(role) == r.name:
            role_id = r.id
    if role_id is None:
        return 0
    user = User.query.filter(User.id == id).first()
    if user.usertype_id == role_id:
        return 1
    return 0

def find_room_available(datein, dateout):
    available = []
    bookings = BookRoom.query.all()
    rooms = Room.query.all()
    for r in rooms:
        check = 0
        for b in bookings:
            if (r.id == b.room_id):
                if ((((b.check_in >= datein and b.check_in <= dateout) or (b.check_out >= datein and b.check_out <= dateout))
                     and
                     (b.status_id != 5 and b.status_id != 3)) or (r.active == 0)):
                    check = 1
                    break
        if check == 0:
            available.append(r.id)
    return available

def do_book_room(room_id, user_id, datein, dateout):
    checkin = datetime.strptime(datein, "%Y-%m-%d").date()
    checkout = datetime.strptime(dateout, "%Y-%m-%d").date()
    if int(room_id) not in find_room_available(checkin,checkout):
        return 0;

    coefficients = Coefficient.query.all()
    coefficients.reverse()
    booking = BookRoom(user_id=int(user_id), check_in=checkin, check_out=checkout,room_id=int(room_id),status_id=1,coefficient_id=coefficients[0].id)
    db.session.add(booking)
    db.session.commit()
    return 1

def cancle_booking(booking_id):
    booking = BookRoom.query.filter(BookRoom.id == booking_id).first()
    if(booking.status_id == 1):
        booking.status_id = 3
        db.session.commit()
        return 1
    return 0

#FOOD:
def cart_stats(cart):
    count, price = 0, 0
    if cart:
        for p in cart.values():
            count = count + p["quantity"]
            price = price + p["quantity"] * p["price"]
    return count, price

def add_receipt(user_id, cart):
    receipt = Receipt(customer_id=user_id)
    db.session.add(receipt)

    for p in list(cart.values()):
        detail = ReceiptDetail(product_id=p["id"],
                               quantity=p["quantity"],
                               price = p["price"],
                               receipt=receipt)
        db.session.add(detail)
    db.session.commit()

def cal_bill_amount(bill_id):
    amount = 0
    detail = ReceiptDetail.query.filter(ReceiptDetail.receipt_id==bill_id)
    for d in detail:
        amount = amount + (d.price * d.quantity)
    return amount

