from flask import Flask, render_template, url_for, redirect, request, make_response, flash
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import enum
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.secret_key = "bardzo trudny string do zlamania"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
db.create_all()
db.session.commit()


def create_app():
    app = Flask(__name__)
    db.init_app(app)
    app.secret_key = "bardzo trudny string do zlamania"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    return app




app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'


class Maseczki(db.Model):
    __tablename__ = "maseczki"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    image = db.Column(db.String(50), nullable=False, unique=False)
    color = db.Column(db.String(20), nullable=False, unique=False)
    size = db.Column(db.String(3), nullable=False, unique=False)
    sex = db.Column(db.String(10), nullable=False, unique=False)
    price = db.Column(db.Integer, nullable=False, unique=False)
    promotion = db.Column(db.Integer, nullable=True, unique=False)
    realprice = db.Column(db.Integer, nullable=False, unique=False)

    def __repr__(self):
        return f"id = {self.id}\n name = {self.name}\n image = {self.image}\n color = {self.color},\n size = {self.size}\n sex = {self.sex}\n price = {self.price}\n price = {self.promotion}\n price = {self.realprice}\n"

    @classmethod
    def db_to_dictionary(cls):
        how_many_id = cls.query.all()
        slownik = {"maseczki": []}
        for id in how_many_id:
            slownik["maseczki"].append(
                {"id": id.id, "name": id.name, "image": id.image, "color": id.color, "size": id.size, "sex": id.sex,
                 "price": id.price, "promotion": id.promotion, "realprice": id.realprice})
        return slownik

    def save_in_db(self):
        db.session.add(self)
        db.session.commit()

    def del_in_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_in_db_by_id(cls, id):
        return cls.query.filter_by(id=id).first()


class Sex(enum.Enum):
    mężczyzna = "MEN"
    kobieta = "WOMAN"
    inna = "UNKNOWN"


class Province(enum.Enum):
    kujawskopomorskie = "Kujawsko-Pomorskie"
    mazowieckie = "Mazowieckie"
    wielkopolskie = "Wikelkopolskie"
    malopolskie = "Małopolskie"
    podkarpackie = "Podkarpackie"
    podlaskie = "Podlaskie"
    slaskie = "Śląskie"
    dolnoslaskie = "Dolno Śląskie"
    pomorskie = "Pomorskie"
    swietokrzyskie = "Świętokrzyskie"
    warminskomazurskie = "Warmińsko-Mazurskie"
    zachodniopomorskie = "Zachodnio Pomorksie"
    lubelskie = "Lubelskie"
    lubuskie = "Lubuskie"
    lodzkie = "Łódzkie"
    opolskie = "Opolskie"


# utworzyć na nowo baze z User
# dodac do bazy zmiana html
# logowanie sprawdzenie
# plus edycja Usera

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(14), unique=True, nullable=False)
    name = db.Column(db.String(20), unique=False, nullable=False)
    surename = db.Column(db.String(20), unique=False, nullable=False)
    mail = db.Column(db.String(35), nullable=False, unique=True)
    password = db.Column(db.String(24), nullable=False, unique=False)
    sex = db.Column(db.Enum(Sex), unique=False, nullable=False)
    birthday = db.Column(db.Integer, unique=False, nullable=False)
    birthmonth = db.Column(db.Integer, unique=False, nullable=False)
    birthyear = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return f"id = {self.id}\n name = {self.name}\n surname = {self.surename}\n mail = {self.mail}\n password = {self.password}\n birthday = {self.birthday}\n birthmonth = {self.birthmonth}\n birthyear = {self.birthyear}\n sex = {self.sex}\n nickname = {self.nickname}"

    @classmethod
    def db_to_dictionary(cls):
        how_many_id = cls.query.all()
        slownik = {"users": []}
        for id in how_many_id:
            slownik["users"].append(
                {"id": id.id, "name": id.name, "surename": id.surename, "mail": id.mail, "password": id.password,
                 "birthday": id.birthday, "birthmonth": id.birthmonth, "birthyear": id.birthyear, "sex": id.sex, "nickname": id.nickname})
        return slownik

    @classmethod
    def get_info(cls, mail):
        user = cls.query.filter_by(mail=mail).first()
        Dictionary = {"id": user.id, "name": user.name, "surename": user.surename, "mail": user.mail, "password": user.password,
                 "birthday": user.birthday, "birthmonth": user.birthmonth, "birthyear": user.birthyear, "sex": user.sex, "nickname": user.nickname}
        return Dictionary

    def save_in_db(self):
        db.session.add(self)
        db.session.commit()

    def del_in_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_in_db_by_id(cls, id):
        return cls.query.filter_by(id=id).first()


