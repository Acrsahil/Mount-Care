from tkinter import *
from tkinter import messagebox
import nepali_datetime
from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import PatternFill, Border, Side, Alignment, Protection, Font,numbers
import random,os
from tkinter import END
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from win32com import client
from ttkbootstrap import Style
import ttkbootstrap as ttk
import amounttowords



if not os.path.exists('billno.txt'):
    with open("billno.txt","w+") as f:
        f.write('1')
else:
    with open("billno.txt","r+") as f:
        billno =  f.read()
        billno = int(billno)
        with open("billno.txt","w") as fl:
            updatebill = billno+1
            update_bill = fl.write(str(updatebill))




today = str(nepali_datetime.date.today())

if not os.path.exists('bills'):
    os.mkdir('bills')

if not os.path.exists('bills'):
    os.mkdir('PDFbills')

wb = load_workbook('brocode.xlsx')
ws = wb.active 

pricelist = {
    "Alovera": 760,
    "Asparagus": 960,
    "Cordyceps": 2090,
    "Flex Seed": 1140,
    "Ganoderma": 1425,
    "Ginseng": 1805,
    "Graps Seed": 1335,
    "Java Plum": 1045,
    "Moringa Leaf": 1045,
    "Safed Musli": 1140,
    "Wood Apple": 950,
    "All Purpose Cream": 617.5,
    "Black Shampoo": 617.5,
    "External Cream": 950,
    "Gilsering Cream": 95,
    "Hair Oil": 570,
    "Mount Shampoo": 475,
    "Shine Cream": 950,
    "Soap": 142,
    "Body Oil": 475,
    "Gastrina": 250,
    "Herbal Paak": 1710,
    "Immunity Paak": 1568,
    "Paste": 200,
    "Sadabahar Tea": 475,
    "Tooth Powder": 523
}


def make_pdf():
    try:
        global billno
        app = client.DispatchEx("Excel.Application")
        app.Interactive = False
        app.Visible = False
        app.DisplayAlerts = False  # 🚫 Prevents prompts like "Do you want to save?"

        file = r"C:\Users\archlinux\Desktop\Mount-Care\brocode.xlsx"
        excel_dir = os.path.dirname(file)

        billno = str(billno)
        billdir = "PDFbills/"
        billno += ".pdf"
        billdir += billno

        pdf_file_path = os.path.join(excel_dir, billdir)

        if not os.path.exists(os.path.dirname(pdf_file_path)):
            os.makedirs(os.path.dirname(pdf_file_path))

        workbook = app.Workbooks.Open(file)
        sheet = workbook.ActiveSheet

        # ✅ Fit to one page without zooming out too much
        sheet.PageSetup.Zoom = False
        sheet.PageSetup.FitToPagesWide = 1
        sheet.PageSetup.FitToPagesTall = 1

        # ✅ Center content horizontally

        sheet.ExportAsFixedFormat(0, pdf_file_path)

        workbook.Close(SaveChanges=False)  # 🔐 Don't save changes

        print("Successfully converted to PDF!")

    except Exception as e:
        print("Error:", e)



def send_email():
    pass

def print_bill():
    pass

#Search Function
def search_bill():
    for i in os.listdir('bills/'):
        if i.split('.')[0] == BillEntry.get():
            f = open(f'bills/{i}','r')
            textarea.delete(1.0,END)
            for data in f:
                textarea.insert(END,data)
            f.close()
            break
    else:
        messagebox.showerror("Error",'Invalid Bill Number')

def reverse_bill():
    st = start
    ws.delete_rows(st,mainbillcnt)

    ofst = 22
    ws.delete_rows(ofst,offerbillcnt)


def write_to_excel():
    # Main Bill
    temp = []
    Otemp = []

    global start,end,Ostart,Oend
    start = 13
    end = 13+mainbillcnt
    print("this is end->",end)


    total = end+1
    discount = end+2
    amtpay = end+3

    for product, qty in mainbill_qty.items():
        temp.append(product)
    for product, qty in offer_qty.items():
        Otemp.append(product)

    
    top = Side(border_style='thin')
    buttom = Side(border_style='thin')
    right = Side(border_style='thin')
    left = Side(border_style='thin')

    border = Border(top=top,right=right,bottom=buttom,left=left)

    alignment = Alignment(horizontal='center',shrink_to_fit=True)
    shrink = Alignment(shrink_to_fit=True)
        
    i = 0
    row = start
    while row < end+1 and i<len(temp):
        ws.insert_rows(row)

        ws['C'+str(row)] = i+1
        ws['D'+str(row)] = temp[i]
        ws['E'+str(row)] = mainbill_qty[temp[i]]
        ws['F'+str(row)] = pricelist[temp[i]]
        ws['G'+str(row)] = mainbill_tprice[temp[i]]

        ws['E'+str(row)].alignment = alignment
        ws['F'+str(row)].alignment = shrink
        ws['G'+str(row)].alignment = shrink

        ws['C'+str(row)].font = Font(bold=True,size=14)
        ws['D'+str(row)].font = Font(bold=True,size=14)
        ws['E'+str(row)].font = Font(bold=True,size=14)
        ws['F'+str(row)].font = Font(bold=True,size=14)
        ws['G'+str(row)].font = Font(bold=True,size=14)

        ws['B'+str(row)].fill = PatternFill(fill_type= 'solid',start_color='9c2c95')
        ws['C'+str(row)].fill = PatternFill(fill_type= 'solid',start_color='9c2c95')
        ws['D'+str(row)].fill = PatternFill(fill_type= 'solid',start_color='9c2c95')
        ws['E'+str(row)].fill = PatternFill(fill_type= 'solid',start_color='9c2c95')
        ws['F'+str(row)].fill = PatternFill(fill_type= 'solid',start_color='9c2c95')
        ws['G'+str(row)].fill = PatternFill(fill_type= 'solid',start_color='9c2c95')
        ws['H'+str(row)].fill = PatternFill(fill_type= 'solid',start_color='9c2c95')

        ws['C'+str(row)].border = border
        ws['D'+str(row)].border = border
        ws['E'+str(row)].border = border
        ws['F'+str(row)].border = border
        ws['G'+str(row)].border = border


        i+=1
        row+=1
    print(mainbillcnt)

    ws['G'+str(total)] = Totals
    ws['G'+str(discount)] = Discounts
    ws['G'+str(amtpay)] = Amountpays
    print(type(Amountpay))
    words = amounttowords.number_to_words(int(float(Amountpay)))

    if len(words)>=44:
        temp = words
        ans = ""
        lsts = words.split() #"sahil is a bad boy" "sahil is"
        while len(temp)>=44:
            ans = lsts.pop() + " " + ans
            temp = " ".join(lsts)
        ws['E'+str(amtpay+1)] = temp
        ws['E'+str(amtpay+2)] = ans
    else:
        ws['E'+str(amtpay+1)] = words




    total = end
    discount = end
    amtpay = end+1

    


