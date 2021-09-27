from tkinter import *
from tkinter import filedialog
import sqlite3

conn = sqlite3.connect('app.db')


cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS items(
        itemName text,
        itemPrice real,
        itemInventory int
)""")

root = Tk()
root.title("POS App")
root.geometry("975x650")

SCREEN_WIDTH, SCREEN_HEIGHT = 975, 650

rowChange = 0
columnChange = -1

newOrderPrice = 0
newOrderList = []

refreshButton = Button(root, text='Refresh', command=lambda:refresh())
refreshButton.place(x=SCREEN_WIDTH - 100, y=10)

newItemOpenWindow = Button(root, text="Add New Item", command=lambda:openItemWindow(), width=29, height=3)
newItemOpenWindow.grid(row=rowChange + 1, column=0, columnspan=2)

PlaceOrderButton = Button(root, text='Checkout', command=lambda:checkout())
PlaceOrderButton.place(x=SCREEN_WIDTH - 100, y=SCREEN_HEIGHT - 100)


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

    bookButton = Button(root, text=name + f'\n{price}', width=12, height=6, command=lambda:addItem(name, price))
    bookButton.grid(row=rowChange, column=columnChange, padx=10, pady=10)

    newItemOpenWindow.grid_configure(row=rowChange + 1, column=0, columnspan=2)
        
        


def addItem(name, price):
    global newOrderPrice
    newOrderPrice += price
    newOrderList.append(name)

    print(str(newOrderList) + ' ' + str(newOrderPrice))

    orderLabel = Label(root, text='Order: \n')
    orderLabel.place_forget()

    for item in newOrderList:
        orderLabel.configure(text=orderLabel.cget("text") + '\n' + item)
    
    orderLabel.configure(text=orderLabel.cget("text") + '\n Total:  ' + str(newOrderPrice))

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

    submitNewItemButton = Button(newItemWindow, text='Submit Item', width=20, command=lambda:submitNewItem(newItemEntry.get(), newItemPriceEntry.get(), None, newItemWindow))
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

    checkoutWindow = Toplevel()
    checkoutWindow.title("Checkout")

    orderLabel = Label(checkoutWindow, text='Order: \n', padx=10, pady=15)
    orderLabel.place_forget()

    for item in newOrderList:
        orderLabel.configure(text=orderLabel.cget("text") + '\n' + item)


    cashEntry = Entry(checkoutWindow)
    cashLabel = Label(checkoutWindow, text='Amount Paid:')
    submitPayButton = Button(checkoutWindow, text='Pay')
    orderTotalLabel = Label(checkoutWindow, text=str(newOrderPrice))

    cashLabel.grid(row=0, column=0)
    cashEntry.grid(row=0, column=1)
    submitPayButton.grid(row=1, column=0, columnspan=2)
    orderTotalLabel.grid(row=2, column=0, columnspan=2)

    orderLabel.grid(row=3, column=0, columnspan=2)




root.mainloop()