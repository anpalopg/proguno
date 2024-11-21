import tkinter as tk
import mysql.connector
from tkinter import ttk
from tkinter import messagebox

# Barra de menú la de arribita
def barra_menu(root):
    barra_menu = tk.Menu(root)
    root.config(menu=barra_menu)

    menu_inicio = tk.Menu(barra_menu)
    barra_menu.add_cascade(label='Inicio', menu=menu_inicio)

    menu_inicio.add_command(label='Crear registro base de datos', command=crear_tabla)
    menu_inicio.add_command(label='Eliminar registro base de datos', command=borrar_tabla)
    menu_inicio.add_command(label='Salir', command=root.quit)  

    barra_menu.add_cascade(label='Consultas', menu=menu_inicio)
    barra_menu.add_cascade(label='Configuración', menu=menu_inicio)
    barra_menu.add_cascade(label='Ayuda', menu=menu_inicio)

# Clase Frame para la GUI 
class Frame(tk.Frame):
    def __init__(self, root=None):
        super().__init__(root)
        self.root = root
        self.pack()
        self.config(width=600, height=400, bg='gray')  
        self.titulo()
        self.listaA()
        self.listaB()
        self.listaC()
        self.insertarA()
        self.insertarB()
        self.insertarC()
        self.treeview() 
        self.botones_izquierda()
        self.botones_derecha()
        self.checkboxes()
        self.insertar_combobox()

    def titulo(self):
        self.label_titulo = tk.Label(self, text='FACTURACIÓN DE PRODUCTOS', bg='gray', fg='black')
        self.label_titulo.config(font=('Arial', 19, 'bold'))
        self.label_titulo.grid(row=0, column=0, columnspan=4, pady=15)  

    def listaA(self):
        self.label_listaA = tk.Label(self, text='Producto:', bg='gray', anchor="w")
        self.label_listaA.config(font=('Arial', 12,'bold'))
        self.label_listaA.grid(row=1, column=0, sticky="w", padx=10)

    def listaB(self):
        self.label_listaB = tk.Label(self, text='Cantidad:', bg='gray', anchor="w")
        self.label_listaB.config(font=('Arial', 12,'bold'))
        self.label_listaB.grid(row=2, column=0, sticky="w", padx=10)

    def listaC(self):
        self.label_listaC = tk.Label(self, text='Valor:', bg='gray', anchor="w")
        self.label_listaC.config(font=('Arial', 12,'bold'))
        self.label_listaC.grid(row=3, column=0, sticky="w", padx=10)

    def insertarA(self):
        self.textbox_insertarA = tk.Entry(self, width=30)
        self.textbox_insertarA.grid(row=1, column=1, padx=5)

    def insertarB(self):
        self.textbox_insertarB = tk.Entry(self, width=30)
        self.textbox_insertarB.grid(row=2, column=1, padx=5)

    def insertarC(self):
        self.textbox_insertarC = tk.Entry(self, width=30)
        self.textbox_insertarC.grid(row=3, column=1, padx=5)

    def botones_izquierda(self):
        self.button_agregar = tk.Button(self, text='Add', bg='pink', command=self.add_item)
        self.button_agregar.grid(row=4, column=1, padx=10, pady=5)

        self.button_limpiar = tk.Button(self, text='Clear', bg='pink', command=self.clear_treeview)
        self.button_limpiar.grid(row=4, column=0, padx=10, pady=5)

    def treeview(self):
        self.tree = ttk.Treeview(self, columns=("ID", "Producto", "Cantidad", "Precio", "Total"), show="headings", height=5)
        self.tree.grid(row=1, column=2, rowspan=4, columnspan=2, padx=10, pady=10, sticky="nsew")

        for col in ("ID", "Producto", "Cantidad", "Precio", "Total"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

    def botones_derecha(self):
        self.button_borrar = tk.Button(self, text='Delete', bg='pink', command=self.delete_item)
        self.button_borrar.grid(row=5, column=0, padx=10, pady=5)

        self.button_facturar = tk.Button(self, text='FACTURAR', bg='lightgreen', command=self.facturar)
        self.button_facturar.grid(row=6, column=3, padx=10, pady=5)

    def checkboxes(self):
        self.checkbox_var1 = tk.BooleanVar()
        self.checkbox1 = tk.Checkbutton(self, text="IVA", variable=self.checkbox_var1, bg='gray')
        self.checkbox1.grid(row=5, column=2, padx=10, pady=10)

        self.checkbox_var2 = tk.BooleanVar()
        self.checkbox2 = tk.Checkbutton(self, text="Sin IVA", variable=self.checkbox_var2, bg='gray')
        self.checkbox2.grid(row=5, column=3, padx=10, pady=10)

    def insertar_combobox(self):
        label_combobox = tk.Label(self, text="Selecciona una opción:")
        label_combobox.grid(row=6, column=0, padx=5, pady=5, sticky="e")

        self.combobox_combobox = ttk.Combobox(self, values=[":)", ":(", "<3", ":|",";)",":D","O_O"])#los emoji's
        self.combobox_combobox.grid(row=6, column=1, padx=5, pady=5)
        self.combobox_combobox.set(":)")  # Valor por defecto


    # Funcionalidad de los botones
    def add_item(self):
        producto = self.textbox_insertarA.get()
        cantidad = self.textbox_insertarB.get()
        precio = self.textbox_insertarC.get()

        if not producto or not cantidad or not precio:
            messagebox.showerror("Error", "Por favor, ingrese todos los datos.")
            return

        if not cantidad.isdigit():
            messagebox.showerror("Error", "Cantidad debe ser un número entero.")
            return

        try:
            cantidad = int(cantidad)
            precio = float(precio)
        except ValueError:
            messagebox.showerror("Error", "Precio debe ser un número válido.")
            return
        
        total = cantidad * precio

    
        self.tree.insert("", tk.END, values=("ID", producto, cantidad, precio, total)) 

        self.textbox_insertarA.delete(0, tk.END)
        self.textbox_insertarB.delete(0, tk.END)
        self.textbox_insertarC.delete(0, tk.END)

    def clear_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def delete_item(self):
        seleccion = self.tree.selection()
        if seleccion:
            for item in seleccion:
                self.tree.delete(item)
        else:
            messagebox.showerror("Error", "Seleccione un elemento para borrar.")


    def facturar(self):
         iva = self.checkbox_var1.get()  
         sin_iva = self.checkbox_var2.get()  
         seleccion_opcion = self.combobox_combobox.get() 

##aca si me toco usar chatgpt no sabia como sacar el iva :(
         total_factura = 0
         for item in self.tree.get_children():  
            valores = self.tree.item(item, "values")
            total_factura += float(valores[4])  

         if iva:
             total_factura *= 1.19  

    
         messagebox.showinfo("Facturar", f"Facturación completada con {'IVA' if iva else 'sin IVA'}.\nTotal: ${total_factura:.2f} {seleccion_opcion}")




# DESDE ACA ES LA BDD TOCA HACERLO DESDE EL MENU
class ConexionDB:
    def __init__(self):
        try:
            self.conexion = mysql.connector.connect(
                host="localhost",  
                user="root",       
                password="",      
                database="facturacion" 
            )
            self.cursor = self.conexion.cursor()
        except mysql.connector.Error as e:
            titulo = "Error en la conexión"
            mensaje = f"No se pudo conectar a la base de datos. Error: {e}"
            messagebox.showerror(titulo, mensaje)

    def ejecutar_sql(self, sql, valores=None):
        try:
            if valores:
                self.cursor.execute(sql, valores)
            else:
                self.cursor.execute(sql)
            self.conexion.commit()
        except mysql.connector.Error as e:
            titulo = "Error al ejecutar SQL"
            mensaje = f"No se pudo ejecutar la operación. Error: {e}"
            messagebox.showerror(titulo, mensaje)

    def cerrar(self):
        self.cursor.close()
        self.conexion.close()


def crear_tabla():
    conexion = ConexionDB()
    sql = """
    CREATE TABLE IF NOT EXISTS productos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(100),
        cantidad INT,
        precio DECIMAL(10, 2)
    )
    """
    conexion.ejecutar_sql(sql)
    conexion.cerrar()
    messagebox.showinfo("Base de datos", "Tabla de productos creada.")


def borrar_tabla():
    conexion = ConexionDB()
    sql = "DROP TABLE IF EXISTS productos"
    conexion.ejecutar_sql(sql)
    conexion.cerrar()
    messagebox.showinfo("Base de datos", "Tabla de productos eliminada.")