def save_bill():
    result = messagebox.askyesno('Confirm','Do you want to save the bill?')
    if result:
        bill_content = textarea.get(1.0,END)
        file = open(f'bills/{billno}.txt','w')
        file.write(bill_content)
        file.close()
        messagebox.showinfo(f'Sucess,{billno} is saved sucessfully')
        wb.save('brocode.xlsx')



#writing in excel file

ws['E7'].value = billno
print("hey")

def bill_area():
    if nameEntry.get()=='' or MoidEntry.get() == '' or dealerEntry.get() == '' or sdealerEntry.get() == '' or AddressEntry.get() == '':
        messagebox.showerror('Error','Customer Detail Are Required!')
    elif TotalEntry.get() == '':
        messagebox.showerror('No Product Are Selected!')
    elif TotalEntry.get() == '0':
        messagebox.showerror('No Product Are Selected!')
    elif TotalEntry1.get() == '' or TotalEntry1.get() =='0.0':
        messagebox.showerror('No Offer Product Are Selected!')
    else:
        textarea.delete(1.0,END)
        textarea.insert(END,'\t*** Mount Care International Pvt Ltd ***\n')
        textarea.insert(END,'\t\tKathmandu-3, Maharajung Chok \n')
        textarea.insert(END,'\t    Phone Number : 9851177355,9823681553 \n')
        textarea.insert(END,f'\n  Bill Number :\t {billno:>17}')
        textarea.insert(END,f'\n  Customer Name :\t {nameEntry.get():>15}')
        textarea.insert(END,f'\n  Customer Id :\t {MoidEntry.get():>17}')
        textarea.insert(END,f'\n  Customer Address :\t {AddressEntry.get():>12}\n')
        textarea.insert(END,f'\n  ====================================================== ')
        textarea.insert(END,f'\n  Product    \t\t\tQuantity                \t\t\tPrice')
        textarea.insert(END,f'\n  ====================================================== ')

        ws['E9'].value = MoidEntry.get() #Customer ID
        ws['E8'].value = nameEntry.get() #Customer Name
        ws['E10'].value = AddressEntry.get() #Customer Address
        ws['G7'].value = today # Date
        
        global mainbillcnt,offerbillcnt,mainbill_qty,mainbill_tprice
        mainbill_tprice = {} # Store the Price of the Product Inserted by Input Field
        mainbill_qty = {} # Store the Quantity of the product

        mainbillcnt = 0 # Entry in product in Main
        offerbillcnt = 0 # Entry of Product in Offer

        #food supplement
        if AloveraEntry.get() != '0':
            mainbillcnt += 1
            textarea.insert(END, f'\n  Alovera\t\t{AloveraEntry.get():>13}  {aloveraprice:>25}')
            mainbill_qty["Alovera"] = AloveraEntry.get() #Product and qty
            mainbill_tprice["Alovera"] = aloveraprice # Product and price

        if AsparagusEntry.get() != '0':
            mainbillcnt += 1
            textarea.insert(END, f'\n  Asparagus\t\t{AsparagusEntry.get():>13}  {asparagusprice:>25}')
            mainbill_qty["Asparagus"] = AsparagusEntry.get() #Product and qty
            mainbill_tprice["Asparagus"] = asparagusprice # Product and price

        if CordycepsEntry.get() != '0':
            mainbillcnt += 1
            textarea.insert(END, f'\n  Cordyceps\t\t{CordycepsEntry.get():>13}  {cordycepsprice:>25}')
            mainbill_qty["Cordyceps"] = CordycepsEntry.get() #Product and qty
            mainbill_tprice["Cordyceps"] = cordycepsprice # Product and price

        if FlexseedEntry.get() != '0':
            mainbillcnt += 1
            textarea.insert(END, f'\n  Cordyceps\t\t{FlexseedEntry.get():>13}  {flexseedprice:>25}')
            mainbill_qty["Flex Seed"] = FlexseedEntry.get() #Product and qty
            mainbill_tprice["Flex Seed"] = flexseedprice # Product and price

        if GanodermaEntry.get() != '0':
            mainbillcnt += 1
            textarea.insert(END, f'\n  Ganoderma\t\t{GanodermaEntry.get():>13}  {ganodermaprice:>25}')
            mainbill_qty["Ganoderma"] = GanodermaEntry.get() #Product and qty
            mainbill_tprice["Ganoderma"] = ganodermaprice # Product and price
        if GinsengEntry.get() != '0':
            mainbillcnt += 1
            textarea.insert(END, f'\n  Ginseng\t\t{GinsengEntry.get():>13}  {ginsengprice:>25}')
            mainbill_qty["Ginseng"] = GinsengEntry.get() #Product and qty
            mainbill_tprice["Ginseng"] = ginsengprice # Product and price
        if GrapsseedEntry.get() != '0':
            mainbillcnt += 1
            textarea.insert(END, f'\n  Graps Seed\t\t{GrapsseedEntry.get():>13}  {grapsseedprice:>25}')
            mainbill_qty["Graps Seed"] = GrapsseedEntry.get() #Product and qty
            mainbill_tprice["Graps Seed"] = grapsseedprice # Product and price
        if JavaplumEntry.get() != '0':
            mainbillcnt += 1
            textarea.insert(END, f'\n  Java Plum\t\t{JavaplumEntry.get():>13}  {javaplumprice:>25}')
            mainbill_qty["Java Plum"] = JavaplumEntry.get() #Product and qty
            mainbill_tprice["Java Plum"] = javaplumprice # Product and price
        if MoringaleafEntry.get() != '0':
            mainbillcnt += 1
            textarea.insert(END, f'\n  Moringa Leaf\t\t{MoringaleafEntry.get():>13}  {moringaleafprice:>25}')
            mainbill_qty["Moringa Leaf"] = MoringaleafEntry.get() #Product and qty
            mainbill_tprice["Moringa Leaf"] = moringaleafprice # Product and price
        if SafedmusliEntry.get() != '0' and SafedmusliEntry.get() != "" and SafedmusliEntry != type('a'):
            mainbillcnt += 1
            textarea.insert(END, f'\n  Safed Musli\t\t{SafedmusliEntry.get():>13}  {safedmusliprice:>25}')
            mainbill_qty["Safed Musli"] = SafedmusliEntry.get() #Product and qty
            mainbill_tprice["Safed Musli"] = safedmusliprice # Product and price
        if WoodappleEntry.get() != '0':
            mainbillcnt += 1
            textarea.insert(END, f'\n  Wood Apple\t\t{WoodappleEntry.get():>13}  {woodappleprice:>25}')
            mainbill_qty["Wood Apple"] = WoodappleEntry.get() #Product and qty
            mainbill_tprice["Wood Apple"] = woodappleprice # Product and price
        

        #Cosmetic
        if AllpurposecreamEntry.get() != '0':
            mainbillcnt += 1
            textarea.insert(END, f'\n  All Purpose Cream\t{AllpurposecreamEntry.get():>9}  {allpurposecreamprice:>25}')
            mainbill_qty["All Purpose Cream"] = AllpurposecreamEntry.get() #Product and qty
            mainbill_tprice["All Purpose Cream"] = allpurposecreamprice # Product and price
        if BlackshampooEntry.get() != '0':
            mainbillcnt += 1
            textarea.insert(END, f'\n  Black Shampoo\t\t{BlackshampooEntry.get():>12}  {balckshampooprice:>25}')
            mainbill_qty["Black Shampoo"] = BlackshampooEntry.get() #Product and qty
            mainbill_tprice["Black Shampoo"] = balckshampooprice # Product and price
        if ExternalcreamEntry.get() != '0':
            mainbillcnt += 1
            textarea.insert(END, f'\n  External Cream\t\t{ExternalcreamEntry.get():>11}  {externalcreamprice:>25}')
            mainbill_qty["External Cream"] = ExternalcreamEntry.get() #Product and qty
            mainbill_tprice["External Cream"] = externalcreamprice # Product and price
        if GilseringcreamEntry.get() != '0':
            mainbillcnt += 1
            textarea.insert(END, f'\n  Gilsering Cream\t\t{GilseringcreamEntry.get():>10}  {gilseringcreamprice:>25}')
            mainbill_qty["Gilsering Cream"] = GilseringcreamEntry.get() #Product and qty
            mainbill_tprice["Gilsering Cream"] = gilseringcreamprice # Product and price
        if HairoilEntry.get() != '0':
            mainbillcnt += 1
            textarea.insert(END, f'\n  Hair Oil\t\t{HairoilEntry.get():>13}  {hairoilprice:>25}')
            mainbill_qty["Hair Oil"] = HairoilEntry.get() #Product and qty
            mainbill_tprice["Hair Oil"] = hairoilprice # Product and price
        if MountshampoocreamEntry.get() != '0':
            mainbillcnt += 1
            textarea.insert(END, f'\n  Mountcare Shampoo\t\t{MountshampoocreamEntry.get():>8}  {mountshampooprice:>25}')
            mainbill_qty["Mount Shampoo"] = MountshampoocreamEntry.get() #Product and qty
            mainbill_tprice["Mount Shampoo"] = mountshampooprice # Product and price
        if ShinecreamEntry.get() != '0':
            mainbill_qty["Shine Cream"] = ShinecreamEntry.get() #Product and qty
            mainbill_tprice["Shine Cream"] = shinecreamprice # Product and price
            mainbillcnt += 1
            textarea.insert(END, f'\n  Shine Cream\t\t{ShinecreamEntry.get():>13}  {shinecreamprice:>25}')
        if SoapEntry.get() != '0':
            mainbill_qty["Soap"] = SoapEntry.get() #Product and qty
            mainbill_tprice["Soap"] = soapprice # Product and price
            mainbillcnt += 1
            textarea.insert(END, f'\n  Soap\t\t{SoapEntry.get():>13}  {soapprice:>25}')

        #Beverage
        if BodyoilEntry.get() != '0':
            mainbillcnt += 1
            textarea.insert(END, f'\n  Body Oil\t\t{BodyoilEntry.get():>13}  {bodyoilprice:>25}')
            mainbill_qty["Body Oil"] = BodyoilEntry.get() #Product and qty
            mainbill_tprice["Body Oil"] = bodyoilprice # Product and price
        if GastrinaEntry.get() != '0':
            mainbillcnt += 1
            textarea.insert(END, f'\n  Gastrina\t\t{GastrinaEntry.get():>13}  {gastrinaprice:>25}')
            mainbill_qty["Gastrina"] = GastrinaEntry.get() #Product and qty
            mainbill_tprice["Gastrina"] = gastrinaprice # Product and price
        if herbalpaakEntry.get() != '0':
            mainbillcnt += 1
            textarea.insert(END, f'\n  Herbal Paak\t\t{herbalpaakEntry.get():>13}  {herbalpaakprice:>25}')
            mainbill_qty["Herbal Paak"] = herbalpaakEntry.get() #Product and qty
            mainbill_tprice["Herbal Paak"] = herbalpaakprice # Product and price
        if ImmunitypaakEntry.get() != '0':
            mainbillcnt += 1
            textarea.insert(END, f'\n  Immunity Paak\t\t{ImmunitypaakEntry.get():>12}  {immunitypaakprice:>25}')
            mainbill_qty["Immunity Paak"] = ImmunitypaakEntry.get() #Product and qty
            mainbill_tprice["Immunity Paak"] = immunitypaakprice # Product and price
        if PasteEntry.get() != '0':
            mainbillcnt += 1
            textarea.insert(END, f'\n  Paste\t\t{PasteEntry.get():>13}  {pasteprice:>25}')
            mainbill_qty["Paste"] = PasteEntry.get() #Product and qty
            mainbill_tprice["Paste"] = pasteprice # Product and price
        if SadabaharteaEntry.get() != '0':
            mainbillcnt += 1
            textarea.insert(END, f'\n  Sadabahar Tea\t\t{SadabaharteaEntry.get():>12}  {sadabaharteaprice:>25}')
            mainbill_qty["Sadabahar Tea"] = SadabaharteaEntry.get() #Product and qty
            mainbill_tprice["Sadabahar Tea"] = sadabaharteaprice # Product and price
        if ToothpowderEntry.get() != '0':
            mainbillcnt += 1
            textarea.insert(END, f'\n  Tooth Powder\t\t{ToothpowderEntry.get():>13}  {toothpowderprice:>25}')
            mainbill_qty["Tooth Powder"] = ToothpowderEntry.get() #Product and qty
            mainbill_tprice["Tooth Powder"] = toothpowderprice # Product and price
        textarea.insert(END,f'\n  ------------------------------------------------------')

        global Totals,Offers,Discounts,Amountpays,Amountpay

        Totals = TotalEntry.get()
        Offers = OfferEntry.get()
        Discounts = DiscountEntry.get()
        Amountpay = AmountpayableEntry.get()


        Totals = "Rs " + Totals
        Offers = "Rs " + Offers
        Discounts = "Rs " + Discounts
        Amountpays = "Rs "+ Amountpay


        
        textarea.insert(END,"\n")
        textarea.insert(END,f'\n  Total Amount  \t\t     {Totals:>24}')
        textarea.insert(END,f'\n  Offer  \t\t     {Offers:>25}')
        textarea.insert(END,f'\n  Discount  \t\t     {Discounts:>25}\n')
        textarea.insert(END,f'\n  Amount Payable  \t\t     {Amountpays:>22}')

        textarea.insert(END,'\n\t\t### Offer Products ###\n')
        textarea.insert(END,f'\n  ====================================================== ')
        textarea.insert(END,f'\n  Product    \t\t\tQuantity\n')
        textarea.insert(END,f'\n  ====================================================== ')

        for product,qty in offer_qty.items():
            if qty>0:
                offerbillcnt+=1
                textarea.insert(END, f'\n  {product}  {qty:>20}')

        print(mainbill_qty)
        print(offer_qty)
        write_to_excel()
        save_bill()
        make_pdf()
        ws['E'+str(end+5)] = '=""'
        reverse_bill()
        wb.save('brocode.xlsx')





