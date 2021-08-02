from flask import Flask, render_template, url_for, redirect, request, make_response
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import enum

app = Flask(__name__)
app.secret_key = "bardzo trudny string do zlamania"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db =  SQLAlchemy(app)
db.create_all() # odkomentowac
db.session.commit()

def create_app():
    app = Flask(__name__)
    db.init_app(app)
    app.secret_key = "bardzo trudny string do zlamania"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    return app

app = create_app()
db.create_all(app=app)







class Maseczki(db.Model):
    __tablename__ = "maseczki"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    image = db.Column(db.String(50), nullable=False, unique=False)
    color = db.Column(db.String(20), nullable=False, unique=False)
    size = db.Column(db.String(3), nullable=False, unique=False)
    sex = db.Column(db.String(10), nullable=False, unique=False)
    price = db.Column(db.Integer, nullable=False, unique=False)

    def __repr__(self):
        return f"id = {self.id}\n name = {self.name}\n image = {self.image}\n color = {self.color},\n size = {self.size}\n sex = {self.sex}\n price = {self.price}\n\n"

    @classmethod
    def db_to_dictionary(cls):
        how_many_id = cls.query.all()
        slownik = {"maseczki" : []}
        for id in how_many_id:
            slownik["maseczki"].append({"id": id.id, "name": id.name, "image": id.image, "color": id.color, "size": id.size, "sex": id.sex, "price": id.price})
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
    surename= db.Column(db.String(20), unique=False, nullable=False)
    mail = db.Column(db.String(35), nullable=False, unique=True)
    password = db.Column(db.String(24), nullable=False, unique=False)
    sex = db.Column(db.Enum(Sex), unique=False, nullable=False) # jeden z kilku?
    age = db.Column(db.Integer, unique=False, nullable=False) # czy data urodzenia?


    def __repr__(self):
        return f"id = {self.id}\n name = {self.name}\n surname = {self.surename}\n mail = {self.mail}\n password = {self.password}\n age = {self.age}\n sex = {self.sex}\n nickname = {self.nickname}"

    @classmethod
    def db_to_dictionary(cls):
        how_many_id = cls.query.all()
        slownik = {"users" : []}
        for id in how_many_id:
            slownik["users"].append({"id": id.id, "name": id.name, "surename": id.surename, "mail": id.mail, "password": id.password, "age": id.age, "sex": id.sex, "nickname": id.nickname})
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


class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.String(30), unique=True, nullable=False)
    header = db.Column(db.String(38), unique=False, nullable=False)
    text = db.Column(db.String(587), unique=False, nullable=False)
    templatesnumber = db.Column(db.Intiger, unique=False, nullable=False)

    def __repr__(self):
        return f"id = {self.id}\n img = {self.img}\n header = {self.header}\n text = {self.text}\n templatesnumber = {self.templatesnumber}"

    @classmethod
    def db_to_dictionary(cls):
        how_many_id = cls.query.all()
        slownik = {"posts": []}
        for id in how_many_id:
            slownik["posts"].append(
                {"id": id.id, "img": id.img, "header": id.header, "text": id.text, "templatesnumber": id.templatesnumber})
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
    templatenumber = db.Column(db.Intiger, unique=False, nullable=False)
    template = db.Column(db.Intiger, unique=False, nullable=False)

    def __repr__(self):
        return f"id = {self.id}\n img = {self.img}\n img2 = {self.img2}\n text = {self.text}\n text2 = {self.text2}\n templatenumber = {self.templatenumber}\n template = {self.templatenumber}"

    @classmethod
    def db_to_dictionary(cls):
        how_many_id = cls.query.all()
        slownik = {"posts": []}
        for id in how_many_id:
            slownik["posts"].append(
                {"id": id.id, "img": id.img, "img2": id.img2, "text": id.text, "text2": id.text2, "templatesnumber": id.templatenumber, "template": id.template})
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

