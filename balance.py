from sqlite import Sqlite
import time

class Balance(Sqlite):

  table = "balance" #Used in sqlite for common methods (all,count)

  def __init__(self):
    Sqlite.__init__(self)
    #This table must be included in the default schema (see evolutions)

  def save(self,weight, user):
    c = self._conn.cursor()
    now = int(time.time())
    c.execute("INSERT INTO balance (timestamp, weight, user) VALUES (?,?,?)",[now, weight, user])
    self._conn.commit()
    c.close()
