from ast import Str
import json

from flask import  Flask, jsonify, request
from flask_restful import Api, Resource
from forecastModels import PredictModel, TotalCovidCasesModel,MortalityRateModel,RecoveryRateModel,CasesByMunicipalityModel, db
from flask_cors import CORS, cross_origin
import pickle
import numpy as np

app = Flask(__name__)


CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)
db.init_app(app)

@app.before_first_request
def create_table():
    db.create_all()
    


class PredictView(Resource):

    '''
    parser = reqparse.RequestParser()
    parser.add_argument('timelag1', 
        type=str,
        required=True,
        help = "Can't leave blank"
    )    
    parser.add_argument('timelag1', 
        type=float,
        required=True,
        help = "Can't leave blank"
    )   
    parser.add_argument('timelag1', 
        type=str,
        required=True,
        help = "Can't leave blank"
    )'''

    
    def get(self):
        TAG = "======>>>"
        predict = PredictModel.query.all()
        # sample0 = list(x.json() for x in predict)
        # sample1 = list(predict.values())
        # print(TAG, sample1)
        return {'Predict': list(x.json() for x in predict)}
        

        
    def post(self):
        TAG = "This is post data===========>>>"
        data = request.get_json()
        new_predict = PredictModel(data['timelag1'],data['timelag2'],data['timelag3'],data['timelag4'],data['timelag5'])
        # sample = list(new_predict.values())
        # row = list(map(int, sample))
        print(TAG, new_predict)
        db.session.add(new_predict)
        db.session.commit()
        db.session.flush()
        return new_predict.json(),201

    
class SinglePredictView(Resource):
    
    def get(self,id):
        TAG = "Inputted Time Lag===========>>>"
        predict = PredictModel.query.filter_by(id=id).first()
        filename = 'xgb_mlmodel_tarlactotalcovid19cases.pkl'
        model_loaded = pickle.load(open(filename, "rb"))
        sample1 = predict.json()
        sample2 = list(sample1.values())
        finalData = list(map(int, sample2))
        predvalues = list()
        print(TAG, finalData)
        for i in range(len(finalData)):
            if i == len(finalData)-1:
                predvalues.append(np.mean(predvalues))
                break
            out = (finalData[i+1] - finalData[i])
            predvalues.append(out)
        newrow = np.array(predvalues)
        result = model_loaded.predict([newrow])
        prediction = str(self.pred_dataout(result, finalData))
        mypreds = [int(i) for i in prediction.strip("[]").split(",")]

        if predict:
               return jsonify([mypreds])
        return {'message':'Product I.D not Found'}, 404


    def pred_dataout(self, predicted_val, row):
        pvtolist = list(predicted_val)
        listostr = "{}".format(pvtolist)
        input_seq = len(row)-1
        finalpred = list()
        filteringst = ''.join([c for c in listostr if c in '0123456789.,'])
        predicted_valsformatted = filteringst.split(",",21)
        predicted_vals = np.array(predicted_valsformatted, dtype=np.float32)
        for i in range(len(predicted_vals)):
            if i == 0:
                out = (row[input_seq] + predicted_vals[i])
                finalpred.append(int(out))
            elif i == len(predicted_vals)-1:
                break
            else:
                out = (finalpred[i-1] + predicted_vals[i])
                finalpred.append(int(out))
        return finalpred

    def delete(self,id):
       predict = PredictModel.query.filter_by(id=id).first()
       if predict:
           db.session.delete(predict)
           db.session.commit()
           return {'message': 'deleted'}
       else:
           return {'message':'Predict not Found'},404

    def put(self, id):
       TAG = "This is updated data===========>>>"
       data = request.get_json()
       predict = PredictModel.query.filter_by(id=id).first()
       if predict:
           predict.timelag1 = data['timelag1']
           predict.timelag2 = data['timelag2']
           predict.timelag3 = data['timelag3']
           predict.timelag4 = data['timelag4']
           predict.timelag5 = data['timelag5']
       else:
           predict = PredictModel(id=id, **data)
       print(TAG, predict)
       db.session.add(predict)
       db.session.commit()

       return predict.json()

    

