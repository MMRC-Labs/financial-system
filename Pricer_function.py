from dateutil import parser
import datetime
import QuantLib as ql
import os

def SA_Bond_pricer(Yeild,Settlement_Date,Bond_name,Maturity_Date,Coupon_Dates, Books_Closed_Dates, Coupon,Redemption_Amount, Nominal, PROUND =5):
    #Convert dates

    Yeild_to_maturity = Yeild
    Settlement_date = Settlement_Date
    Bond = Bond_name
    Maturity_date = Maturity_Date
    Coupon = Coupon
    Coupon_dates = Coupon_Dates
    BcDates = Books_Closed_Dates
    Redemption_amount = Redemption_Amount
    PROUND = PROUND
    Nominal = Nominal

    #Maturity and settlement date
    dt = parser.parse(Settlement_date,)
    date = ql.Date(dt.day,dt.month,dt.year)
    M_b = parser.parse(Maturity_date,)
    M_b = ql.Date(M_b.day,M_b.month,M_b.year)

    #Date converter function:
    def convert_date(date_string):
        import QuantLib as ql
        from dateutil import parser
        
        temp_date = parser.parse(date_string + " " + str(dt.year),)
        temp_date = ql.Date(temp_date.day,temp_date.month,temp_date.year)
        return temp_date
    
    #Coupon and books closed dates
    Coupon_date_1 = convert_date(Coupon_dates[0])
    Coupon_date_2 = convert_date(Coupon_dates[1])
    BCD_1 = convert_date(BcDates[0])
    BCD_2 = convert_date(BcDates[1])

    #Last and next coupon dates:
    def LCD(Date,Coupon_date_1,Coupon_date_2):
        max_coupon_date = max(Coupon_date_1,Coupon_date_2)
        min_coupon_date = min(Coupon_date_1,Coupon_date_2)
        if (date.month() >= max_coupon_date.month()):
                return max_coupon_date   
        elif((date.month() < max_coupon_date.month()) and (date.month() >= min_coupon_date.month())) :
            return min_coupon_date
        else: 
            return calendar.advance(min_coupon_date,ql.Period(-6,ql.Months))
        
    #Calendar
    calendar = ql.SouthAfrica()

    last_cd = LCD(Date = date,Coupon_date_1=Coupon_date_1,Coupon_date_2=Coupon_date_2)
    next_cd = calendar.advance(last_cd,ql.Period(6,ql.Months))

    #Proximity
    bcd_use = next_cd - 10 #I should find another way to do this, maybe closest BCD to this?

    #Number of remaining coupons
    N = round((M_b-next_cd)/(365.25/2),0) 

    #Cumex
    if (date < bcd_use):
        cumex = 1
    else:
        cumex = 0  

    #DaysAccrued
    if (cumex ==1):
        daysacc = (date - last_cd)
    else:
        daysacc = (date - next_cd)

    #Coupon
    CPN = Coupon/2

    #Coupon payable on NCD
    cpn_at_ncd = CPN*cumex

    #Intermediary results

    #Semi +- annual discount factor
    F = 1/(1+Yeild_to_maturity/200)

    #Broken period
    if (next_cd != M_b):
        BP = (next_cd-date)/(next_cd - last_cd)
    else:
        BP = (next_cd-date)/(365/2)

    #Broken period discount factor
    if (next_cd != M_b):
        BPF = F**BP
    else:
        BPF = F/(F+BP*(1-F))

    #Differentials
    #The first differential of BPF with respect to F, dBPF = ∂BPF/∂F
    if (next_cd != M_b):
        dBPF = (BP*BPF)/F
    else:
        dBPF = (BP*(BPF**2))/(F**2)

    #Differentials
    #The second differential of BPF with respect to F, d2BPF = ∂2BPF/∂F2
    if (next_cd != M_b):
        d2BPF = dBPF*(BP-1)/F
    else:
        d2BPF = dBPF*(BP*BPF-F)/(F**2)

    if (F!=1):
        dCPN = CPN*(1-(N-N*F +1)*F**N)/((1-F)**2)
    else:
        dCPN = CPN*N(N**2-1)/3

    dR = N*Redemption_amount*F**(N-1)

    d2R = N*(N-1)*Redemption_amount*(F**(N-2))

    if (F!=1):
        d2CPN = CPN*(2-(N*(1-F)*(2+(N-1)*(1-F))+2*F)*(F**(N-1)))/(1-F)**3
    else:
        d2CPN = CPN*N*(N**2-1)/3

    #Results
    #Unrounded and rounded accrued interest
    accrint = (daysacc*Coupon)/365
    raccrint = round(accrint,PROUND)

    #Unrounded all-in price
    if (F!=1):
        AIP = BPF*(cpn_at_ncd+CPN*F*(1-F**N)/(1-F)+Redemption_amount*(F**N))
    else:
        AIP = cpn_at_ncd + Coupon*N + Redemption_amount

    #Unrounded clean price
    CP = AIP - accrint

    #Rounded clean price
    Rounded_CP = round(CP,PROUND)
    #Rounded All-in-price
    Rounded_AIP = Rounded_CP + raccrint 
    #Consideration

    #Interest consideration
    IntConsid = round(raccrint*Nominal/100,2)
    #All-in consideration
    All_in_Consid = round(Rounded_AIP*Nominal/100,2)
    #Clean consideration
    CleanConsid = All_in_Consid - IntConsid

    #Sensitivities
    dAIP = dBPF*AIP/BPF + BPF*(dCPN+dR)
    d2AIP = d2BPF*AIP/BPF+ dBPF*((BPF*dAIP-AIP*dBPF)/BPF**2 + dCPN + dR)+BPF*(d2CPN+d2R)
    Delta = -1*(F**2)*dAIP/200

    #Duration and complexity
    Dmod = -100*Delta/AIP
    Dur = Dmod/F
    Rand_per_point = Delta*100
    d2AIPy = (dAIP*(F**3)/2 + d2AIP*(F**4)/4)/10000
    Conv = (10000/AIP)*d2AIPy

    data = {'AIP': AIP,
            'CP' : CP,
            'All_in_Consid': All_in_Consid,
            'Clean_Consideration': CleanConsid,
            'Accrued_Int_rounded': raccrint,
            'Delta': Delta,
            'DaysAcc': daysacc,
            'Conv': Conv,
            'Rounded_AIP': Rounded_AIP,
            'Rounded_CP': Rounded_CP,
            'Cumex': cumex,
            'Duration': Dur,
            'Modified_Duration': Dmod,
            'Rand_per_Point':Rand_per_point,
            'Number_of_Coupons': N,
            'Last_CD' : last_cd,
            'Next_CD': next_cd,
            'CD_1': Coupon_date_1,
            'CD_2': Coupon_date_2,
            'BCD_1':BCD_1,
            'BCD_2': BCD_2,
            'Broken_Period': BP,
            'Broken_Period_Factor': BPF,
            'F':F,
            'Accrued_Int':accrint,
            'D2AIP': d2AIP,
            'D2R': d2R,
            'D2CPN':d2CPN,
            'DAIP':dAIP,
            'Remaining_Coupons':N,
            'Date': date
            }

    return data