def update_total_discount(event=None):
    # Call your existing total function to recalculate the total and discount
    total()
def total():
    # food supplement price calculation

    global aloveraprice,asparagusprice,cordycepsprice,flexseedprice,ganodermaprice,ginsengprice,grapsseedprice,javaplumprice,moringaleafprice,safedmusliprice,woodappleprice
    global allpurposecreamprice,balckshampooprice,externalcreamprice,gilseringcreamprice,hairoilprice,mountshampooprice,shinecreamprice,soapprice
    global bodyoilprice,gastrinaprice,herbalpaakprice,immunitypaakprice,pasteprice,sadabaharteaprice,toothpowderprice

    aloveraprice = float(AloveraEntry.get())*760
    asparagusprice = float(AsparagusEntry.get())*960
    cordycepsprice = float(CordycepsEntry.get())*2090
    flexseedprice = float(FlexseedEntry.get())*1140
    ganodermaprice = float(GanodermaEntry.get())*1425
    ginsengprice = float(GinsengEntry.get())*1805
    grapsseedprice = float(GrapsseedEntry.get())*1335
    javaplumprice = float(JavaplumEntry.get())*1045
    moringaleafprice = float(MoringaleafEntry.get())*1045
    safedmusliprice = float(SafedmusliEntry.get())*1140
    woodappleprice = float(WoodappleEntry.get())*950


    #Cosmetic item
    allpurposecreamprice = float(AllpurposecreamEntry.get())*617.5
    balckshampooprice = float(BlackshampooEntry.get())*617.5  
    externalcreamprice = float(ExternalcreamEntry.get())*950
    gilseringcreamprice = float(GilseringcreamEntry.get())*95
    hairoilprice = float(HairoilEntry.get())*570
    mountshampooprice = float(MountshampoocreamEntry.get())*475
    shinecreamprice = float(ShinecreamEntry.get())*950
    soapprice = float(SoapEntry.get())*142

    #Beverage item
    bodyoilprice = float(BodyoilEntry.get())*475
    gastrinaprice = float(GastrinaEntry.get())*250
    herbalpaakprice = float(herbalpaakEntry.get())*1710
    immunitypaakprice = float(ImmunitypaakEntry.get())*1568
    pasteprice = float(PasteEntry.get())*190
    sadabaharteaprice = float(SadabaharteaEntry.get())*475
    toothpowderprice = float(ToothpowderEntry.get())*523
    
    #tatal price of summplement products
    
    tatalsum = aloveraprice+asparagusprice+cordycepsprice+flexseedprice+ganodermaprice+ginsengprice+grapsseedprice+javaplumprice+moringaleafprice+safedmusliprice+woodappleprice

    #tatal price of cosmetic 
    tatalsum += allpurposecreamprice+balckshampooprice+externalcreamprice+gilseringcreamprice+hairoilprice+mountshampooprice+shinecreamprice+soapprice

    #tatal price of cosmetic 
    tatalsum += bodyoilprice+gastrinaprice+herbalpaakprice+immunitypaakprice+pasteprice+sadabaharteaprice+toothpowderprice
    dis = tatalsum*0.10
    offer = tatalsum*0.05
    amtpay = tatalsum-dis

    tatalsum = '{:.1f}'.format(tatalsum)
    dis = '{:.1f}'.format(dis)
    offer = '{:.1f}'.format(offer)
    amtpay = '{:.1f}'.format(amtpay)





    TotalEntry.delete(0,END)
    DiscountEntry.delete(0,END)
    OfferEntry.delete(0,END)
    AmountpayableEntry.delete(0,END)

    TotalEntry.insert(0,f"{tatalsum}")
    DiscountEntry.insert(0,f"{dis}")
    OfferEntry.insert(0,f"{offer}")
    AmountpayableEntry.insert(0,f"{amtpay}")