#Section for Total Covid Cases
class TotalCovidCasesView(Resource):
    def post(self):
        data = request.get_json()
        new_totalcovidcases = TotalCovidCasesModel(data['totalcovidcases'])
        db.session.add(new_totalcovidcases)
        db.session.commit()
        db.session.flush()
        return new_totalcovidcases.json(),201
   
    def get(self):
        TAG = "======>>>"
        totalcovidcases = TotalCovidCasesModel.query.all()
        return {'Total Covid Cases': list(x.json() for x in totalcovidcases)}

class SingleTotalCovidCasesView(Resource):
    def get(self,id):
        totalcovidcases = TotalCovidCasesModel.query.filter_by(id=id).first()
        if totalcovidcases:
           json_totalcovidcases = totalcovidcases.json()
           value_totalcovidcases = json_totalcovidcases.values()
           map_totalcovidcases = list(map(int, value_totalcovidcases))
           int_totalcovidcases = map_totalcovidcases[0]

           return jsonify([int_totalcovidcases, int_totalcovidcases])
        return {'message':'Product I.D not Found'}, 404

    def delete(self,id):
       totalcovidcases = TotalCovidCasesModel.query.filter_by(id=id).first()
       if totalcovidcases:
           db.session.delete(totalcovidcases)
           db.session.commit()
           
           return {'message': 'deleted'}
       else:
           return {'message':'Predict not Found'},404

    def put(self, id):
       data = request.get_json()
       totalcovidcases = TotalCovidCasesModel.query.filter_by(id=id).first()
       if totalcovidcases:
           totalcovidcases.totalcovidcases = data['totalcovidcases']
       else:
           totalcovidcases = TotalCovidCasesModel(id=id, **data)
      
       db.session.add(totalcovidcases)
       db.session.commit()

       return totalcovidcases.json()

#Section for Mortality Rate
class MortalityRate(Resource):
    def post(self):
        data = request.get_json()
        data2 = request.get_json()
        new_mortalitycount = MortalityRateModel(data['mortalitycount'])
        db.session.add(new_mortalitycount)
        db.session.commit()
        db.session.flush()
        return new_mortalitycount.json(),201
   
    def get(self):
        TAG = "======>>>"
        mortalitycount = MortalityRateModel.query.all()
        return {'Mortality Rate': list(x.json() for x in mortalitycount)}

class SingleMortalityRate(Resource):
    def get(self,id):
        TAG = "Result>>>>>>>>"
        mortalitycount = MortalityRateModel.query.filter_by(id=id).first()
        totalcovidcases = TotalCovidCasesModel.query.filter_by(id=id).first()
        allmortalitycount = MortalityRateModel.query.all()
        #converting mortality count into int
        json_mortalitycount = mortalitycount.json()
        value_mortalitycount = json_mortalitycount.values()
        map_mortalitycount = list(map(int, value_mortalitycount))
        int_mortalitycount = map_mortalitycount[0]

        #all mortality count
        a = list(x.json() for x in allmortalitycount)
        a_key = "mortalitycount"
        values_of_key = [a_dict[a_key] for a_dict in a]
        map_mortalitycountall = list(map(int, values_of_key))
        lengthoflist = len(map_mortalitycountall)
        int_mortalitycountall = map_mortalitycountall[lengthoflist-2]
        
        #converting totalcovidcases into int
        json_totalcovidcases = totalcovidcases.json()
        value_totalcovidcases = json_totalcovidcases.values()
        map_totalcovidcases = list(map(int, value_totalcovidcases))
        int_totalcovidcases = map_totalcovidcases[0]

        #processing mortalitycount to make it rate(mortalitycount/totalcovidcases*100)
        mortalitycount_formula = int_mortalitycount/int_totalcovidcases*100
        mortalitycount_rate = round(mortalitycount_formula, 2)

        #getting the total covid 19 cases rate(100 - mortality_rate )
        totalcovidcases_rate = 100 - mortalitycount_rate
        inputted_totalcovidcases = int_totalcovidcases*1
       
       #getting the increase percentage for mortality rate
        mortalitycountincrease = int_mortalitycount - int_mortalitycountall
        formulamortalitycountincrease = mortalitycountincrease/int_mortalitycountall*100
        percentmortalitycountincrease = round(formulamortalitycountincrease,2)


        print(TAG )
        if mortalitycount:
           return jsonify([mortalitycount_rate, totalcovidcases_rate, inputted_totalcovidcases, percentmortalitycountincrease, mortalitycountincrease])
        return {'message':'Product I.D not Found'}, 404

    def delete(self,id):
       mortalitycount = MortalityRateModel.query.filter_by(id=id).first()
       if mortalitycount:
           db.session.delete(mortalitycount)
           db.session.commit()
           return {'message': 'deleted'}
       else:
           return {'message':'Predict not Found'},404

    def put(self, id):
       data = request.get_json()
       mortalitycount = MortalityRateModel.query.filter_by(id=id).first()
       if mortalitycount:
           mortalitycount.mortalitycount = data['mortalitycount']
       else:
           mortalitycount = MortalityRateModel(id=id, **data)
      
       db.session.add(mortalitycount)
       db.session.commit()

       return mortalitycount.json()




