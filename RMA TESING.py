# -*- coding: utf-8 -*-
import pandas as pd
from pandas import ExcelFile
from pandas import ExcelWriter
from datetime import datetime



def mainMenu(): # Start here
    print('### Soft for rma test ### alpha 0.3v\n')
    print('### Trying to connect to rma container file ##')
    
    ## read csf file
    
    #EXCEL_FILE = "C:/Users/Golubev/Documents/RMAFILE.xlsx"
    EXCEL_FILE = "rmatest.xlsx"
    
    df = pd.read_excel(EXCEL_FILE, sheet_name="OutERP")
    
    print("\n Succsefull parsed next index : {}".format(df.columns))
    
    #print("Choose option:\n1. Add RMA\n2. Find RMA\n\n")
    
    var_x = ""
    var_xx = ""
    
    while(var_x != "0"):
        print("\nChoose option:\n 1. Add RMA\n 2. Find RMA\n 3. Return rows of file\n 0. Exit() ")
        var_x = input(': ')
        if var_x == "1":
            add_rma(df)
            var_x = ""
        if var_x == "2":
            var_xx = input('\n 1. Fild solo SN? \n 2. Find all SN in box?\n 3. Show all boxes\n 0. Return to menu\n : ')
            df = pd.read_excel(EXCEL_FILE, sheet_name="OutERP")
            if var_xx == "1":
                SN = input('SN : ')
                search_SN(SN, df)
                var_x, var_xx = "", ""
            elif  var_xx == "2":
                BOX = input('Box : ')
                srch_all_SN_box(BOX, df)
                var_x, var_xx = "", ""
            elif var_xx == "3":
                show_boxes(df)
                var_x, var_xx = "", ""

        if var_x == "3":
            count_Len_xlx(df)
            var_x = ""    
            
def add_rma(df_temp):
    print("### Adding to file new RMA### \n")
    new_Rma = input('SN : ')
    
    while(len(new_Rma) < 6):
        new_Rma = input("##SN can not be < 6, please rewrite SN :##\n : ")
    
    Accaept_var = input('Confirm (Y/N or  y/n) : ')
    
    while not ((Accaept_var == "Y") or (Accaept_var == "N") or (Accaept_var == "y") or (Accaept_var == "n")):
        Accaept_var = input('Only Y/N input : ')
    if ((Accaept_var == "N") or (Accaept_var == "n")):
        return
    current_IB = datetime.now().date()
    #print("Last box is {}".format((df_temp['Location'][len(df_temp)])))
    new_box = input('box : ')
    
    while(len(new_box) < 5):
        new_box = input("##locator of the box can not be < 5, please rewrite box number ##\n : ")
    
    Inspect_result = input('Result of ispection\n (Write "OK" if result of instection is good)\n\n : ') 
    dfcon = pd.DataFrame({"SN":[new_Rma], "I/B date":[current_IB], "Location":[new_box], "Inspection":[Inspect_result]})
    append_df_to_excel(dfcon, EXCEL_FILE)
     
def append_df_to_excel(df_temp, excel_path):
    df_excel = pd.read_excel(excel_path)
    result = pd.concat([df_excel, df_temp], ignore_index=True)
    result.to_excel(excel_path, index=False, sheet_name='OutERP')
    global df
    df = result.copy()
    
    
def search_SN(SN, df_temp):
    for i in df_temp.index:
        if SN == df_temp['SN'][i]:
            Find = ("SN {0} inside {1} box, inspection result : {2}".format(SN, df_temp['Location'][i],df_temp['Inspection'][i]))
            Find_tr = "yes"
            break;
        else:
            Find_tr = "no"
    if Find_tr == "yes":
        print(Find)
    elif Find_tr == "no":
        print("SN is not found.") 
    QUESTION_RETURN = input('Return to menu?')
    if QUESTION_RETURN == 'N':
        exit()

def srch_all_SN_box(box, df_temp):
    Sn_Box_list = []
    n = 0
    for i in df_temp.index:
        if box == df_temp['Location'][i]:
            n += 1
            Sn_Box_list.append("{3}# SN {0} inside {1} box, inspection : {2}".format(df_temp['SN'][i], box, df_temp['Inspection'][i], n))
            #print("SN {0} inside {1} box".format(df_temp['SN'][i],box))
        
    if len(Sn_Box_list) <= 0:
        print("Mathes not found...")
    else:
        for i in range(len(Sn_Box_list)):
            print(Sn_Box_list[i]) 
            
def show_boxes(df_temp):
    boxes_list = []
    for i in df_temp.index:
        if df_temp['Location'][i] not in boxes_list:
            boxes_list.append(df_temp['Location'][i])
    boxes_list = [x for x in boxes_list if str(x) != 'nan']
    print("\n Current boxes : \n ")
    boxes_list = sorted(boxes_list)
    
    print("\n###    All boxes    ###\n")
    for i in range(len(boxes_list)):
        print(boxes_list[i])
    print("\n###    END    ###\n")

    #Отлов индексов 2019R в строке
    #Отлов остальных...
    aidelist = []; doctorSrlist = []; InjSrlist = []; MbSrlist = []; OrionSrlist = []
    
    #aidelist.copy(boxes_list)
    for i in range(len(boxes_list)):
        indexR = boxes_list[i].find("2019R")
        indexRD = boxes_list[i].find("2019RD")
        indexRI = boxes_list[i].find("2019RI")
        indexRM = boxes_list[i].find("2019RM")
        indexRO = boxes_list[i].find("2019RO")
        
        if ((indexR > -1) and (indexRD == -1) and (indexRI == -1) and (indexRM == -1) and (indexRO == -1)):
            aidelist.append(boxes_list[i])
        elif ((indexR > -1) and (indexRD > -1) and (indexRI == -1) and (indexRM == -1) and (indexRO == -1)):
            doctorSrlist.append(boxes_list[i])
        elif ((indexR > -1) and (indexRD == -1) and (indexRI > -1) and (indexRM == -1) and (indexRO == -1)):
            InjSrlist.append(boxes_list[i])
        elif ((indexR > -1) and (indexRD == -1) and (indexRI == -1) and (indexRM > -1) and (indexRO == -1)):
            MbSrlist.append(boxes_list[i])
        elif ((indexR > -1) and (indexRD == -1) and (indexRI == -1) and (indexRM == -1) and (indexRO > -1)):
            OrionSrlist.append(boxes_list[i])
    
    print("\n###    FROM AIDE    ###\n")
    for i in range(len(aidelist)):
        print(aidelist[i])
    print("\n###    END AIDE    ###")
    
    print("\n###    FROM DR service    ###\n")
    for i in range(len(doctorSrlist)):
        print(doctorSrlist[i])
    print("\n###    END DR service    ###")
    
    print("\n###    FROM Inj service    ###\n")
    for i in range(len(InjSrlist)):
        print(InjSrlist[i])
    print("\n###    END Inj service    ###")
    
    print("\n###    FROM Mobile service    ###\n")
    for i in range(len(MbSrlist)):
        print(MbSrlist[i])
    print("\n###    END Mobile service    ###")
    
    print("\n###    FROM Orion service    ###\n")
    for i in range(len(OrionSrlist)):
        print(OrionSrlist[i])    
    print("\n###    END Orion service    ###")

def count_Len_xlx(df_temp):
    print("\nRows in file : {}".format(len(df_temp)))
    
mainMenu()