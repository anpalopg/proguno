import tkinter as tk
from producto.gui_app import Frame, barra_menu  

def main():
    root = tk.Tk()
    root.title('FACTURACION')
    barra_menu(root)  # MENU
    app = Frame(root)  #  clase Frame 
     


     
    root.mainloop()  

if __name__ == '__main__':
    main()
