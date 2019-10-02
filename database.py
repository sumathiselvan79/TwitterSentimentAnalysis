
import pyrebase
config = {
    "apiKey": "AIzaSyAl9dATghwb-SfjiAgCiZ4NPh27cPGl2_8",
    "authDomain": "riskmap-1535607326285.firebaseapp.com",
    "databaseURL": "https://riskmap-1535607326285.firebaseio.com",
    "projectId": "riskmap-1535607326285",
    "storageBucket" : "riskmap-1535607326285.appspot.com",
    "messagingSenderId": "801660111392"
  }
#
def insertData(dictionary):
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    db.child("/").remove()
    results = db.child("/").push(dictionary)
    return results

