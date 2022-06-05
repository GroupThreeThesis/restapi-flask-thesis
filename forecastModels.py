from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
#Table for Prediction Inputs (TimeLag)
class PredictModel(db.Model):
    __tablename__ = 'predict'
    id = db.Column(db.Integer, primary_key=True)
    timelag1 = db.Column(db.Integer())
    timelag2 = db.Column(db.Integer())
    timelag3 = db.Column(db.Integer())
    timelag4 = db.Column(db.Integer())
    timelag5 = db.Column(db.Integer())


    def __init__(self, timelag1, timelag2, timelag3, timelag4, timelag5):
        self.timelag1 = timelag1
        self.timelag2 = timelag2
        self.timelag3 = timelag3
        self.timelag4 = timelag4
        self.timelag5 = timelag5

    def json(self):
        return{"timelag1":self.timelag1, "timelag2":self.timelag2, "timelag3":self.timelag3, "timelag4":self.timelag4, "timelag5":self.timelag5}

#Table for Tarlac Total Covid-19 Cases input(Cases)
class TotalCovidCasesModel(db.Model):
    __tablename__ = 'tarlactotalcovidcases'
    id = db.Column(db.Integer, primary_key=True)
    totalcovidcases = db.Column(db.Integer())

    def __init__(self, totalcovidcases):
        self.totalcovidcases = totalcovidcases
    
    def json(self):
        return{"totalcovidcases": self.totalcovidcases}

#Table for Mortality Rate Input
class MortalityRateModel(db.Model):
    __tablename__ = 'mortalityrate'
    id = db.Column(db.Integer, primary_key=True)
    mortalitycount = db.Column(db.Integer())

    def __init__(self, mortalitycount):
        self.mortalitycount = mortalitycount
    
    def json(self):
        return{"mortalitycount": self.mortalitycount}



#Table for Recovery Rate Input
class RecoveryRateModel(db.Model):
    __tablename__ = 'recoveryrate'
    id = db.Column(db.Integer, primary_key=True)
    recoverycount = db.Column(db.Integer())

    def __init__(self, recoverycount):
        self.recoverycount = recoverycount
    
    def json(self):
        return{"recoverycount": self.recoverycount}

#Table for Cases by Municipality Input
class CasesByMunicipalityModel(db.Model):
    __tablename__ = 'casesbymunicipality'
    id = db.Column(db.Integer, primary_key=True)
    anao = db.Column(db.Integer())
    bamban = db.Column(db.Integer())
    camiling = db.Column(db.Integer())
    capas = db.Column(db.Integer())
    concepcion = db.Column(db.Integer())
    gerona = db.Column(db.Integer())
    lapaz = db.Column(db.Integer())
    mayantoc = db.Column(db.Integer())
    moncada = db.Column(db.Integer())
    paniqui = db.Column(db.Integer())
    pura = db.Column(db.Integer())
    ramos = db.Column(db.Integer())
    sanclemente = db.Column(db.Integer())
    sanjose = db.Column(db.Integer())
    sanmiguel = db.Column(db.Integer())
    santaignacia = db.Column(db.Integer())
    tarlaccity = db.Column(db.Integer())
    victoria = db.Column(db.Integer())

    def __init__(self, anao, bamban, camiling, capas, concepcion, gerona, lapaz, mayantoc, moncada, 
    paniqui, pura, ramos, sanclemente, sanjose, sanmiguel, santaignacia, tarlaccity, victoria):
        self.anao = anao
        self.bamban = bamban
        self.camiling = camiling
        self.capas = capas
        self.concepcion = concepcion
        self.gerona = gerona
        self.lapaz = lapaz
        self.mayantoc = mayantoc
        self.moncada = moncada
        self.paniqui = paniqui
        self.pura = pura
        self.ramos = ramos
        self.sanclemente = sanclemente
        self.sanjose = sanjose
        self.sanmiguel = sanmiguel
        self.santaignacia = santaignacia
        self.tarlaccity = tarlaccity
        self.victoria = victoria

    
    def json(self):
        return{"anao": self.anao, "bamban": self.bamban,"camiling": self.camiling,"capas": self.capas,"concepcion": self.concepcion,
        "gerona": self.gerona,"lapaz": self.lapaz,"mayantoc": self.mayantoc,"moncada": self.moncada,"paniqui": self.paniqui,
        "pura": self.pura,"ramos": self.ramos,"sanclemente": self.sanclemente,"sanjose": self.sanjose,"sanmiguel": self.sanmiguel,
        "santaignacia": self.santaignacia,"tarlaccity": self.tarlaccity,"victoria": self.victoria,}


