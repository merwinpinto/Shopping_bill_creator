from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

def generate_bill():
    print("Shopping - Bill Generator")
    print("Enter product details. Type 'done' when finished.\n")
    Companyname = input("Enter your company Name: ").title()
    products = []
    grand_total = 0
    total_quantity = 0 

    def clean_and_validate_name(raw_name):
        cleaned = raw_name.strip().title()
        if any(char.isdigit() for char in cleaned):
            raise ValueError("❌ Product name must not contain numbers.")
        return cleaned

    while True:
        raw_name = input("Product Name: ").strip()
        if raw_name.lower() == 'done':
            break

        try:
            name = clean_and_validate_name(raw_name)
        except ValueError as e:
            print(e)
            continue

        try:
            weight_per_unit = float(input("Weight per unit (kg/L): "))
            price_per_unit = float(input("Price per unit (₹): "))
            quantity = int(input("Quantity: "))
        except ValueError:
            print("❌ Invalid input. Please enter valid numbers for weight, quantity, and price.\n")
            continue

        total_price = price_per_unit * quantity
        grand_total += total_price
        total_quantity += quantity

        products.append({
            "name": name,
            "weight": weight_per_unit * quantity,
            "price": total_price,
            "quantity": quantity,
            "unit_price": price_per_unit
        })

        print(f"Product Added: {name} | Qty: {quantity} | Price: ₹{total_price:.2f}\n")

    print("\n" + "=" * 45)
    print(Companyname + " INVOICE BILL")
    print("=" * 45)
    print(f"{'Product':15} {'Qty':>5} {'Weight(kg/L)':>12} {'Total(₹)':>12}")
    print("-" * 45)

    for p in products:
        print(f"{p['name'][:15]:15} {p['quantity']:>5} {p['weight']:>12.2f} {p['price']:>12.2f}")

    print("-" * 45)
    print(f"{'TOTAL':15} {total_quantity:>5} {'':>12} {grand_total:>12.2f}")  # ✅ Show total quantity
    print("=" * 45)
    print("Bill Generated!")

    save_bill_as_pdf(Companyname, products, total_quantity, grand_total)

def save_bill_as_pdf(Companyname, products, total_quantity, grand_total):
    filename = f"{Companyname}_invoice_bill_{datetime.now().strftime('%d%m%Y')}.pdf"
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, height - 50, f"{Companyname} Final Bill")

    c.setFont("Helvetica", 10)
    c.drawString(40, height - 80, f"Date: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")

    c.setFont("Helvetica-Bold", 10)
    y = height - 120
    c.drawString(40, y, "Product")
    c.drawString(160, y, "Qty")
    c.drawString(200, y, "Weight (kg/L)")
    c.drawString(300, y, "Total")

    c.line(40, y - 5, 500, y - 5)
    c.setFont("Helvetica", 10)

    for p in products:
        y -= 20
        if y < 100:
            c.showPage()
            y = height - 100
        c.drawString(40, y, p['name'][:20])
        c.drawString(160, y, str(p['quantity']))
        c.drawString(200, y, f"{p['weight']:.2f}")
        c.drawString(300, y, f"{p['price']:.2f}")

    y -= 30
    c.setFont("Helvetica-Bold", 11)
    c.drawString(40, y, "TOTAL")
    c.drawString(160, y, str(total_quantity)) 
    c.drawString(300, y, f"{grand_total:.2f}")

    y -= 40
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(40, y, f"Thank you for shopping with {Companyname}")
    y -= 20
    c.drawString(40, y, "Visit Again")

    c.save()
    print(f"PDF bill saved as '{filename}'")

generate_bill()