#GUI part
root=Tk()
root.title('Mount Care System')
root.geometry('1920x1080')
root.iconbitmap('icon.ico')
style = Style(theme='darkly')
headingLabel=Label(root,text='Mount Care Billing System',font=('times new roman',30,'bold'),bg='gray20',fg='chartreuse3',bd=13,relief=GROOVE)
headingLabel.pack(fill=X)

customer_details_Frame=LabelFrame(root,text='Customer Details',font=('times new roman',18,'bold'),fg='chartreuse3',border=8,relief=GROOVE,bg='gray20')
customer_details_Frame.pack(fill=X)

nameLabel =Label(customer_details_Frame,text='Name',font=('times new roman',15,'bold'),bg='gray20',fg='white')
nameLabel.grid(row=0,column=0)


nameEntry = Entry(customer_details_Frame,font=('arial',15),bd=7,width=18) #name field
nameEntry.grid(row=0,column=1,padx=(0,20))


AddressLabel =Label(customer_details_Frame,text='Address',font=('times new roman',15,'bold'),bg='gray20',fg='white')
AddressLabel.grid(row=0,column=2,pady=2)

AddressEntry = Entry(customer_details_Frame,font=('arial',15),bd=7,width=10) #name field
AddressEntry.grid(row=0,column=3,padx=(0,20))

MoidLabel =Label(customer_details_Frame,text='Mo Id',font=('times new roman',15,'bold'),bg='gray20',fg='white')
MoidLabel.grid(row=0,column=4,pady=2)

MoidEntry = Entry(customer_details_Frame,font=('arial',15),bd=7,width=18) #name field
MoidEntry.grid(row=0,column=5,padx=(0,20))

dealerLabel =Label(customer_details_Frame,text='Dealer',font=('times new roman',15,'bold'),bg='gray20',fg='white')
dealerLabel.grid(row=0,column=6,pady=2)

dealerEntry = Entry(customer_details_Frame,font=('arial',15),bd=7,width=18) #name field
dealerEntry.grid(row=0,column=7,padx=(0,20))

sdealerLabel =Label(customer_details_Frame,text='SDealer',font=('times new roman',15,'bold'),bg='gray20',fg='white')
sdealerLabel.grid(row=0,column=8,pady=2)

