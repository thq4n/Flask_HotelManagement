from mainapp import db
from mainapp import admin
from flask_admin.contrib.sqla import ModelView
from mainapp.models import RoomType,Room,Nationality,UserType,User,Status,Coefficient,BookRoom,Bill,UserRoom,BillDetail,Report,LoginUser
from flask_admin import BaseView,expose
from flask import redirect
from flask_login import logout_user, current_user
from mainapp.utils import *
from datetime import date

class ReportView(BaseView):
    @expose('/')  # de chi dan admin map vao day
    def index(self):
        report = Report.query.all()
        roomtype = RoomType.query.all()
        room = Room.query.all()

        labels = []
        values = []
        today = date.today()

        title = "Báo cáo doanh thu theo loại phòng tháng " + str(today.month) + "/" + str(today.year)
        for item in roomtype:
            labels.append(item)
            gt = 0
            for i in report:
                if i.month == today.month and i.year == today.year and i.room.roomtype_id == item.id:
                    gt += i.revenue
            values.append(gt)

        title2 = "Báo cáo mật độ sử dụng phòng tháng " + str(today.month) + "/" + str(today.year)
        labels2 = []
        values2 = []
        max = 0
        for item in room:
            labels2.append(item.name)
            gt = 0
            for i in report:
                if i.month == 1 and i.year == 2021 and i.room_id == item.id:
                    gt = i.used
                    max = i.end_month.day
            values2.append(gt)

        return self.render('admin/report.html', labels=labels, values=values, title=title, labels2=labels2,
                           values2=values2, title2=title2, max=max)

    def is_accessible(self):
        return current_user.is_authenticated

class Configuration(ModelView):
    can_delete = False
    def is_accessible(self):
        return (current_user.is_authenticated and (check_role(current_user.user_id,'Admin') or check_role(current_user.user_id,'Employee')))

class RoomTypeView(ModelView):
    column_display_pk = True
    can_delete = False
    form_excluded_columns = ['rooms','active']
    column_editable_list = ['active']
    def is_accessible(self):
        return (current_user.is_authenticated and check_role(current_user.user_id,'Admin'))

class NationalityView(ModelView):
    column_display_pk = True
    can_delete = False
    form_excluded_columns = ['users']

    def is_accessible(self):
        return (current_user.is_authenticated and check_role(current_user.user_id,'Admin'))


class UserTypeView(ModelView):
    column_display_pk = True
    can_delete = False
    form_excluded_columns = ['users','active']
    column_editable_list = ['active']
    def is_accessible(self):
        return (current_user.is_authenticated and check_role(current_user.user_id,'Admin'))


class StatusView(ModelView):
    form_excluded_columns = ['book_room']
    can_delete = False
    can_edit = False
    can_create = False
    column_display_pk = True
    def is_accessible(self):
        return (current_user.is_authenticated and check_role(current_user.user_id,'Admin'))

class CoefficientView(ModelView):
    form_excluded_columns = ['book_room','active']
    can_delete = False
    can_edit = False
    column_display_pk = True
    column_editable_list = ['active']
    def is_accessible(self):
        return (current_user.is_authenticated and check_role(current_user.user_id,'Admin'))

class BillView(ModelView):
    column_display_pk = True
    form_excluded_columns = ['bill_detail','total_price']
    def is_accessible(self):
        return (current_user.is_authenticated and (check_role(current_user.user_id,'Admin') or check_role(current_user.user_id,'Employee')))

class BillDetailView(ModelView):
    form_excluded_columns = ['bill_detail']
    def is_accessible(self):
        return (current_user.is_authenticated and (check_role(current_user.user_id,'Admin') or check_role(current_user.user_id,'Employee')))

class UserModelView(ModelView):
    form_excluded_columns = ['book_room','bill','login_user','user_room','active']
    page_size = 10
    can_delete = False
    column_searchable_list=['name','ic','phone','email']
    column_editable_list=['active','nationality','usertype']

    def is_accessible(self):
        return (current_user.is_authenticated and (check_role(current_user.user_id,'Admin') or check_role(current_user.user_id,'Employee')))


class UserRoomView(ModelView):
    page_size = 10
    can_create = False
    can_edit = False

    def is_accessible(self):
        return (current_user.is_authenticated and (check_role(current_user.user_id,'Admin') or check_role(current_user.user_id,'Employee')))

class RoomView(ModelView):
    page_size = 10
    can_delete = False
    column_searchable_list=['name']
    column_editable_list=['active']
    inline_models = [BookRoom]
    form_excluded_columns = ['report','active']

    def is_accessible(self):
        return (current_user.is_authenticated and (check_role(current_user.user_id,'Admin') or check_role(current_user.user_id,'Employee')))

class BookRoomView(ModelView):
    form_excluded_columns = ['bill_detail']
    inline_models = [UserRoom]
    column_editable_list = ['status']

    def is_accessible(self):
        return (current_user.is_authenticated and (check_role(current_user.user_id,'Admin') or check_role(current_user.user_id,'Employee')))

class ReportModelView(ModelView):
    form_excluded_columns = ['used','revenue']

    def is_accessible(self):
        return (current_user.is_authenticated and (check_role(current_user.user_id,'Admin') or check_role(current_user.user_id,'Employee')))

class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return (current_user.is_authenticated and (check_role(current_user.user_id,'Admin') or check_role(current_user.user_id,'Employee')))

class LoginUserView(ModelView):
    def is_accessible(self):
        return (current_user.is_authenticated and check_role(current_user.user_id,'Admin'))

admin.add_view(RoomTypeView(RoomType,db.session,category='Configuration'))
admin.add_view(NationalityView(Nationality,db.session,category='Configuration'))
admin.add_view(UserTypeView(UserType,db.session,category='Configuration'))
admin.add_view(StatusView(Status,db.session,category='Configuration'))
admin.add_view(CoefficientView(Coefficient,db.session,category='Configuration'))
admin.add_view(RoomView(Room,db.session))
admin.add_view(UserModelView(User,db.session,category='User'))
admin.add_view(BookRoomView(BookRoom,db.session))
admin.add_view(BillView(Bill,db.session,category='Bill'))
admin.add_view(BillDetailView(BillDetail,db.session,category='Bill'))
admin.add_view(UserRoomView(UserRoom,db.session))

admin.add_view(ReportModelView(Report,db.session))
admin.add_view(LoginUserView(LoginUser,db.session,category='User'))
admin.add_view(ReportView(name='Report Us'))
admin.add_view(LogoutView(name='Logout'))

#FOOD:
class MyView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated
admin.add_view(MyView(Category, db.session, category='FOOD'))
admin.add_view(MyView(Product, db.session, category='FOOD'))
admin.add_view(MyView(Receipt, db.session, category='FOOD'))
admin.add_view(MyView(ReceiptDetail, db.session, category='FOOD'))