#Section for Recovery Rate
class RecoveryRate(Resource):
    def post(self):
        data = request.get_json()
        new_recoverycount = RecoveryRateModel(data['recoverycount'])
        db.session.add(new_recoverycount)
        db.session.commit()
        db.session.flush()
        return new_recoverycount.json(),201
   
    def get(self):
        TAG = "======>>>"
        recoverycount = RecoveryRateModel.query.all()
        return {'Recovery Rate': list(x.json() for x in recoverycount)}

class SingleRecoveryRate(Resource):
    def get(self,id):
        TAG = "Recovery Count>>>>>>>>"
        recoverycount = RecoveryRateModel.query.filter_by(id=id).first()
        allrecoverycount = RecoveryRateModel.query.all()
        #converting recovery count into int
        json_recoverycount = recoverycount.json()
        value_recoverycount = json_recoverycount.values()
        map_recoverycount = list(map(int, value_recoverycount))
        int_recoverycount = map_recoverycount[0]

        totalcovidcases = TotalCovidCasesModel.query.filter_by(id=id).first()
        #converting totalcovidcases into int
        json_totalcovidcases = totalcovidcases.json()
        value_totalcovidcases = json_totalcovidcases.values()
        map_totalcovidcases = list(map(int, value_totalcovidcases))
        int_totalcovidcases = map_totalcovidcases[0]

        #all recovery count
        a = list(x.json() for x in allrecoverycount)
        a_key = "recoverycount"
        values_of_key = [a_dict[a_key] for a_dict in a]
        map_recoverycountall = list(map(int, values_of_key))
        lengthoflist = len(map_recoverycountall)
        int_recoverycountall = map_recoverycountall[lengthoflist-2]

        #processing mortalitycount to make it rate(mortalitycount/totalcovidcases*100)
        recoverycount_formula = int_recoverycount/int_totalcovidcases*100
        recoverycount_rate = round(recoverycount_formula, 2)

        #getting the total covid 19 cases rate(100 - mortality_rate )
        totalcovidcases_rate = round(100 - recoverycount_rate, 2)
        inputted_totalcovidcases = int_totalcovidcases*1

        #getting the increase percentage for recovery rate
        recoverycountincrease = int_recoverycount - int_recoverycountall
        formularecoverycountincrease = recoverycountincrease/int_recoverycountall*100
        percentrecoverycountincrease = round(formularecoverycountincrease,2)
        TAG2 = "toatal CC>>>>>"
        print(TAG, int_recoverycount )
        print(TAG2, int_totalcovidcases)
        if recoverycount:
           return jsonify([recoverycount_rate, totalcovidcases_rate, inputted_totalcovidcases, percentrecoverycountincrease, recoverycountincrease])
        return {'message':'Product I.D not Found'}, 404

    def delete(self,id):
       recoverycount = RecoveryRateModel.query.filter_by(id=id).first()
       if recoverycount:
           db.session.delete(recoverycount)
           db.session.commit()
           return {'message': 'deleted'}
       else:
           return {'message':'Predict not Found'},404

    def put(self, id):
       data = request.get_json()
       recoverycount = RecoveryRateModel.query.filter_by(id=id).first()
       if recoverycount:
           recoverycount.recoverycount = data['recoverycount']
       else:
           recoverycount = RecoveryRateModel(id=id, **data)
      
       db.session.add(recoverycount)
       db.session.commit()

       return recoverycount.json()