sdealerEntry = Entry(customer_details_Frame,font=('arial',15),bd=7,width=18) #name field
sdealerEntry.grid(row=0,column=9,padx=(0,20))

BillLabel =Label(customer_details_Frame,text='Bill Number',font=('times new roman',15,'bold'),bg='gray20',fg='white')
BillLabel.grid(row=0,column=10,pady=2)

BillEntry = Entry(customer_details_Frame,font=('arial',15),bd=7,width=18) #name field
BillEntry.grid(row=0,column=11,padx=(0,20))

searchButton = Button(customer_details_Frame,text='SEARCH',font=("arial",13,'bold'),bd=7,width=10,command=search_bill)
searchButton.grid(row=0,column=13,padx=(0,13),pady=8)


productFrame=Frame(root)
productFrame.pack()

FoodSupplementFrame = LabelFrame(productFrame,text='Food Supplement',font=('times new roman',18,'bold'),fg='chartreuse3',border=8,relief=GROOVE,bg='gray20')
FoodSupplementFrame.grid(row=0,column=0)


aloveraLabel=Label(FoodSupplementFrame,text='Alovera',font=('times new roman',15,'bold'),bg='gray20',fg='white')
aloveraLabel.grid(row=0,column=0,pady=9,padx=10,sticky='w')

AloveraEntry=Entry(FoodSupplementFrame,font=('times new roman',15,'bold'),width=10,bd=5)
AloveraEntry.grid(row=0,column=1,pady=9,padx=10)
AloveraEntry.insert(0,0)

AsparagusLabel=Label(FoodSupplementFrame,text='Asparagus',font=('times new roman',15,'bold'),bg='gray20',fg='white')
AsparagusLabel.grid(row=1,column=0,pady=9,padx=10,sticky='w')

AsparagusEntry=Entry(FoodSupplementFrame,font=('times new roman',15,'bold'),width=10,bd=5)
AsparagusEntry.grid(row=1,column=1,pady=9,padx=10)
AsparagusEntry.insert(0,0)

CordycepsLabel=Label(FoodSupplementFrame,text='Cordyceps',font=('times new roman',15,'bold'),bg='gray20',fg='white')
CordycepsLabel.grid(row=2,column=0,pady=9,padx=10,sticky='w')

CordycepsEntry=Entry(FoodSupplementFrame,font=('times new roman',15,'bold'),width=10,bd=5)
CordycepsEntry.grid(row=2,column=1,pady=9,padx=10)
CordycepsEntry.insert(0,0)

FlexseedLabel=Label(FoodSupplementFrame,text='Flexseed',font=('times new roman',15,'bold'),bg='gray20',fg='white')
FlexseedLabel.grid(row=3,column=0,pady=9,padx=10,sticky='w')

FlexseedEntry=Entry(FoodSupplementFrame,font=('times new roman',15,'bold'),width=10,bd=5)
FlexseedEntry.grid(row=3,column=1,pady=9,padx=10)
FlexseedEntry.insert(0,0)

GanodermaLabel=Label(FoodSupplementFrame,text='Ganoderma',font=('times new roman',15,'bold'),bg='gray20',fg='white')
GanodermaLabel.grid(row=4,column=0,pady=9,padx=10,sticky='w')

GanodermaEntry=Entry(FoodSupplementFrame,font=('times new roman',15,'bold'),width=10,bd=5)
GanodermaEntry.grid(row=4,column=1,pady=9,padx=10)
GanodermaEntry.insert(0,0)

GinsengLabel=Label(FoodSupplementFrame,text='Ginseng',font=('times new roman',15,'bold'),bg='gray20',fg='white')
GinsengLabel.grid(row=5,column=0,pady=9,padx=10,sticky='w')

GinsengEntry=Entry(FoodSupplementFrame,font=('times new roman',15,'bold'),width=10,bd=5)
GinsengEntry.grid(row=5,column=1,pady=9,padx=10)
GinsengEntry.insert(0,0)

#begin
GrapsseedLabel=Label(FoodSupplementFrame,text='Graps Seed',font=('times new roman',15,'bold'),bg='gray20',fg='white')
GrapsseedLabel.grid(row=6,column=0,pady=9,padx=10,sticky='w')

GrapsseedEntry=Entry(FoodSupplementFrame,font=('times new roman',15,'bold'),width=10,bd=5)
GrapsseedEntry.grid(row=6,column=1,pady=9,padx=10)
GrapsseedEntry.insert(0,0)

JavaplumLabel=Label(FoodSupplementFrame,text='Java Plum',font=('times new roman',15,'bold'),bg='gray20',fg='white')
JavaplumLabel.grid(row=7,column=0,pady=9,padx=10,sticky='w')

JavaplumEntry=Entry(FoodSupplementFrame,font=('times new roman',15,'bold'),width=10,bd=5)
JavaplumEntry.grid(row=7,column=1,pady=9,padx=10)
JavaplumEntry.insert(0,0)

MoringaleafLabel=Label(FoodSupplementFrame,text='Moringa Leaf',font=('times new roman',15,'bold'),bg='gray20',fg='white')
MoringaleafLabel.grid(row=8,column=0,pady=9,padx=10,sticky='w')

MoringaleafEntry=Entry(FoodSupplementFrame,font=('times new roman',15,'bold'),width=10,bd=5)
MoringaleafEntry.grid(row=8,column=1,pady=9,padx=10)
MoringaleafEntry.insert(0,0)

SafedmusliLabel=Label(FoodSupplementFrame,text='Safed Musli',font=('times new roman',15,'bold'),bg='gray20',fg='white')
SafedmusliLabel.grid(row=9,column=0,pady=9,padx=10,sticky='w')

SafedmusliEntry=Entry(FoodSupplementFrame,font=('times new roman',15,'bold'),width=10,bd=5)
SafedmusliEntry.grid(row=9,column=1,pady=9,padx=10)
SafedmusliEntry.insert(0,0)

WoodappleLabel=Label(FoodSupplementFrame,text='Wood Apple',font=('times new roman',15,'bold'),bg='gray20',fg='white')
WoodappleLabel.grid(row=10,column=0,pady=9,padx=10,sticky='w')

WoodappleEntry=Entry(FoodSupplementFrame,font=('times new roman',15,'bold'),width=10,bd=5)
WoodappleEntry.grid(row=10,column=1,pady=9,padx=10)
WoodappleEntry.insert(0,0)

CosmeticFrame = LabelFrame(productFrame,text='Cosmetic',font=('times new roman',18,'bold'),fg='chartreuse3',border=8,relief=GROOVE,bg='gray20')

CosmeticFrame.grid(row=0,column=1,sticky='N')


#begin
AllpurposecreamLabel=Label(CosmeticFrame,text='All Purpose Cream',font=('times new roman',15,'bold'),bg='gray20',fg='white')
AllpurposecreamLabel.grid(row=0,column=0,pady=9,padx=10,sticky='w')