class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.String(30), unique=True, nullable=False)
    header = db.Column(db.String(38), unique=False, nullable=False)
    text = db.Column(db.String(587), unique=False, nullable=False)
    templatesnumber = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return f"id = {self.id}\n img = {self.img}\n header = {self.header}\n text = {self.text}\n templatesnumber = {self.templatesnumber}"

    @classmethod
    def db_to_dictionary(cls):
        how_many_id = cls.query.all()
        slownik = {"posts": []}
        for id in how_many_id:
            slownik["posts"].append(
                {"id": id.id, "img": id.img, "header": id.header, "text": id.text,
                 "templatesnumber": id.templatesnumber})
        return slownik

    def save_in_db(self):
        db.session.add(self)
        db.session.commit()

    def del_in_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_in_db_by_id(cls, id):
        return cls.query.filter_by(id=id).first()


class PostAdvanced(db.Model):
    __tablename__ = "postadvanced"
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.String(30), unique=False, nullable=True)
    img2 = db.Column(db.String(30), unique=False, nullable=True)
    text = db.Column(db.String(587), unique=False, nullable=True)
    text2 = db.Column(db.String(587), unique=False, nullable=True)
    post = db.relationship('Post')
    postid = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    template = db.relationship('Template')
    templateid = db.Column(db.Integer, db.ForeignKey('template.id'), nullable=False)

    def __repr__(self):
        return f" id = {self.id}\n postid = {self.postid}\n img = {self.img}\n img2 = {self.img2}\n text = {self.text}\n text2 = {self.text2}"

    @classmethod
    def db_to_dictionary(cls):
        how_many_id = cls.query.all()
        slownik = {"posts": []}
        for id in how_many_id:
            slownik["posts"].append(
                {"id": id.id, "postid": id.postid, "img": id.img, "img2": id.img2, "text": id.text, "text2": id.text2,
                 "template": id.template})
        return slownik

    def save_in_db(self):
        db.session.add(self)
        db.session.commit()

    def del_in_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_in_db_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_in_db_by_postid(cls, postid):
        return cls.query.filter_by(postid=postid)


class Template(db.Model):
    __tablename__ = "template"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)

    def __repr__(self):
        return f"id = {self.id}\n name = {self.name}"

    @classmethod
    def db_to_dictionary(cls):
        how_many_id = cls.query.all()
        slownik = {"posts": []}
        for id in how_many_id:
            slownik["posts"].append(
                {"id": id.id, "name": id.name})
        return slownik

    def save_in_db(self):
        db.session.add(self)
        db.session.commit()

    def del_in_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_in_db_by_id(cls, id):
        return cls.query.filter_by(id=id).first()


class Adress(db.Model):
    __tablename__ = "adress"
    id = db.Column(db.Integer, primary_key=True)
    Province = db.Column(db.Enum(Province), unique=False, nullable=False) #enum
    postalcode = db.Column(db.String(5), unique=False, nullable=False)
    township = db.Column(db.String(20), unique=False, nullable=False)
    street = db.Column(db.String(35), nullable=False, unique=False)
    streetnumber = db.Column(db.String(24), nullable=False, unique=False)
    flatnumber = db.Column(db.String(10), unique=False, nullable=False)
    user = db.relationship('User')
    userid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"id = {self.id}\n Privince = {self.Province}\n postalcode = {self.postalcode}\n township = {self.township}\n street = {self.street}\n streeetnumber = {self.streetnumber}\n flatnumber = {self.flatnumber}\n user = {self.user}"

    @classmethod
    def db_to_dictionary(cls):
        how_many_id = cls.query.all()
        slownik = {"users" : []}
        for id in how_many_id:
            slownik["users"].append({"id": id.id, "province": id.Province, "postalcode": id.postalcode, "township": id.township, "street": id.street, "streetnumber": id.strretnumber, "flatnuber": id.flatnumber, "user": id.user})
        return slownik

    def save_in_db(self):
        db.session.add(self)
        db.session.commit()

    def del_in_db(self):
        db.session.delete(self)
        db.session.commit()


    @classmethod
    def find_in_db_by_id(cls, id):
        return cls.query.filter_by(id = id).first()