# SA_Bond_pricer(Yeild=7.5, Settlement_Date='26 August 2005', Coupon= 10.5, 
#                Maturity_Date='21 Dec 2026', Coupon_Dates= ['21 June','21 Dec'], 
#                Books_Closed_Dates= ['11 June','11 December'], Redemption_Amount= 100, Nominal= 1.5e6,
#                Bond_name='R186'
#                )


# os.chdir('D:/MMRC_Labs/Pricer_Repo')
# current_directory = os.getcwd()
# print("Current Working Directory:", current_directory)

# data = SA_Bond_pricer(Yeild=7.5, Settlement_Date='26 August 2005', Coupon= 10.5, 
#                Maturity_Date='21 Dec 2026', Coupon_Dates= ['21 June','21 Dec'], 
#                 Books_Closed_Dates= ['11 June','11 December'], Redemption_Amount= 100, Nominal= 1.5e6,
#               Bond_name='R186')

# print(data['AIP'])

def convert_full_date(date_string):
    import QuantLib as ql
    from dateutil import parser
    
    temp_date = parser.parse(date_string)
    temp_date = ql.Date(temp_date.day,temp_date.month,temp_date.year)
    return temp_date


def isBD_SA(Date):
    #First convert the date
    temp_date = convert_full_date(Date)
    calendar = ql.SouthAfrica()
    is_business_day = calendar.isBusinessDay(temp_date)*1
    return is_business_day

    #Last and next coupon dates:
def LCD_SA(Settlement_Date,Coupon_date_1,Coupon_date_2):
        calendar = ql.SouthAfrica()
        max_coupon_date = max(Coupon_date_1,Coupon_date_2)
        min_coupon_date = min(Coupon_date_1,Coupon_date_2)
        if (Settlement_Date.month() >= max_coupon_date.month()):
                return max_coupon_date   
        elif((Settlement_Date.month() < max_coupon_date.month()) and (Settlement_Date.month() >= min_coupon_date.month())) :
            return min_coupon_date
        else: 
            return calendar.advance(min_coupon_date,ql.Period(-6,ql.Months))

# print(isBD_SA('25 Nov 2017')*1)

# data1 = SA_Bond_pricer(Yeild=7.5, Settlement_Date='22 Nov 2017', Coupon= 8.875, 
#                 Maturity_Date='28 Feb 2035', Coupon_Dates= ['28 Feb','31 Aug'], 
#                 Books_Closed_Dates= ['18 Feb','21 Aug'], Redemption_Amount= 100, Nominal= 100,
#                 Bond_name='R2035'
#                 )

# print("Last_CD: ",data1['Last_CD'] , "Next_CD: ", data1['Next_CD'],"Cumex=", data1['Cumex'], "AIP:", data1['AIP'])