AllpurposecreamEntry=Entry(CosmeticFrame,font=('times new roman',15,'bold'),width=10,bd=5)
AllpurposecreamEntry.grid(row=0,column=1,pady=9,padx=10)
AllpurposecreamEntry.insert(0,0)

BlackshampooLabel=Label(CosmeticFrame,text='Black Shampoo',font=('times new roman',15,'bold'),bg='gray20',fg='white')
BlackshampooLabel.grid(row=1,column=0,pady=9,padx=10,sticky='w')

BlackshampooEntry=Entry(CosmeticFrame,font=('times new roman',15,'bold'),width=10,bd=5)
BlackshampooEntry.grid(row=1,column=1,pady=9,padx=10)
BlackshampooEntry.insert(0,0)

ExternalcreamLabel=Label(CosmeticFrame,text='External Cream',font=('times new roman',15,'bold'),bg='gray20',fg='white')
ExternalcreamLabel.grid(row=2,column=0,pady=9,padx=10,sticky='w')

ExternalcreamEntry=Entry(CosmeticFrame,font=('times new roman',15,'bold'),width=10,bd=5)
ExternalcreamEntry.grid(row=2,column=1,pady=9,padx=10)
ExternalcreamEntry.insert(0,0)

GilseringcreamLabel=Label(CosmeticFrame,text='Gilsering Cream',font=('times new roman',15,'bold'),bg='gray20',fg='white')
GilseringcreamLabel.grid(row=3,column=0,pady=9,padx=10,sticky='w')

GilseringcreamEntry=Entry(CosmeticFrame,font=('times new roman',15,'bold'),width=10,bd=5)
GilseringcreamEntry.grid(row=3,column=1,pady=9,padx=10)
GilseringcreamEntry.insert(0,0)

HairoilLabel=Label(CosmeticFrame,text='Hair Oil',font=('times new roman',15,'bold'),bg='gray20',fg='white')
HairoilLabel.grid(row=4,column=0,pady=9,padx=10,sticky='w')

HairoilEntry=Entry(CosmeticFrame,font=('times new roman',15,'bold'),width=10,bd=5)
HairoilEntry.grid(row=4,column=1,pady=9,padx=10)
HairoilEntry.insert(0,0)

MountshampoocreamLabel=Label(CosmeticFrame,text='Mount Shampoo',font=('times new roman',15,'bold'),bg='gray20',fg='white')
MountshampoocreamLabel.grid(row=5,column=0,pady=9,padx=10,sticky='w')

MountshampoocreamEntry=Entry(CosmeticFrame,font=('times new roman',15,'bold'),width=10,bd=5)
MountshampoocreamEntry.grid(row=5,column=1,pady=9,padx=10)
MountshampoocreamEntry.insert(0,0)

ShinecreamLabel=Label(CosmeticFrame,text='Shine Cream',font=('times new roman',15,'bold'),bg='gray20',fg='white')
ShinecreamLabel.grid(row=6,column=0,pady=9,padx=10,sticky='w')

ShinecreamEntry=Entry(CosmeticFrame,font=('times new roman',15,'bold'),width=10,bd=5)
ShinecreamEntry.grid(row=6,column=1,pady=9,padx=10)
ShinecreamEntry.insert(0,0)

SoapLabel=Label(CosmeticFrame,text='Soap',font=('Hair Oil',15,'bold'),bg='gray20',fg='white')
SoapLabel.grid(row=7,column=0,pady=9,padx=10,sticky='w')

SoapEntry=Entry(CosmeticFrame,font=('times new roman',15,'bold'),width=10,bd=5)
SoapEntry.grid(row=7,column=1,pady=9,padx=10)
SoapEntry.insert(0,0)

BeverageFrame = LabelFrame(productFrame,text='Beverage',font=('times new roman',18,'bold'),fg='chartreuse3',border=8,relief=GROOVE,bg='gray20')

BeverageFrame.grid(row=0,column=2,sticky='N')

#begin

BodyoilLabel=Label(BeverageFrame,text='Body Oil',font=('times new roman',15,'bold'),bg='gray20',fg='white')
BodyoilLabel.grid(row=0,column=0,pady=9,padx=10,sticky='w')

BodyoilEntry=Entry(BeverageFrame,font=('times new roman',15,'bold'),width=10,bd=5)
BodyoilEntry.grid(row=0,column=1,pady=9,padx=10)
BodyoilEntry.insert(0,0)

GastrinaLabel=Label(BeverageFrame,text='Gastrina',font=('times new roman',15,'bold'),bg='gray20',fg='white')
GastrinaLabel.grid(row=1,column=0,pady=9,padx=10,sticky='w')

GastrinaEntry=Entry(BeverageFrame,font=('times new roman',15,'bold'),width=10,bd=5)
GastrinaEntry.grid(row=1,column=1,pady=9,padx=10)
GastrinaEntry.insert(0,0)

herbalpaakLabel=Label(BeverageFrame,text='Herbal Paak',font=('times new roman',15,'bold'),bg='gray20',fg='white')
herbalpaakLabel.grid(row=2,column=0,pady=9,padx=10,sticky='w')

herbalpaakEntry=Entry(BeverageFrame,font=('times new roman',15,'bold'),width=10,bd=5)
herbalpaakEntry.grid(row=2,column=1,pady=9,padx=10)
herbalpaakEntry.insert(0,0)

ImmunitypaakLabel=Label(BeverageFrame,text='Immunity Paak',font=('times new roman',15,'bold'),bg='gray20',fg='white')
ImmunitypaakLabel.grid(row=3,column=0,pady=9,padx=10,sticky='w')

ImmunitypaakEntry=Entry(BeverageFrame,font=('times new roman',15,'bold'),width=10,bd=5)
ImmunitypaakEntry.grid(row=3,column=1,pady=9,padx=10)
ImmunitypaakEntry.insert(0,0)

PasteLabel=Label(BeverageFrame,text='Paste',font=('times new roman',15,'bold'),bg='gray20',fg='white')
PasteLabel.grid(row=4,column=0,pady=9,padx=10,sticky='w')

PasteEntry=Entry(BeverageFrame,font=('times new roman',15,'bold'),width=10,bd=5)
PasteEntry.grid(row=4,column=1,pady=9,padx=10)
PasteEntry.insert(0,0)

SadabaharteaLabel=Label(BeverageFrame,text='Sadabahar Tea',font=('times new roman',15,'bold'),bg='gray20',fg='white')
SadabaharteaLabel.grid(row=5,column=0,pady=9,padx=10,sticky='w')

SadabaharteaEntry=Entry(BeverageFrame,font=('times new roman',15,'bold'),width=10,bd=5)
SadabaharteaEntry.grid(row=5,column=1,pady=9,padx=10)
SadabaharteaEntry.insert(0,0)

