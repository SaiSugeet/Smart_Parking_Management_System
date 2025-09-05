import re
import qrcode
from datetime import datetime
from flask import Flask, render_template_string
from PIL import Image
import threading


app = Flask(__name__)


Vehicle_Number = []
Vehicle_Type = []
vehicle_Name = []
Owner_Name = []
Date = []
Time = []
receipts = {}  


two_wheelers = 100
four_wheelers = 200



@app.route("/receipt/<vno>")
def receipt(vno):
    return receipts.get(vno, "<h2>❌ Receipt not found</h2>")



def parking_system():
    global two_wheelers, four_wheelers
    try:
        while True:
            print("----------------------------------------------------------------------------------------")
            print("\t\tParking Management System")
            print("----------------------------------------------------------------------------------------")
            print("1.Vehicle Entry")
            print("2.Remove Entry")
            print("3.View Parked Vehicle ")
            print("4.View Left Parking Space ")
            print("5.Amount Details ")
            print("6.Bill (Generate QR Receipt)")
            print("7.Close Programme ")
            print("+---------------------------------------------+")
            ch = int(input("\tSelect option:"))

            
            if ch == 1:
                while True:
                    Vno = input("\tEnter vehicle number (e.g., KA-08-AS-2345) - ").upper()
                    pattern = r"^[A-Z]{2}-\d{2}-[A-Z]{1,2}-\d{4}$"
                    if Vno == "":
                        print("###### Enter Vehicle No. ######")
                    elif not re.match(pattern, Vno):
                        print("###### Enter Valid Indian Vehicle Number (KA-08-AS-2345) ######")
                    elif Vno in Vehicle_Number:
                        print("###### Vehicle Number Already Exists ######")
                    else:
                        Vehicle_Number.append(Vno)
                        break

                while True:
                    Vtype = input("\tEnter vehicle type (Two-Wheeler=A / Four-Wheeler=B): ").lower()
                    if Vtype == "a":
                        Vehicle_Type.append("Two-Wheeler")
                        two_wheelers -= 1
                        break
                    elif Vtype == "b":
                        Vehicle_Type.append("Four-Wheeler")
                        four_wheelers -= 1
                        break
                    else:
                        print("###### Please Enter Valid Option ######")

                vname = input("\tEnter vehicle name - ") or "Unknown"
                vehicle_Name.append(vname)

                OName = input("\tEnter owner name - ") or "Unknown"
                Owner_Name.append(OName)

                now = datetime.now()
                Date.append(now.strftime("%d-%m-%Y"))
                Time.append(now.strftime("%H:%M:%S"))

                print("\n✅ Record detail saved.")

            
            elif ch == 2:
                Vno = input("\tEnter vehicle number to Delete - ").upper()
                if Vno in Vehicle_Number:
                    i = Vehicle_Number.index(Vno)
                    for lst in [Vehicle_Number, Vehicle_Type, vehicle_Name, Owner_Name, Date, Time]:
                        lst.pop(i)
                    print("✅ Removed Successfully")
                else:
                    print("❌ No Such Entry")

            
            elif ch == 3:
                print("Vehicle No.\tType\tName\tOwner\tDate\tTime")
                for i in range(len(Vehicle_Number)):
                    print(Vehicle_Number[i], Vehicle_Type[i], vehicle_Name[i],
                          Owner_Name[i], Date[i], Time[i])

            
            elif ch == 4:
                print("Spaces Available: Two-Wheelers =", two_wheelers,
                      "Four-Wheelers =", four_wheelers)

            
            elif ch == 5:
                print("Rates: Two-Wheeler = ₹30/hour | Four-Wheeler = ₹60/hour")

            
            elif ch == 6:
                Vno = input("\tEnter vehicle number (KA-08-AS-2345) - ").upper()
                if Vno not in Vehicle_Number:
                    print("❌ No Such Entry")
                    continue

                i = Vehicle_Number.index(Vno)
                hr = int(input("\tEnter No. of Hours Vehicle Parked - ") or "1")

                amt = hr * (30 if Vehicle_Type[i] == "Two-Wheeler" else 60)
                tax = 0.18 * amt
                total = amt + tax

                now = datetime.now()
                billing_date = now.strftime("%d-%m-%Y")
                billing_time = now.strftime("%H:%M:%S")

                receipt_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Parking Receipt</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body {{ background: #f8f9fa; }}
    .receipt-card {{ max-width: 500px; margin: 50px auto; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="card shadow-lg receipt-card">
      <div class="card-header text-center bg-primary text-white">
        <h4>🚗 Parking Receipt</h4>
      </div>
      <div class="card-body">
        <p><b>Vehicle No:</b> {Vno}</p>
        <p><b>Type:</b> {Vehicle_Type[i]}</p>
        <p><b>Owner:</b> {Owner_Name[i]}</p>
        <hr>
        <p><b>Date of Entry:</b> {Date[i]} {Time[i]}</p>
        <p><b>Billing Date:</b> {billing_date} {billing_time}</p>
        <hr>
        <p><b>Parking Charge:</b> ₹{amt}</p>
        <p><b>Tax (18%):</b> ₹{tax:.2f}</p>
        <h5 class="text-success">Total: ₹{total:.2f}</h5>
      </div>
      <div class="card-footer text-center">
        ✅ Thank you for using our service!
      </div>
    </div>
  </div>
</body>
</html>
"""
                receipts[Vno] = receipt_html  

                
                url = f"http://192.168.1.146:5000/receipt/{Vno}"
                qr = qrcode.make(url)
                qr_filename = f"receipt_{Vno}.png"
                qr.save(qr_filename)
                Image.open(qr_filename).show()

                print(f"✅ Bill Generated. Scan QR to view: {url}")

            elif ch == 7:
                print("👋 Exiting...")
                break

    except Exception as e:
        print("⚠️ Error:", e)
        parking_system()



if __name__ == "__main__":
    
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=5000, debug=False)).start()
    
    parking_system()