#Section for Cases by Municipality
class CasesByMunicipality(Resource):
    def post(self):
        TAG = "This is post data===========>>>"
        data = request.get_json()
        new_cases = CasesByMunicipalityModel(data['anao'],data['bamban'],data['camiling'],data['capas'],data['concepcion']
        ,data['gerona'],data['lapaz'],data['mayantoc'],data['moncada'],data['paniqui'],data['pura']
        ,data['ramos'],data['sanclemente'],data['sanjose'],data['sanmiguel'],data['santaignacia'],data['tarlaccity']
        ,data['victoria'])
        db.session.add(new_cases)
        db.session.commit()
        db.session.flush()
        return new_cases.json(),201
    def get(self):
        TAG = "======>>>"
        cases = CasesByMunicipalityModel.query.all()
        return {'Cases By Municipality': list(x.json() for x in cases)}

class SingleCasesByMunicipality(Resource):
    def get(self,id):
        TAG = "===========>>>"
        cases = CasesByMunicipalityModel.query.filter_by(id=id).first()
        totalcovidcases = TotalCovidCasesModel.query.filter_by(id=id).first()
        alltotalcovidcases = TotalCovidCasesModel.query.all()
        json_cases = cases.json()
        values_cases = list(json_cases.values())
        int_cases = list(map(int, values_cases))
        
        #converting totalcovidcases into int
        json_totalcovidcases = totalcovidcases.json()
        value_totalcovidcases = json_totalcovidcases.values()
        map_totalcovidcases = list(map(int, value_totalcovidcases))
        int_totalcovidcases = map_totalcovidcases[0]

        #all total covid cases
        a = list(x.json() for x in alltotalcovidcases)
        a_key = "totalcovidcases"
        values_of_key = [a_dict[a_key] for a_dict in a]
        map_totalcovidcasesall = list(map(int, values_of_key))
        lengthoflist = len(map_totalcovidcasesall)
        int_totalcovidcasesall = map_totalcovidcasesall[lengthoflist-2]
        
        #getting the increase percentage for total ccovid cases
        totalcovidcasesincrease = int_totalcovidcases - int_totalcovidcasesall
        formulatotalcovidcasesincrease = totalcovidcasesincrease/int_totalcovidcasesall*100
        percenttotalcovidcasesincrease = round(formulatotalcovidcasesincrease, 2)
        if cases:
               return jsonify([int_cases, percenttotalcovidcasesincrease, totalcovidcasesincrease])
        return {'message':'Product I.D not Found'}, 404

    def delete(self,id):
       cases = CasesByMunicipalityModel.query.filter_by(id=id).first()
       if cases:
           db.session.delete(cases)
           db.session.commit()
           return {'message': 'deleted'}
       else:
           return {'message':'Predict not Found'},404

    def put(self, id):
       data = request.get_json()
       cases = CasesByMunicipalityModel.query.filter_by(id=id).first()
       if cases:
           cases.anao = data['anao']
           cases.bamban = data['bamban']
           cases.camiling = data['camiling']
           cases.capas = data['capas']
           cases.concepcion = data['concepcion']
           cases.gerona = data['gerona']
           cases.lapaz = data['lapaz']
           cases.mayantoc = data['mayantoc']
           cases.moncada = data['moncada']
           cases.paniqui = data['paniqui']
           cases.pura = data['pura']
           cases.ramos = data['ramos']
           cases.sanclemente = data['sanclemente']
           cases.sanjose = data['sanjose']
           cases.sanmiguel = data['sanmiguel']
           cases.santaignacia = data['santaignacia']
           cases.tarlaccity = data['tarlaccity']
           cases.victoria = data['victoria']

       else:
           cases = CasesByMunicipalityModel(id=id, **data)
      
       db.session.add(cases)
       db.session.commit()

       return cases.json()

api.add_resource(PredictView, '/predict')
api.add_resource(SinglePredictView, '/predict/<int:id>')

api.add_resource(TotalCovidCasesView, '/totalcovidcases')
api.add_resource(SingleTotalCovidCasesView, '/totalcovidcases/<int:id>')

api.add_resource(MortalityRate, '/mortalitycount')
api.add_resource(SingleMortalityRate, '/mortalitycount/<int:id>')

api.add_resource(RecoveryRate, '/recoverycount')
api.add_resource(SingleRecoveryRate, '/recoverycount/<int:id>')

api.add_resource(CasesByMunicipality, '/casesbymunicipality')
api.add_resource(SingleCasesByMunicipality, '/casesbymunicipality/<int:id>')


if __name__ == '_main_':
    app.run(debug = True)
