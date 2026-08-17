from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory list to store sales entries for the session
sales_data = []

@app.route('/')
def index():
    # Calculate aggregate sales total
    grand_total = sum(item['total'] for item in sales_data)
   
    # Default currency symbol for summary card if sales exist, otherwise GH₵
    current_currency = sales_data[-1]['currency'] if sales_data else 'GH₵'
   
    return render_template(
        'index.html',
        sales=sales_data,
        grand_total=grand_total,
        currency=current_currency
    )

@app.route('/add', methods=['POST'])
def add_sale():
    # Retrieve form data
    product_name = request.form.get('product')
    quantity = int(request.form.get('quantity'))
    price = float(request.form.get('price'))
    currency = request.form.get('currency', 'GH₵')
   
    # Calculate item total
    total = quantity * price
   
    # Store record with currency choice
    sale_entry = {
        'product': product_name,
        'quantity': quantity,
        'price': price,
        'currency': currency,
        'total': total
    }
   
    sales_data.append(sale_entry)
    return redirect(url_for('index'))

@app.route('/delete/<int:index>')
def delete_sale(index):
    # Remove entry by index position
    if 0 <= index < len(sales_data):
        sales_data.pop(index)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)