from flask import Flask, render_template, url_for, redirect, request, make_response
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import enum

app = Flask(__name__)
app.secret_key = "bardzo trudny string do zlamania"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
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


@app.route("/maseczka/<id>")
def maseczka(id):
    products = Maseczki.db_to_dictionary()
    return render_template('sklep-produkt.html', maseczka=products['maseczki'][int(id)])

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
    return render_template('index.html')

@app.route("/wylogowanie")
def logout():
    resp = make_response(redirect(url_for('index')))
    resp.delete_cookie('mail')
    return resp

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
