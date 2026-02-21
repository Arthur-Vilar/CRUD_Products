import sqlite3, time

connection = sqlite3.connect("database.db")
cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS products(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT NOT NULL,
               price REAL NOT NULL
               )
               """)

connection.commit()

def requestOp():
    while True:
        try:
            op = int(input('''[1] = ADD PRODUCT
[2] = CONSULT PRODUCTS
[3] = UPDATE PRODUCT
[4] = REMOVE PRODUCT
[9] = FINISH PROGRAM
What operation do you want? '''))
            if op in [1, 2, 3, 4, 9]: return op
        except ValueError: pass
        print('\033[31mInput a valid number!\033[m')

def requestName():
    name = input('Input the name of product(Enter to back to menu): ').strip()
    return name

def requestPrice():
        while True:
            try:
                price = input('Input the price of product: ').replace(',', '.')
                price = float(price)
                if price > 0: return price
            except ValueError: pass
            print('\033[31mInput a valid number!\033[m')

def requestId():
    if hasProducts():
        while True:
            try:
                productId = int(input('Input product id: '))
            except ValueError:
                print('\033[31mInput a valid number!\033[m')
                continue
            cursor.execute('SELECT 1 FROM products WHERE id = ?', (productId, ))
            product = cursor.fetchone()
            if product: return productId
            print('\033[31mProduct not found!\033[m')

def hasProducts():
    cursor.execute("SELECT 1 FROM products LIMIT 1")
    product = cursor.fetchone()
    if product: return True
    return False

def addProduct():
    name = requestName()
    if not name: return
    price = requestPrice()
    cursor.execute("""INSERT INTO products(name, price)
                   VALUES(?,?)
                    """, (name, price))
    connection.commit()
    
def readProducts():
    if hasProducts():
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        print('-' * 80) 
        for product in products:
            print(f'{product[0]} = {product[1]} | R${product[2]:.2f}')
        print('-' * 80)
    else:
        print('\033[31mNo products found..\033[m')

def updateProduct():
    if hasProducts():
        try:
            productId = requestId()
            if not productId: return
            name = requestName()
            if not name: return
            price = requestPrice()
            cursor.execute("""UPDATE products
                        SET name = ?, price = ? 
                            WHERE id = ?  """, (name, price, productId))
            connection.commit()
        except ValueError: pass
    else: 
        print('\033[31mNo products found..\033[m')


def deleteProduct():
    if hasProducts():
        productId = requestId()
        if not productId: return
        cursor.execute('DELETE FROM products WHERE id = ?', (productId,)) 
        connection.commit()
    else: 
        print('\033[31mNo products found..\033[m')


while True:
    op = requestOp()

    if op == 1:
        addProduct()
    elif op == 2:
        readProducts()
    elif op == 3:
        updateProduct()
    elif op == 4:
        deleteProduct()
    elif op == 9:
        print('\033[33mYour List is going finished...\033[m')
        connection.close()
        time.sleep(1.5)
        break

