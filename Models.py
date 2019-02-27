from AssumedVariables import *
from math import *

# Sales Volume
class SalesVolume():
  def __init__(self, Target_OD_Shops=100, Prior_Year_OD_Retention_Rate=100, Pcnt_Relationship_Wins=10):
    self.Target_OD_Shops = Target_OD_Shops # #
    self.Pcnt_Relationship_Wins = Pcnt_Relationship_Wins # %
    self.Prior_Year_OD_Retention_Rate = Prior_Year_OD_Retention_Rate # 100%
    self.Median_Num_Doors_per_Target = 20
    self.Median_Num_Patients_per_Day = 25
    self.Days_in_Month = 24
    self.Pcnt_Walkers_try_Platform = 20 # % Walkers Try Platform

    self.Pcnt_Eyeglass = Pcnt_Patients_who_need_eyeglasses # % Eyeglass
    self.Pcnt_Patients_that_Walk = Pcnt_of_Walkers # % Patients that Walk

  def calc_sales(self):

    self.Total_NEW_DK_OD_Market = self.Pcnt_Relationship_Wins * self.Target_OD_Shops * self.Prior_Year_OD_Retention_Rate # =F27*F26*F28

    self.Total_New_Patients_per_OD = self.Total_NEW_DK_OD_Market * \
                                     self.Median_Num_Doors_per_Target * \
                                     self.Median_Num_Patients_per_Day * \
                                     self.Days_in_Month * 12 # F33 = F29*F30*F31*F32*12

    self.Total_Platform_Customer_Base = self.Total_New_Patients_per_OD # F34 = F33

    self.Total_OD_Doors = floor(self.Total_Platform_Customer_Base / # F35 = ROUNDDOWN(F34/(F31*F32*12),0)
                                (self.Median_Num_Patients_per_Day * self.Days_in_Month * 12))

    self.Annual_DK_Patient_Market = self.Total_Platform_Customer_Base * \
                                    self.Pcnt_Eyeglass * \
                                    self.Pcnt_Patients_that_Walk # F38 = F34*F36*F37

    self.Customers_who_Try_DK_Platform = self.Annual_DK_Patient_Market * self.Pcnt_Walkers_try_Platform # F40 =F38*F39
    self.Num_of_trials = self.Annual_DK_Patient_Market * \
                    self.Pcnt_Walkers_try_Platform * \
                    Avg_Customer_Trials # F41 = F38*F39*$C$27
    self.Capture_rate = DK_Conversion # F42
    self.Total_Customers = self.Capture_rate * self.Customers_who_Try_DK_Platform # F43 =F42*F40


# Annual Costs
class AnnualCosts(SalesVolume):
  def __init__(self,
               New_OD_Sales=25e4,          OD_Retention=1e5,
               End_Consumer_Marketing_Q=0, Other_SGnA=3e5,   Warehouse_Costs=0):

    self.New_OD_Sales             = New_OD_Sales
    self.OD_Retention             = OD_Retention
    self.End_Consumer_Marketing_Q = End_Consumer_Marketing_Q
    self.Other_SGnA               = Other_SGnA
    self.Warehouse_Costs          = Warehouse_Costs

  def next_annual_costs(self):

    self.New_OD_Sales = New_OD_Door_Acq_Cost * (self.Target_OD_Shops * self.Median_Num_Doors_per_Target) # F7 = $C$15*(G26*G30)
    self.OD_Retention = Retension_Support * self.Total_NEW_DK_OD_Market # F8 = $C$22*G29

    # End-Consumer Marketing?
    self.Other_SGnA = (self.Other_SGnA / self.New_OD_Sales) * self.New_OD_Sales # F10 = ($F$10/$F$7)*G7

    self.Customer_Service_Reps = round(self.Num_of_trials/(Daily_Customer_Service_Hours *
                                                          Num_Trials_per_Customer_Service_per_hr *
                                                          Days_per_week_per_Staff *
                                                          Staff_Working_Weeks_a_Year),1) # F12 =ROUNDUP(F41/($C$17*$C$18*$C$19*$C$20),1)
    self.Total_Customer_Service_Costs = self.Total_Customer_Service_Costs * \
                                        Cost_per_hr_for_Customer_Service * \
                                        Daily_Customer_Service_Hours * \
                                        Days_per_week_per_Staff * 52 # F13 =F12*$C$16*$C$17*$C$19*52
    self.Trial_Inventory_Build = Cost_per_Trial_Frame * self.Num_of_trials / Uses_of_Trail_Frame # F14 =(F41/$C$29)*$C$28

    self.AC_Total = self.New_OD_Sales + \
                    self.OD_Retention + \
                    self.End_Consumer_Marketing_Q + \
                    self.Other_SGnA + \
                    self.Warehouse_Costs + \
                    self.Customer_Service_Reps + \
                    self.Total_Customer_Service_Costs + \
                    self.Trial_Inventory_Build


# Technical Dev & Maintenance
class TechDevMaintenance(AnnualCosts):
  def __init__(self,
               Client_Channel_Business_Rules=5e4, Site_Dev_per_Enhancement="?",
               Algorithm_Development=25e4,        IT_Infrastructure_Maintenance=3e5,
               Amplified_Expertise=1e5):

    self.Client_Channel_Business_Rules = Client_Channel_Business_Rules
    self.Site_Dev_per_Enhancement      = Site_Dev_per_Enhancement
    self.Algorithm_Development         = Algorithm_Development
    self.IT_Infrastructure_Maintenance = IT_Infrastructure_Maintenance
    self.Amplified_Expertise           = Amplified_Expertise
    self.TDV_Total = Client_Channel_Business_Rules + Site_Dev_per_Enhancement + \
                     Algorithm_Development + IT_Infrastructure_Maintenance + Amplified_Expertise
    self.Total_Annual_Overhead_Costs = self.TDV_Total + self.AC_Total # F23 = F22 + F15


# OD Onboarding Per Door
class ODOnboarding(TechDevMaintenance):
  def __init__(self):
    self.OD_Training = self.Total_NEW_DK_OD_Market * self.Median_Num_Doors_per_Target * OD_Support_Training # F46 =(F29*F30)*$C$42
    self.OD_Setup    = self.Total_NEW_DK_OD_Market * self.Median_Num_Doors_per_Target * OD_Support_Setup    # F47 =F29*F30*$C$43
    self.Total_OD_Onboarding_Costs = self.OD_Training + self.OD_Setup

    # DK Platform Revenue
    self.Revenue_from_OD  = self.Total_OD_Doors * Per_Door_Licensing_Fee_per_Mo * 12 # F51 =F35*$C$11*12
    self.Purchase_Bonus   = self.Total_Customers * DK_Purchase_Bonus # F52 =F43*$C$12
    self.Total_DK_Revenue = self.Revenue_from_OD + self.Purchase_Bonus


# Trial Variable Costs/Revenue
class