app = create_app()
db.create_all(app=app)
admin = Admin(app, name='posts', template_mode='bootstrap4')


admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Maseczki, db.session))
admin.add_view(ModelView(PostAdvanced, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Template, db.session))
admin.add_view(ModelView(Adress, db.session))

####################################################################################################################################################################
# class orders(db.Model):
#     __tablename__ = "orders"
#     id = db.Column(db.Integer, primary_key=True)
#     Province = db.Column(db.Enum(Province), unique=True, nullable=False) #enum
#     postalcode = db.Column(db.String(5), unique=False, nullable=False)
#     township = db.Column(db.String(20), unique=False, nullable=False)
#     street = db.Column(db.String(35), nullable=False, unique=True)
#     streetnumber = db.Column(db.String(24), nullable=False, unique=False)
#     flatnumber = db.Column(db.String(10), unique=False, nullable=False)
#     user = db.relationship('User', lazy='dynamic')
#
#
#     def __repr__(self):
#         return f"id = {self.id}\n name = {self.name}\n surname = {self.surename}\n mail = {self.mail}\n password = {self.password}\n age = {self.age}\n sex = {self.sex}\n nickname = {self.nickname}"
#
#     @classmethod
#     def db_to_dictionary(cls):
#         how_many_id = cls.query.all()
#         slownik = {"users" : []}
#         for id in how_many_id:
#             slownik["users"].append({"id": id.id, "name": id.name, "surename": id.surename, "mail": id.mail, "password": id.password, "age": id.age, "sex": id.sex, "nickname": id.nickname})
#         return slownik
#
#     def save_in_db(self):
#         db.session.add(self)
#         db.session.commit()
#
#     def del_in_db(self):
#         db.session.delete(self)
#         db.session.commit()
#
#
#     @classmethod
#     def find_in_db_by_id(cls, id):
#         return cls.query.filter_by(id = id).first()
#################################################################################################################################################################

# znajdz co chcesz usunac
# mojac to w pamieci uzyjesz
# odczytaj_rekordy()
@app.route("/maseczki")
def maseczki():
    nowa_maseczka = Maseczki(name="Zebra", image=r"zebra.png", color="black", size="M", sex="man", price=10, promotion=7, realprice=7)
    nowa_maseczka.save_in_db()
    # print(Maseczki.query.all())
    # for liscie i dostaniesz wszysktie rekordy
    products = Maseczki.db_to_dictionary()

    # chcialbym zeby maseczki ustawialy sie na stronie automatycznie w  zaleznosci od ilosci w zmiennej maseczki

    # lista_rzczy ktore nacze sie w projekcie albo lista rzeczy co chce miec w projekcice ;D
    return render_template('sklep-maseczki.html', maseczki=products['maseczki'])


@app.route("/kategorie")
def kategorie():
    return render_template('sklep-kategorie.html')


@app.route("/post/<id>")
def post(id):
    postadvanced = PostAdvanced.find_in_db_by_postid(id)
    for x in postadvanced:
        print(x.text)
    return render_template('post.html', postadvanced=postadvanced)


@app.route("/blog")
def blog():
    posts = Post.db_to_dictionary()
    howmanyfor = len(posts["posts"])
    return render_template('blog.html', posty=posts['posts'], howmanyfor=howmanyfor)


@app.route("/maseczka/<id>")
def maseczka(id):
    products = Maseczki.db_to_dictionary()
    return render_template('sklep-maseczka.html', maseczka=products['maseczki'][int(id)])


@app.route("/logowanie", methods=['POST', 'GET'])
def login():
    if validlogin(request.values.get("mail"), request.values.get("password")) == True:
        resp = make_response(redirect(url_for('accountaboutme')))
        resp.set_cookie('mail', request.values.get("mail"), max_age=7200)
        return resp
    return render_template('login.html')


