from market import db, bcrypt , login_manger
from flask_login import UserMixin


@login_manger.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model , UserMixin):
    id  = db.Column(db.Integer, primary_key=True)
    username  = db.Column(db.String(length=30), nullable=False, unique=True )
    email  = db.Column(db.String(length=50), nullable=False, unique=True )
    password_hash  = db.Column(db.String(length=60), nullable=False)
    budget  = db.Column(db.Integer() , nullable=False , default = 1000)
    item = db.relationship('Item' , backref = 'owned_user' , lazy = True)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')


    @property
    def prittier_budget(self):
        if len(str(self.budget)) >= 4:
            return f"{str(self.budget)[:-3]},{str(self.budget)[-3:]}$"
        else:
            return f"{self.budget}$"

# my func to display bugdet in better form ..

    def pr(self , x):
        '''
        returns budget in good form ..
        but call it inside ','.join(reversed(list( here )))
        '''
        x = str(x)
        while len(x) >= 4:
            res = x[-3:]
            x = x[:-3]
            yield res
        else:
            yield x 

    @property
    def budget_pr(self):
        return ','.join(reversed(list(self.pr(self.budget)))) + '$'


    def check_password_correction(self , attemted_password):
        return bcrypt.check_password_hash(self.password_hash ,attemted_password)

    def can_purchase(self , item_obj):
        return self.budget >= item_obj.price 

    def can_sell(self , obj):
        return obj in self.item

    def __repr__(self):
        return f'User name : {self.username}'


class Item(db.Model):
    id  = db.Column(db.Integer, primary_key=True)
    name  = db.Column(db.String(length=30), nullable=False, unique=True )
    price  = db.Column(db.Integer(), nullable=False)
    barcode  = db.Column(db.String(length=12), nullable=False, unique=True )
    description  = db.Column(db.String(length=1024), nullable=False , unique=True)
    owner = db.Column(db.Integer() , db.ForeignKey('user.id'))

    def buy(self, usr):
        self.owner = usr.id
        usr.budget -= self.price
        db.session.commit()

    def sell(self, usr):
        self.owner = None
        usr.budget += self.price
        db.session.commit()

    def __repr__(self):
        return f'Item object name : {self.name}'
