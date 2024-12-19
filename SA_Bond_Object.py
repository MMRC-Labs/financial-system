class SA_Bond:
    def __init__(self, name, nominal, redemption, coupon, coupon_frequency, maturity_date, coupon_dates, books_closed_dates):
         self.name = name
         self.redemption = redemption
         self.nominal = nominal
         self.coupon = coupon 
         self.maturity_date = maturity_date
         self.coupon_dates = coupon_dates
         self.books_closed_dates = books_closed_dates
         self.coupon_frequency = coupon_frequency
   
    def calculate_coupon_rate(self):
     return self.coupon/self.coupon_frequency
    
    def __str__(self):
       return f"Bond(name={self.name}, face_value={self.nominal}, coupon_rate={self.coupon}, maturity_date={self.maturity_date})"
    
# bond1 = SA_Bond(name="R186",nominal=100, maturity_date="21 Dec 2026",coupon_dates=["21 June","21 Dec"], 
#                 books_closed_dates=["11 June","11 Dec"],redemption=100, coupon=10.5, coupon_frequency=2)

# print(bond1.books_closed_dates)