@app.route("/rejestracja", methods=['POST', 'GET'])
def register():
    error = " "
    if request.method == 'POST':
        error = validregister()
    if error is None:
        error = " "
    return render_template('register.html', error=error)

@app.route("/konto/adresy/dodaj_nowy_adres", methods=['POST', 'GET'])
def addadres():
    error = " "
    flash("You have added adress")
    if request.method == 'POST':
        error = validaddadres()
        if error is None:
            flash("You have added adress")
            return redirect(url_for('accountadress', newadres=True))
    province = []
    for a in Province:
        province.append(a)
    # user = User.find_in_db_by_id(1)
    # print(user)
    #
    # nowy_adres = Adress(Province="Lubelskie", township="bydgoszcz", postalcode='86-011', street='ask', streetnumber='21', flatnumber='3', userid=1)
    # print(nowy_adres)
    # nowy_adres.save_in_db()
    # db.session.query(Adress).delete()
    # db.session.commit()

    return render_template('account-adres-add.html', province=province, error=error)


@app.route("/dodawaniedokoszyka/<product>/<id>/<addorundo>")
def addtobasket(product, id, addorundo):
    cookies = (request.cookies.get(f'product-{product}'))
    print(cookies)
    print(id)
    resp = make_response(redirect(url_for('basket')))
    if not cookies:
        resp.set_cookie(f'product-{product}', f".{id}", max_age=120)
        return resp
    if addorundo == "add":
        resp.set_cookie(f'product-{product}', f"{cookies}.{id}", max_age=120)
        return resp
    if addorundo == "undo":
        resp.set_cookie(f'product-{product}', f"{cookies.replace(f'.{id}', '', 1)}", max_age=120)
        return resp


@app.route("/dodawaniedokoszyka2/<product>/<id>/<addorundo>")
def addtobasket2(product, id, addorundo):
    cookies = (request.cookies.get(f'product-{product}'))
    print(cookies)
    print(id)
    resp = make_response(redirect(url_for('maseczka', id=id)))
    if not cookies:
        resp.set_cookie(f'product-{product}', f".{id}", max_age=120)
        return resp
    if addorundo == "add":
        resp.set_cookie(f'product-{product}', f"{cookies}.{id}", max_age=120)
        return resp
    if addorundo == "undo":
        resp.set_cookie(f'product-{product}', f"{cookies.replace(f'.{id}', '', 1)}", max_age=120)
        return resp


@app.route("/konto/o-mnie")
def accountaboutme():
    print(request.cookies.get('mail'))
    mail = (request.cookies.get('mail'))
    if veryfication(mail):
        user = User.get_info(mail=mail)
        print(user)
        today = datetime.today()
        user_age = datetime(user["birthyear"], user["birthmonth"], user["birthday"])
        user_month_day = datetime(datetime.today().year, user["birthmonth"], user["birthday"])
        age = today - user_age
        year = today.year - user_age.year
        if user_month_day > today:
            year = year - 1

        # uzyc datetime dla uzytkownika
        # datetime dla now() - uzytkoniwk ye=> year
        age = int(age.days/365)
        print(age)
        print(year)

        # 2020 2000  10.10  10.09
        return render_template("account-about-me.html", user=user, age=year)
    return redirect(url_for('login'))


@app.route("/konto/moje-zamówienia")
def accountorders():
    print(request.cookies.get('mail'))
    mail = (request.cookies.get('mail'))
    if veryfication(mail):
        return render_template("account-orders.html")
    return redirect(url_for('login'))


@app.route("/konto/adresy")
def accountadress(newadres=False):
    print(newadres)
    print(request.cookies.get('mail'))
    mail = (request.cookies.get('mail'))
    if veryfication(mail):
        return render_template("account-adress.html", newadres=newadres)
    return redirect(url_for('login'))
@app.route("/konto/ulubione-posty")
def accountfavoriteposts():
    print(request.cookies.get('mail'))
    mail = (request.cookies.get('mail'))
    if veryfication(mail):
        return render_template("account-favorite-posts.html")
    return redirect(url_for('login'))


def veryfication(mail):
    return mail


@app.route("/")
def index():
    products = Maseczki.db_to_dictionary()
    newproducts = [products['maseczki'][7], products['maseczki'][8], products['maseczki'][9], products['maseczki'][10],
                   products['maseczki'][11], products['maseczki'][13]]
    return render_template('index.html', newproducts=newproducts)


