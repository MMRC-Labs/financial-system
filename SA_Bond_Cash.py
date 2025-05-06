#SA bond cashflows

#This function takes an SA bond object and then projects cashflows

from SA_Bond_Object import SA_Bond
from Pricer_function import convert_full_date,LCD_SA
import QuantLib as ql, numpy as np, pandas as pd

def convert_date(date_string, Year):
    import QuantLib as ql
    from dateutil import parser
        
    temp_date = parser.parse(date_string + " " + str(Year),)
    temp_date = ql.Date(temp_date.day,temp_date.month,temp_date.year)
    return temp_date

def generate_coupon_dates(Next_Coupon_Date,Bond_Object):
    calendar = ql.SouthAfrica()
    # Define the business day convention
    business_day_convention = ql.ModifiedFollowing
    coupon_dates = []
    current_date = convert_full_date(Next_Coupon_Date)
    Mat_date = convert_full_date(Bond_Object.maturity_date)
    
    while current_date <= Mat_date:
        coupon_dates.append(current_date)
        current_date = calendar.advance(current_date,ql.Period(6,ql.Months),business_day_convention)
        
    # if current_date == Bond_Object.maturity_date: 
    #     coupon_dates.append(Bond_Object.maturity_date)
    
    return coupon_dates


def project_cash(Date, Bond_Object):
    Settlement_Date = convert_full_date(Date) #Probably unnecessary, but ensures date is date

    Coupon_dates = Bond_Object.coupon_dates
    #Coupon, maturity and books closed dates
    Coupon_date_1 = convert_date(Coupon_dates[0], Year= Settlement_Date.year())
    Coupon_date_2 = convert_date(Coupon_dates[1], Year= Settlement_Date.year())
    M_b = convert_full_date(Bond_Object.maturity_date)

    #define calendar
    calendar = ql.SouthAfrica()

    last_cd = LCD_SA(Settlement_Date = Settlement_Date,Coupon_date_1=Coupon_date_1,Coupon_date_2=Coupon_date_2)
    next_cd = calendar.advance(last_cd,ql.Period(6,ql.Months))

    #Proximity
    bcd_use = next_cd - 10 #I should find another way to do this, maybe closest BCD to this?

    #Number of remaining coupons
    N = round((M_b-next_cd)/(365.25/2),0) 

    #Cumex
    if (Settlement_Date < bcd_use):
        cumex = 1
    else:
        cumex = 0 

    #Coupon
    CPN = Bond_Object.coupon*Bond_Object.nominal/200 #We want actual cashflows because coupon is not expressed as a percentage in the bond definition

    #Coupon payable on NCD
    cpn_at_ncd = CPN*cumex

    #Coupon dates from coupon generator:
    coupon_dates = generate_coupon_dates(next_cd,Bond_Object=Bond_Object)

    #Cashflows
    cashflows = np.full(N,CPN)
    #Add redemption for last payment
    cashflows[-1] += Bond_Object.redemption

    df = pd.dataframe({
        'Date': np.arange(1,N+1),
        'Cashflow': cashflows
    })

    return df

bond1 = SA_Bond(name="R186",nominal=100, maturity_date="21 Dec 2026",coupon_dates=["21 June","21 Dec"], 
                books_closed_dates=["11 June","11 Dec"],redemption=100, coupon=10.5, coupon_frequency=2)
bond2 = SA_Bond(name="R186",nominal=100, maturity_date="31 Jan 2040",coupon_dates=["31 Jan","31 July"], 
                books_closed_dates=["21 July","21 Jan"],redemption=100, coupon=9.0, coupon_frequency=2)

test = generate_coupon_dates(Next_Coupon_Date="21 June 2024",Bond_Object=bond1)
test1 = generate_coupon_dates(Next_Coupon_Date="31 Jan 2024",Bond_Object=bond2)
test3 = project_cash(Date="21 June 2024",Bond_Object=bond1)

#test2 = convert_date("21 Jan", 2024)
# test4 = convert_full_date("31 Jan 2024")

#print(test2.month())

#print(bond1.maturity_date)







    