ToothpowderLabel=Label(BeverageFrame,text='Tooth Powder',font=('times new roman',15,'bold'),bg='gray20',fg='white')
ToothpowderLabel.grid(row=6,column=0,pady=9,padx=10,sticky='w')

ToothpowderEntry=Entry(BeverageFrame,font=('times new roman',15,'bold'),width=10,bd=5)
ToothpowderEntry.grid(row=6,column=1,pady=9,padx=10)
ToothpowderEntry.insert(0,0)



billFrame=Frame(productFrame,bd=8,relief=GROOVE)
billFrame.grid(row=0,column=3,padx=10)

billareaLabel=Label(billFrame,text='Bill Area',font=('times new roman',18,'bold'),bd=7,relief=GROOVE)
billareaLabel.pack(fill=X)

scrollbar=Scrollbar(billFrame,orient=VERTICAL)
scrollbar.pack(side=RIGHT,fill=Y)

textarea=Text(billFrame,height=35,width=60,yscrollcommand=scrollbar.set) #28,55
textarea.pack()
scrollbar.config(command=textarea.yview)


billFrame=Frame(productFrame,bd=8,relief=GROOVE)
billFrame.grid(row=0,column=4,padx=10)

OfferFrame = LabelFrame(productFrame, text='Offer Section', font=('times new roman', 18, 'bold'), fg='chartreuse3',
                         border=8, relief=GROOVE, bg='gray20')
OfferFrame.grid(row=0, column=4)

# Creating a canvas and scrollbar for the Offer Section
offer_canvas = Canvas(OfferFrame, bg='gray20', bd=0, relief=GROOVE, width=400, height=580)
offer_scrollbar = Scrollbar(OfferFrame, orient=VERTICAL, command=offer_canvas.yview)
offer_scrollbar.pack(side=RIGHT, fill=Y)
offer_canvas.pack(side=LEFT, fill=BOTH, expand=True)
offer_canvas.configure(yscrollcommand=offer_scrollbar.set)

# Create a frame inside the canvas to hold the widgets
offer_frame = Frame(offer_canvas, bg='gray20')
offer_canvas.create_window((0, 0), window=offer_frame, anchor='nw')

def create_product_entries(frame, products):
    entry_dict = {}
    
    for index, product in enumerate(products):
        label = Label(frame, text=product, font=('times new roman', 15, 'bold'), bg='gray20', fg='white')
        label.grid(row=index, column=0, sticky='w', pady=5, padx=10)

        entry = Entry(frame, font=('times new roman', 15, 'bold'), bd=5, width=10)
        entry.grid(row=index, column=1, pady=5)
        entry.insert(0,0)
        entry_dict[product] = entry  # Associate each entry field with its product name

    for entry in entry_dict.values():
        entry.bind('<FocusOut>', lambda event: calculate_total(entry_dict))  # Bind FocusOut event

def calculate_total(entry_dict):
    total = 0
    global offer_qty
    offer_qty = {}
    for product, entry in entry_dict.items():
        try:
            if product == "Alovera":
                value = int(entry.get())*760
                if value != 0 and product not in offer_qty: offer_qty[product] = int(entry.get())
            elif product == "Asparagus":
                value = int(entry.get())*960
                if value != 0 and product not in offer_qty: offer_qty[product] = int(entry.get())
            elif product == "Cordyceps":
                value = int(entry.get())*2090
                if value != 0 and product not in offer_qty: offer_qty[product] = int(entry.get())
            elif product == "Flexseed":
                value = int(entry.get())*1140
                if value != 0 and product not in offer_qty: offer_qty[product] = int(entry.get())
            elif product == "Ganoderma":
                value = int(entry.get())*1425
                if value != 0  and product not in offer_qty: offer_qty[product] = int(entry.get())
            elif product == "Ginseng":
                value = int(entry.get())*1805
                if value != 0 and product not in offer_qty: offer_qty[product] = int(entry.get())
            elif product == "Graps Seed":
                value = int(entry.get())*1335
                if value != 0 and product not in offer_qty: offer_qty[product] = int(entry.get())
            elif product == "Java Plum":
                value = int(entry.get())*1045
                if value != 0 and product not in offer_qty: offer_qty[product] = int(entry.get())
            elif product == "Moringa Leaf":
                value = int(entry.get())*1045
                if value != 0 and product not in offer_qty: offer_qty[product] = int(entry.get())
            elif product == "Safed Musli":
                value = int(entry.get())*1140
            elif product == "Wood Apple":
                value = int(entry.get())*950
                if value != 0 and product not in offer_qty: offer_qty[product] = int(entry.get())
            elif product == "All Purpose Cream":
                value = int(entry.get())*617
                if value != 0 and product not in offer_qty: offer_qty[product] = int(entry.get())
            elif product == "Black Shampoo":
                value = int(entry.get())*617.5
                if value != 0 and product not in offer_qty: offer_qty[product] = int(entry.get())
            elif product == "External Cream":
                value = int(entry.get())*950
                if value != 0 and product not in offer_qty: offer_qty[product] = int(entry.get())
            elif product == "Gilsering Cream":
                value = int(entry.get())*95
                if value != 0 and product not in offer_qty: offer_qty[product] = int(entry.get())
            elif product == "Hair Oil":
                value = int(entry.get())*570
                if value != 0 and product not in offer_qty: offer_qty[product] = int(entry.get())
            elif product == "Mount Shampoo":
                value = int(entry.get())*475
                if value != 0 and product not in offer_qty: offer_qty[product] = int(entry.get())
            elif product == "Shine Cream":
                value = int(entry.get())*950
                if value != 0 and product not in offer_qty: offer_qty[product] = int(entry.get())
            elif product == "Soap":
                value = int(entry.get())*142
                if value != 0 and product not in offer_qty: offer_qty[product] = int(entry.get())
            elif product == "Body Oil":
                value = int(entry.get())*475
                if value != 0 and product not in offer_qty: offer_qty[product] = int(entry.get())
            elif product == "Gastrina":
                value = int(entry.get())*250
                if value != 0 and product not in offer_qty: offer_qty[product] = int(entry.get())
            elif product == "Herbal Paak":
                value = int(entry.get())*1710
                if value != 0 and product not in offer_qty: offer_qty[product] = int(entry.get())
            elif product == "Immunity Paak":
                value = int(entry.get())*1568
                if value != 0 and product not in offer_qty: offer_qty[product] = int(entry.get())
            elif product == "Paste":
                value = int(entry.get())*190
                if value != 0 and product not in offer_qty: offer_qty[product] = int(entry.get())
            elif product == "Sadabahar Tea":
                value = int(entry.get())*475
                if value != 0 and product not in offer_qty: offer_qty[product] = int(entry.get())
            elif product == "Tooth Powder":
                value = int(entry.get())*523
                if value != 0 and product not in offer_qty: offer_qty[product] = int(entry.get())
            total += value
        except ValueError:
            pass  # Ignore non-integer inputs

    TotalEntry1.delete(0,END)  # You can replace print with any action you want to take with the total value
    TotalEntry1.insert(0,f"{total}")



