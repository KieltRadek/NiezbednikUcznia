from ModelsDataBase.DataBase import Base, engine
from ModelsDataBase.User import User
from ModelsDataBase.Schedule import Schedule
from ModelsDataBase.Grade import Grade

#tu tworzymy bazę JEDNORAZOWO, w mainie z GUI tworzyłaby się za kazdym razem
if __name__ == '__main__':
    Base.metadata.create_all(engine)
    print("Utworzono baze danych")