class Template(db.Model):
    __tablename__ = "template"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)

    def __repr__(self):
        return f"id = {self.id}\n img = {self.img}\n img2 = {self.img2}\n text = {self.text}\n text2 = {self.text2}\n templatenumber = {self.templatenumber}\n template = {self.templatenumber}"

    @classmethod
    def db_to_dictionary(cls):
        how_many_id = cls.query.all()
        slownik = {"posts": []}
        for id in how_many_id:
            slownik["posts"].append(
                {"id": id.id, "img": id.img, "img2": id.img2, "text": id.text, "text2": id.text2, "templatesnumber": id.templatenumber, "template": id.template})
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
####################################################################################################################################################################
# class adress(db.Model):
#     __tablename__ = "adress"
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
#
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
    nowa_maseczka = Maseczki(name="Zebra", image=r"zebra.png", color="black", size="M", sex="man", price=10)
    nowa_maseczka.save_in_db()
    # print(Maseczki.query.all())
    # for liscie i dostaniesz wszysktie rekordy
    products = Maseczki.db_to_dictionary()
    #chcialbym zeby maseczki ustawialy sie na stronie automatycznie w  zaleznosci od ilosci w zmiennej maseczki

    # lista_rzczy ktore nacze sie w projekcie albo lista rzeczy co chce miec w projekcice ;D
    return render_template('sklep-maseczki.html', maseczki=products['maseczki'])


@app.route("/kategorie")
def kategorie():
    return render_template('sklep-kategorie.html')

@app.route("/post")
def post():
    return render_template('post.html')

@app.route("/blog")
def blog():
    posts = {"posts" : [{"id" : 1, "img" : "post1.jpg", "header" : "Maseczka z drucikem jak uszyć?", "text" : "text numer 1"}, {"id" : 2, "img" : "slide1.jpg", "header" : "Jak zrobić slider w css", "text" : "text numer 2"}]}
    howmanyfor = len(posts["posts"])
    return render_template('blog.html', posty=posts['posts'], howmanyfor = howmanyfor)

@app.route("/maseczka/<id>")
def maseczka(id):
    products = Maseczki.db_to_dictionary()
    return render_template('sklep-maseczka.html', maseczka=products['maseczki'][int(id)])

@app.route("/logowanie", methods=['POST', 'GET'])
def login():
    if validlogin(request.values.get("mail"), request.values.get("password")) == True:
        resp = make_response(redirect(url_for('accountaboutme')))
        resp.set_cookie('mail', request.values.get("mail"), max_age=300)
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
        return render_template("account-about-me.html")
    return redirect(url_for('login'))

@app.route("/konto/moje-zamówienia")
def accountorders():
    print(request.cookies.get('mail'))
    mail = (request.cookies.get('mail'))
    if veryfication(mail):
        return render_template("account-orders.html")
    return redirect(url_for('login'))

@app.route("/konto/bezpieczeństwo")
def accountseciurity():
    print(request.cookies.get('mail'))
    mail = (request.cookies.get('mail'))
    if veryfication(mail):
        return render_template("account-seciurity.html")
    return redirect(url_for('login'))

@app.route("/konto/adresy")
def accountadress():
    print(request.cookies.get('mail'))
    mail = (request.cookies.get('mail'))
    if veryfication(mail):
        return render_template("account-adress.html")
    return redirect(url_for('login'))\

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
    newproducts = [products['maseczki'][7], products['maseczki'][8], products['maseczki'][9], products['maseczki'][10], products['maseczki'][11], products['maseczki'][13]]
    return render_template('index.html', newproducts = newproducts)

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
    age = request.values.get("age")
    sex = request.values.get("sex")
    surename = request.values.get("surename")
    mail = request.values.get("mail")
    secoundmail = request.values.get("secoundmail")
    password = request.values.get("password")
    secoundpassword = request.values.get("secoundpassword")
    user = [name, surename, mail, secoundmail, password, secoundpassword, nickname, age, sex]
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
                            addnewuser(True, name, surename, mail, password, age, Sex[sex].name, nickname)

                            print(age)
                            print(nickname)
def addnewuser(valid, name, surename, mail, password, age, sex, nickname):
    if valid is True:
        nowy_użytkownik = User(name=name, surename=surename,mail=mail, password=password, age=age, sex=sex, nickname=nickname)
        nowy_użytkownik.save_in_db()
        print(User.query.all())
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
