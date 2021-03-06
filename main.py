from tkinter.ttk import *
from tkinter import filedialog
import sqlite3
from tkinter import Tk
from ttkthemes import themed_tk as tkt
from tkinter import Toplevel
conn = sqlite3.connect('app.db')


cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS items(
        itemName text,
        itemPrice real,
        itemInventory int
)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS dailyBatch(
        itemsSold text,
        itemPrice real
    )""")

conn.commit()

root = tkt.ThemedTk()
root.get_themes()
root.set_theme("breeze")

root.title("POS App")
root.geometry("975x650")

SCREEN_WIDTH, SCREEN_HEIGHT = 975, 650

rowChange = 0
columnChange = -1

newOrderPrice = []
newOrderList = []
newOrderTotal = 0

refreshButton = Button(root, text='Refresh', command=lambda:refresh())
refreshButton.place(x=SCREEN_WIDTH - 100, y=10)

newItemOpenWindow = Button(root, text="Add New Item", command=lambda:openItemWindow())
newItemOpenWindow.grid(row=rowChange + 1, column=0, columnspan=2)

PlaceOrderButton = Button(root, text='Checkout', command=lambda:checkout())
PlaceOrderButton.place(x=SCREEN_WIDTH - 150, y=SCREEN_HEIGHT - 200)

getDailyTotalButton = Button(root, text='Get Daily Total', command=lambda:getDailyTotal())
getDailyTotalButton.place(x=SCREEN_WIDTH - 150, y=SCREEN_HEIGHT - 150)

clearBatchButton = Button(root, text='Clear Daily Batch', command=lambda:clearBatch())
clearBatchButton.place(x=SCREEN_WIDTH-150, y=SCREEN_HEIGHT-50)

def refresh():
    global refreshButton

    cursor.execute("SELECT * FROM items")

    items = cursor.fetchall()

    for item in items:
        loadItem(item[0], item[1])
    
    refreshButton.place_forget()



def loadItem(name, price):
    global rowChange
    global columnChange
    global newItemOpenWindow

    columnChange += 1
    if columnChange == 5:
        rowChange += 1
        columnChange = 0

    bookButton = Button(root, text=name + f'\n{price}', command=lambda:addItem(name, price))
    bookButton.grid(row=rowChange, column=columnChange, padx=10, pady=10, ipadx=10, ipady=30)

def addItem(name, price):
    global newOrderPrice
    global newOrderTotal
    newOrderTotal = 0
    newOrderPrice.append(price)
    newOrderTotal = 0
    newOrderList.append(name)

    for x in newOrderPrice:
        newOrderTotal += x


    print(str(newOrderList) + ' ' + str(newOrderTotal))

    orderLabel = Label(root, text='Order: \n')
    orderLabel.place_forget()

    for item in newOrderList:
        orderLabel.configure(text=orderLabel.cget("text") + '\n' + item)
    
    orderLabel.configure(text=orderLabel.cget("text") + '\n Total:  ' + str(newOrderTotal))

    orderLabel.place(x=SCREEN_WIDTH - 150, y=100)




def openItemWindow():
    global filename

    newItemWindow = Toplevel()
    newItemWindow.title("Add New Item")
    newItemWindow.geometry("400x200")

    newItemEntry = Entry(newItemWindow)
    newItemNameLabel = Label(newItemWindow, text="Item Name:")

    newItemPriceEntry = Entry(newItemWindow)
    newItemPriceLabel = Label(newItemWindow, text="Item Price")

    newItemNameLabel.grid(row=1, column=0, padx=10, pady=5)
    newItemEntry.grid(row=1, column=1, padx=10, pady=5)
    newItemPriceLabel.grid(row=2, column=0, padx=10, pady=5)
    newItemPriceEntry.grid(row=2, column=1, padx=10, pady=5)
    newItemImageButton = Button(newItemWindow, text="Select Image", command=lambda:browseFiles(newItemWindow))
    newItemImageButton.grid(row=3, column=0, padx=10, pady=5)

    submitNewItemButton = Button(newItemWindow, text='Submit Item', command=lambda:submitNewItem(newItemEntry.get(), newItemPriceEntry.get(), None, newItemWindow))
    submitNewItemButton.grid(row=4, column=0, padx=10, pady=15, columnspan=2)



def browseFiles(window):
    global filename
    filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("PNG Files",
                                                        "*.png*"),
                                                       ("all files",
                                                        "*.*")))
                    
    fileSelectedLabel = Label(window, text="Selected Image: " + filename)
    fileSelectedLabel.grid(row=3, column=1, columnspan=2, padx=10, pady=5)                
            


def submitNewItem(itemName, itemPrice, itemImage, window):
    cursor.execute("INSERT INTO items VALUES (:name, :price, :image)",
    {
        'name': itemName,
        'price': itemPrice,
        'image': itemImage
    })

    conn.commit()
    loadItem(itemName, itemPrice)
    window.destroy()


def checkout():
    global newOrderPrice
    global newOrderList
    global newOrderTotal
    global checkoutWindow

    checkoutWindow = Toplevel()
    checkoutWindow.title("Checkout")

    orderLabel = Label(checkoutWindow, text='Order: \n', padx=10, pady=15)
    orderLabel.place_forget()

    for item in newOrderList:
        orderLabel.configure(text=orderLabel.cget("text") + '\n' + item)


    cashEntry = Entry(checkoutWindow)
    cashLabel = Label(checkoutWindow, text='Amount Paid:')
    submitPayButton = Button(checkoutWindow, text='Pay', command=lambda:clearOrder())
    orderTotalLabel = Label(checkoutWindow, text=str(newOrderTotal))

    cashLabel.grid(row=0, column=0)
    cashEntry.grid(row=0, column=1)
    submitPayButton.grid(row=1, column=0, columnspan=2)
    orderTotalLabel.grid(row=2, column=0, columnspan=2)

    orderLabel.grid(row=3, column=0, columnspan=2)


def clearOrder():
    global newOrderList
    global newOrderPrice
    global newOrderTotal
    global checkoutWindow

    priceCounter = 0

    for x in newOrderList:

        cursor.execute("INSERT INTO dailyBatch VALUES(:itemSold, :itemPrice)",
        {
            'itemSold': x,
            'itemPrice': newOrderPrice[priceCounter]

        })
        conn.commit()
        priceCounter += 1
    
    newOrderList.clear()
    newOrderPrice.clear()
    newOrderTotal = 0
    checkoutWindow.destroy()


def getDailyTotal():

    cursor.execute("SELECT itemPrice FROM dailybatch")

    totals = cursor.fetchall()
    dailyTotal = 0

    for x in totals:
        dailyTotal += x[0]

    
    
    dailyTotalLabel = Label(root, text='Daily Total: ' + str(dailyTotal))
    dailyTotalLabel.place(x=SCREEN_WIDTH - 150, y=SCREEN_HEIGHT - 100)

def clearBatch():
    confirmClearbatch = Toplevel()
    confirmClearbatch.title("CONFIRM NEW BATCH")

    cancelButton = Button(confirmClearbatch, text="Cancel", command=lambda:cancelNewBatch(confirmClearbatch))
    confirmButton = Button(confirmClearbatch, text="Confirm", command=lambda:deleteBatch(confirmClearbatch))

    cancelButton.grid(row=0, column=0)
    confirmButton.grid(row=0, column=1)

def cancelNewBatch(window):
    window.destroy()

def deleteBatch(window):
    cursor.execute("DELETE FROM dailyBatch")
    conn.commit()
    window.destroy()



root.mainloop()