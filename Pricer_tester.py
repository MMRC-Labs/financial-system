import unittest

from Pricer_function import SA_Bond_pricer
#These are based on the R2040 on 22 Nov 2022 with yeild of 7.5% :https://bondcalculator.jse.co.za/BondSingle.aspx?calc=Spot

class testBondPricer(unittest.TestCase):
    
    def test_AIP(self):
        self.assertAlmostEqual(
            SA_Bond_pricer(Yeild=8,Settlement_Date='22 Nov 2022',Bond_name='R2040', Coupon=9.0,
                           Maturity_Date='31 Jan 2040', Coupon_Dates=['31 July','31 Jan'],
                           Books_Closed_Dates=['21 Jan','21 July'],Redemption_Amount=100,
                           Nominal=100,PROUND=5)['AIP'],
                           112.02160,
                           places=5
                           )

    def test_CP(self):
         self.assertAlmostEqual(
              SA_Bond_pricer(Yeild=8,Settlement_Date='22 Nov 2022',Bond_name='R2040', Coupon=9.0,
                           Maturity_Date='31 Jan 2040', Coupon_Dates=['31 July','31 Jan'],
                           Books_Closed_Dates=['21 Jan','21 July'],Redemption_Amount=100,
                           Nominal=100,PROUND=5)['CP'], 
                           109.21064,
                           places=5
                           )
    def test_daysAcc(self):
         self.assertEqual(SA_Bond_pricer(Yeild=8,Settlement_Date='22 Nov 2022',Bond_name='R2040', Coupon=9.0,
                           Maturity_Date='31 Jan 2040', Coupon_Dates=['31 July','31 Jan'],
                           Books_Closed_Dates=['21 Jan','21 July'],Redemption_Amount=100,
                           Nominal=100,PROUND=5)['DaysAcc'], 
                           114
                           )
         
    def test_Cumex(self):
         self.assertEqual(SA_Bond_pricer(Yeild=8,Settlement_Date='22 Nov 2022',Bond_name='R2040', Coupon=9.0,
                           Maturity_Date='31 Jan 2040', Coupon_Dates=['31 July','31 Jan'],
                           Books_Closed_Dates=['21 Jan','21 July'],Redemption_Amount=100,
                           Nominal=100,PROUND=5)['Cumex'], 
                           1
                           )
    def test_Delta(self):     #This being correct means that the intermediate results are also correct
        self.assertAlmostEqual(
            SA_Bond_pricer(Yeild=8,Settlement_Date='22 Nov 2022',Bond_name='R2040', Coupon=9.0,
                           Maturity_Date='31 Jan 2040', Coupon_Dates=['31 July','31 Jan'],
                           Books_Closed_Dates=['21 Jan','21 July'],Redemption_Amount=100,
                           Nominal=100,PROUND=5)['Delta'],
                           -9.877276837,
                           places=9
                           )
    def test_Duration(self):     #This being correct means that the intermediate results are also correct
        self.assertAlmostEqual(
            SA_Bond_pricer(Yeild=8,Settlement_Date='22 Nov 2022',Bond_name='R2040', Coupon=9.0,
                           Maturity_Date='31 Jan 2040', Coupon_Dates=['31 July','31 Jan'],
                           Books_Closed_Dates=['21 Jan','21 July'],Redemption_Amount=100,
                           Nominal=100,PROUND=5)['Duration'],
                           9.169988485,
                           places=9
                           )
    def test_Broken_Period(self):     #This being correct means that the intermediate results are also correct
        self.assertAlmostEqual(
            SA_Bond_pricer(Yeild=8,Settlement_Date='22 Nov 2022',Bond_name='R2040', Coupon=9.0,
                           Maturity_Date='31 Jan 2040', Coupon_Dates=['31 July','31 Jan'],
                           Books_Closed_Dates=['21 Jan','21 July'],Redemption_Amount=100,
                           Nominal=100,PROUND=5)['Broken_Period'],
                           0.380434783,
                           places=9
                           )
        

if __name__ =='__main__':
        unittest.main()