# Products data
food_supplement_products = ['Alovera', 'Asparagus', 'Cordyceps', 'Flexseed', 'Ganoderma', 'Ginseng',
                            'Graps Seed', 'Java Plum', 'Moringa Leaf', 'Safed Musli', 'Wood Apple']

cosmetic_products = ['All Purpose Cream', 'Black Shampoo', 'External Cream', 'Gilsering Cream', 'Hair Oil',
                     'Mount Shampoo', 'Shine Cream', 'Soap']

beverage_products = ['Body Oil', 'Gastrina', 'Herbal Paak', 'Immunity Paak', 'Paste', 'Sadabahar Tea', 'Tooth Powder']

# Create product entries
food_supplement_products.extend(cosmetic_products)
food_supplement_products.extend(beverage_products)

offer_product =  create_product_entries(offer_frame, food_supplement_products)


# Configuring canvas scrolling region
offer_frame.update_idletasks()
offer_canvas.config(scrollregion=offer_canvas.bbox("all"))

# Binding mouse wheel event to canvas
def on_mousewheel(event):
    offer_canvas.yview_scroll(int(-1 * (event.delta / 130)), "units")

offer_canvas.bind_all("<MouseWheel>", on_mousewheel)

BillmenuFrame = LabelFrame(root,text='Bill Menu',font=('times new roman',18,'bold'),fg='chartreuse3',border=8,relief=GROOVE,bg='gray20')
BillmenuFrame.pack(pady=10,side=TOP, anchor=NW)

TotalLabel=Label(BillmenuFrame,text='Total',font=('times new roman',14,'bold'),bg='gray20',fg='white')
TotalLabel.grid(row=0,column=0,pady=5,padx=10,sticky='w')

TotalEntry=Entry(BillmenuFrame,font=('times new roman',14,'bold'),width=15,bd=5)
TotalEntry.grid(row=0,column=1,pady=5,padx=10)

DiscountLabel=Label(BillmenuFrame,text='Discount',font=('times new roman',14,'bold'),bg='gray20',fg='white')
DiscountLabel.grid(row=2,column=0,pady=5,padx=10,sticky='w')

DiscountEntry=Entry(BillmenuFrame,font=('times new roman',14,'bold'),width=15,bd=5)
DiscountEntry.grid(row=2,column=1,pady=5,padx=10)

AmountpayableLabel=Label(BillmenuFrame,text='Amount Payable',font=('times new roman',14,'bold'),bg='gray20',fg='white')
AmountpayableLabel.grid(row=3,column=0,pady=5,padx=10,sticky='w')

AmountpayableEntry=Entry(BillmenuFrame,font=('times new roman',14,'bold'),width=15,bd=5)
AmountpayableEntry.grid(row=3,column=1,pady=5,padx=10)

#begin

OfferLabel=Label(BillmenuFrame,text='Offer',font=('times new roman',14,'bold'),bg='gray20',fg='white')
OfferLabel.grid(row=0,column=2,pady=5,padx=10,sticky='w')

OfferEntry=Entry(BillmenuFrame,font=('times new roman',14,'bold'),width=15,bd=5)
OfferEntry.grid(row=0,column=3,pady=5,padx=10)

buttonFrame=Frame(BillmenuFrame,bd=8,relief=GROOVE)
buttonFrame.grid(row=0,column=4,rowspan=7)

totalButton=Button(buttonFrame,text='TOTAL',font=('arial',18,'bold'),bg='chartreuse3',fg='white',bd=5,width=8,command=total)
totalButton.grid(row=0,column=0,pady=30,padx=5)

BillButton=Button(buttonFrame,text='BILL',font=('arial',18,'bold'),bg='chartreuse3',fg='white',bd=5,width=8,command=bill_area)
BillButton.grid(row=0,column=1,pady=30,padx=5)

EmailButton=Button(buttonFrame,text='EMAIL',font=('arial',18,'bold'),bg='chartreuse3',fg='white',bd=5,width=8)
EmailButton.grid(row=0,column=2,pady=30,padx=5)

PrintButton=Button(buttonFrame,text='PRINT',font=('arial',18,'bold'),bg='chartreuse3',fg='white',bd=5,width=8,command=make_pdf)
PrintButton.grid(row=0,column=3,pady=30,padx=10,)

ClearButton=Button(buttonFrame,text='CLEAR',font=('arial',18,'bold'),bg='chartreuse3',fg='white',bd=5,width=8)
ClearButton.grid(row=0,column=4,pady=30,padx=5)

#here uis t
# Here is the existing code for the first bill menu...


lev = Label(BillmenuFrame, text='Offer Bill', font=('times new roman', 18, 'bold'), bg='gray20', fg='chartreuse3')
lev.grid(row=0, column=5, pady=5, padx=(147,0))

TotalLabel2 = Label(BillmenuFrame, text='Offer Total', font=('times new roman', 13, 'bold'), bg='gray20', fg='white')
TotalLabel2.grid(row=2, column=5, pady=5, padx=(150,0))

TotalEntry1=Entry(BillmenuFrame,font=('times new roman',14,'bold'),width=10,bd=5)
TotalEntry1.grid(row=2,column=6,pady=5,padx=(50,1000))

ClearButton2=Button(BillmenuFrame,text='CLEAR',font=('arial',14,'bold'),bg='chartreuse3',fg='white',bd=5,width=8)
ClearButton2.grid(row=3,column=6,pady=3,padx=(50,1000))

# Bind update_total_discount function to all entry widgets for Food Supplements
for entry in [AloveraEntry, AsparagusEntry, CordycepsEntry, FlexseedEntry, GanodermaEntry, GinsengEntry, GrapsseedEntry, JavaplumEntry, MoringaleafEntry, SafedmusliEntry, WoodappleEntry]:
    entry.bind('<FocusOut>', update_total_discount)

# Bind update_total_discount function to all entry widgets for Cosmetics
for entry in [AllpurposecreamEntry, BlackshampooEntry, ExternalcreamEntry, GilseringcreamEntry, HairoilEntry, MountshampoocreamEntry, ShinecreamEntry, SoapEntry]:
    entry.bind('<FocusOut>', update_total_discount)

# Bind update_total_discount function to all entry widgets for Beverages
for entry in [BodyoilEntry, GastrinaEntry, herbalpaakEntry, ImmunitypaakEntry, PasteEntry, SadabaharteaEntry, ToothpowderEntry]:
    entry.bind('<FocusOut>', update_total_discount)

root.mainloop()