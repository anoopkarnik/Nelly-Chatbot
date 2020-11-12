import datetime
from NellyStore import *

def db_getChatCount(PreviousDays):
    _dateTo = datetime.utcnow()
    _dateFrom = _dateTo + datetime.timedelta(days=-1*PreviousDays)
    _db = get_data_coll()
    _db.aggregate([
        {"$match": { "TimeStamp": { "$gte": _dateFrom }}},
        {"$group" :
         {"_id":
          {
              "SessionID":"$SessionID",
              "Date": { "$dateToString" : { format: "%Y-%m-%d", date: "$TimeStamp"}}
              }
          },
          "Count" : {"$sum": 1}
          }])
    return  _db.find_one({'_id':ObjectId(_id)})
