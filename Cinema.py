import os
from datetime import datetime

#Provided rules:
#time formated in 00:00
#duration of the movie is in minutes

class Movie():
    def __init__(self, title:str, duration:int, showtimes:list):
        #The class is iniciated, with duration and time validation according to the rules above.
        self.title = title
        if not self.validate_duration(duration):
                raise TypeError("Valid duration is an int larger than 0 (in minutes)")
        self.duration = duration
        for time in showtimes:
            if self.validate_time(time) == False:
                raise TypeError("Valid time format is 00:00 and must be included in <8:00, 20:00>")
            
        self.showtime = showtimes
    @staticmethod
    def validate_time(time:str) -> bool:
        #Time validation according to the rules mentioned above
        try:
            datetime.strptime(time, "%H:%M")
        except ValueError:
            return False
        time = time.split(":")
        numericTime =  int(time[0])*60 + int(time[1])
        return numericTime >= 8*60 and numericTime <= 20*60
    
    @staticmethod
    def validate_duration(duration:int) -> bool:
        #Duration validation according to the rules mentioned above
        return duration > 0
       
    def add_showtime(self, time:str):
        #Adds a screening time
        if self.validate_time(time):
            if time in self.showtime:
                print("This movie already runs at this time")
            else:
                self.showtime.append(time)

    def remove_showtime(self, time:str):
        #Removes a screening time
        if time in self.showtime:
            self.showtime.remove(time)
        else:
            print("No showtime at this time.")

    def display_details(self, printMode=False) ->dict:
        #Displays all the movie details in 2 types.
        #False - As a returned list  (default)
        #True - As printed values

        data = {"title":self.title, "duration":self.duration, "showtimes": self.showtime}
        if printMode == False: return data
        else:
            print(f"Title: {self.title}")
            print(f"Duration {int(self.duration/60)}h {self.duration%60}m")
            print(f"Showtimes: {self.showtime}")

class Customer():
    def __init__(self, first_name:str, last_name:str):
         #The class is iniciated
         self.first_name = first_name
         self.last_name = last_name
         self.reservations = []
    def add_reservation(self, movie:Movie, time:str, private_reservation = False, vip = False):
        #Adds a reservation as a disctionary into the reservation list
        #Takes into account the posibility of a VIP customer
        if movie.validate_time(time) == False:
            raise TypeError("Valid time format is 00:00 and must be included in <8:00, 20:00>")
        if time in movie.showtime:
            if private_reservation:
                self.reservations.append({"Movie":movie.title, "Time": time, "ReservationType":"Private", "Discount":"VIP"})
            else:
                if vip:
                    self.reservations.append({"Movie":movie.title, "Time": time, "ReservationType":"Normal", "Discount":"VIP"})
                else:
                    self.reservations.append({"Movie":movie.title, "Time": time, "ReservationType":"Normal", "Discount":"None"})  
        else:
            print("No movie at this time")
    def display_reservations(self):
        #Prints out the self.reservation list
        print(f"{self.first_name} {self.last_name}")
        for rsrv in self.reservations:
            print(rsrv)

class VIPCustomer(Customer):
    def __init__(self, first_name, last_name):
        #The class is iniciated
        super().__init__(first_name, last_name)
    def get_discounted_price(self, price:int) -> int:
        #Adds a discount to the price, can be used later in code with the reservation dictionary
        return price * 0.8
    def book_private_show(self, movie:Movie, time:str):
        #Books a private show, changing the values of add_reservation function
        super().add_reservation(movie, time, True, True)

         
class Cinema():
    def __init__(self):
        #The class is iniciated
        self.movieList = []
        self.customerList = []

    def add_movie(self, movie:Movie):
        #Adds a movie
        self.movieList.append(movie)

    def add_customer(self, customer:Customer):
        #Adds a customer
        self.customerList.append(customer)

    def display_movies(self):
        #Displays all movies in the self.movieList list
        for movie in self.movieList:
            print(movie.display_details())

#Application capability showcase
def main():

    #Two test movies
    from_movie = Movie("From", 230, ["8:00", "9:00", "9:50"])
    lost_movie = Movie("Lost", 342, ["8:00", "9:00", "9:50"])

    #Regular customer Jon adding a reservation
    jon = Customer("Jon", "Smith")
    jon.add_reservation(from_movie, "9:50")

    #VIP customer Jon Jon adding a reservation
    vipJon = VIPCustomer("Jon", "Jon")
    vipJon.book_private_show(from_movie, "9:50")

    #Creating the example Cinema
    cinema = Cinema()

    #Example use of the Cinema class
    cinema.add_movie(from_movie)
    cinema.add_movie(lost_movie)
    cinema.display_movies()
    cinema.add_customer(vipJon)
    cinema.add_customer(jon)
    

    #Example of how to add reservations
    for jon in cinema.customerList:
        if(type(jon) == VIPCustomer):
            jon.add_reservation(cinema.movieList[0], "9:50", False, True)
        else:
            jon.add_reservation(cinema.movieList[0], "9:50")
        jon.display_reservations()

if __name__ == "__main__":
    main()