@app.route("/wylogowanie")
def logout():
    resp = make_response(redirect(url_for('index')))
    resp.delete_cookie('mail')
    return resp


@app.route("/koszyk")
def basket():
    masks = Maseczki.db_to_dictionary()
    products = {}
    for product in ["maseczka"]:
        try:
            cookies = [int(element) for element in request.cookies.get(f'product-{product}').split(".")[1:]]
        except AttributeError as e:
            break
        unique = set(cookies)
        ids = {}
        for a in unique:
            ids[a] = cookies.count(a)
        products[product] = ids
        print(products)
    return render_template("basket.html", maseczka=masks['maseczki'], products=products)


def validregister():
    nickname = request.values.get("nickname")
    name = request.values.get("name")
    birthday = request.values.get("birthday")
    birthmonth = request.values.get("birthmonth")
    birthyear = request.values.get("birthyear")
    sex = request.values.get("sex")
    surename = request.values.get("surename")
    mail = request.values.get("mail")
    secoundmail = request.values.get("secoundmail")
    password = request.values.get("password")
    secoundpassword = request.values.get("secoundpassword")
    user = [name, surename, mail, secoundmail, password, secoundpassword, nickname, birthday, birthmonth, birthyear, sex]
    next = "true"
    for a in user:
        if next == "true":
            if a == "":
                next = "false"
                return "nie uzupełniono wszystich pól"
    if next == "true":
        for a in user:
            for b in a:
                if next == "true":
                    if b == " ":
                        next = "false"
                        return "W formularzau nie można używać spacji"
        if next == "true":
            next = "false"
            for b in mail:
                if b == "@":
                    next = "true"
            if next == "false":
                return "adres e-mail nie zawiera @"
            if next == "true":
                if secoundmail != mail:
                    next = "false"
                    return "maile nie są identyczne"
                if next == "true":
                    if secoundpassword != password:
                        next = "false"
                        return "hasła nie są identyczne"
                    if next == "true":
                        if len(password) < 8 or len(password) > 24:
                            next = "false"
                            return "hasło może zawierać od 8 do 24 znaków"
                        if next == "true":
                            print(sex)
                            addnewuser(True, name, surename, mail, password, birthday, birthmonth, birthyear, Sex[sex].name, nickname)
                            print(nickname)

def validaddadres():
    prowince = request.values.get("Prowince")
    city = request.values.get("city")
    postalcode = request.values.get("postalcode")
    street = request.values.get("street")
    housenumber = request.values.get("housenumber")
    flatnumber = request.values.get("flatnumber")
    userid = User.get_info(request.cookies.get('mail'))
    adres = [prowince, city, postalcode, street, housenumber, flatnumber]
    next = "true"
    for a in adres:
        if next == "true":
            if a == "":
                next = "false"
                return "nie uzupełniono wszystich pól"
    if next == "true":
        for a in adres:
            for b in a:
                if next == "true":
                    if b == " ":
                        next = "false"
                        return "W formularzau nie można używać spacji"
        if next == "true":
            addnewadres(True, prowince, city, postalcode, street, housenumber, flatnumber, userid['id'])

def addnewuser(valid, name, surename, mail, password, birthday, birthmonth, birthyear, sex, nickname):
    if valid is True:
        nowy_użytkownik = User(name=name, surename=surename, mail=mail, password=password, birthday=birthday, birthmonth=birthmonth, birthyear=birthyear, sex=sex,
                               nickname=nickname)
        nowy_użytkownik.save_in_db()
        print(User.query.all())
def addnewadres(valid, province, city, postalcode, street, housenumber, flatnumber, userid):
    if valid is True:
        nowy_adres = Adress(Province=province, township=city, postalcode=postalcode, street=street, streetnumber=int(housenumber), flatnumber=int(flatnumber), userid=userid)
        print(nowy_adres)
        nowy_adres.save_in_db()

def validlogin(mail, password):
    users = User.db_to_dictionary()
    for user in users["users"]:
        if user["mail"] == mail and user['password'] == password:
            return True
        else:
            print("e-mail lub hasło są błędne")
            return False


if __name__ == "__main__":
    app.run(port=8000, debug=True)
