
#LIBRERIAS
import customtkinter, os, minecraft_launcher_lib, subprocess, tkinter
from tkinter import messagebox
from PIL import Image

#OTROS
customtkinter.set_appearance_mode("dark")

#VALORES
user_windows = os.environ['USERNAME']
L_Version = "3.0 Stable"

#PERSONALIZAR
minecraft_directory = f"C://Users//{user_windows}//AppData//Roaming//.minecraft"

#OTHERS
versiones = minecraft_launcher_lib.utils.get_installed_versions(minecraft_directory)
todas_las_versiones = [version.get('id', 'N/A') for version in versiones]

#AVISO
print(f"Consola de desarrollador, favor de no cerrar esta pestaña.")
print("Codigo por Jakedev098, Keimasempai & Paulscode.")

#INTERFAZ
class RoundedComboboxFrame(customtkinter.CTkFrame): #VAR VERSIONS
    def __init__(self, master=None, width=100, height=10, **kwargs):
        super().__init__(master, width=width, height=height, **kwargs)

class App(customtkinter.CTk): #APP

    #RESOLUCION
    width = 900
    height = 600

    #IRSE A CONFIGURACION
    def conf_frame_event(self):
        self.MAIN_frame.grid_forget()
        self.conf_frame.grid(row=0, column=0, sticky="ns")

    #SUGERENCIAS VERSIONES
    def actualizar_sugerencias(self):
        try:
            self.combobox_version['values'] = self.todas_las_versiones
        except:
            self.combobox_version['values'] = "NAN"

    #IRSE AL MENU (FRAME)
    def men_event(self):
        self.conf_frame.grid_forget()
        self.ins_frame.grid_forget()
        self.MAIN_frame.grid(row=0, column=0, sticky="ns")
    
    #MENSAJE DE INFO
    def inf_ung(self, mensaje=None):
        messagebox.showinfo("Informe!", mensaje)

    #IRSE A INSTALACION (FRAME)
    def install_minecraft(self):
        version_inst = self.combobox_version.get()
        if not version_inst:
            self.inf_ung("Por favor, ingresa una versión de Minecraft.")
            self.men_event()
        elif version_inst in todas_las_versiones:
            self.inf_ung(f"La versión {version_inst} ya está instalada.")
            self.men_event()
        elif version_inst == "¿Cual version seria?":
            self.inf_ung(f"Inserta una version Por favor.")
            self.men_event()
        else:
            try:
                self.inf_ung(f"Se está instalando la versión {version_inst}!")
                minecraft_launcher_lib.install.install_minecraft_version(version_inst, minecraft_directory)
                self.inf_ung(f"¡Se instaló correctamente la {version_inst}!")
                self.men_event()
            except Exception as e:
                self.inf_ung(f"¡Ha ocurrido un error!, asegurate de haber puesto bien la version!: {e}")
                return

    #INICIADOR
    def launch_event(self):
        mine_user = self.username_entry.get()
        mine_version = self.combobox_version.get()
        if not mine_version:
            self.inf_ung("Por favor, ingresa una versión de minecraft.")
            self.men_event()
        elif len(mine_user) < 4:
            self.inf_ung("El nombre de usuario debe tener al menos 4 caracteres.")
            self.men_event()
        elif not mine_user.isalnum():
            self.inf_ung("El nombre de usuario solo puede contener letras y números.")
            self.men_event()
        elif mine_user.isdigit():
            self.inf_ung("El nombre de usuario no puede consistir solo en números.")
            self.men_event()
        else:
            try:
                options = {
                    'username': mine_user,
                    'uuid': '',
                    'token': '',
                    'jvmArguments': ["-Xmx2G", "-Xms2G"]
                }
                try:
                    if 'forge' in mine_version.lower() or 'fabric' in mine_version.lower():
                        self.inf_ung(f"Se esta iniciando minecraft {mine_version}!, porfavor, no cierre el launcher.")
                    else:
                        self.inf_ung(f"Se esta iniciando minecraft {mine_version}!, porfavor, no cierre el launcher.")
                        minecraft_launcher_lib.install.install_minecraft_version(mine_version, minecraft_directory)
                    minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(mine_version, minecraft_directory, options)
                    self.destroy()
                    subprocess.run(minecraft_command)
                except Exception as e:
                    self.inf_ung(f"¡Ha ocurrido un error!, asegurate de haber puesto bien la version: {e}")
                    self.men_event()
            except Exception as e:
                self.inf_ung(f"¡Ha ocurrido un error! {e}")
                self.men_event()

    #INTERFAZ GRAFICA
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #DATOS BASICOS
        self.title(f"Jakecherry Launcher {L_Version}")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)
        current_path_ = os.path.dirname(os.path.realpath(__file__))
        self.iconbitmap(os.path.join(current_path_, "images", "logo.ico"))

        #BG
        current_path = os.path.dirname(os.path.realpath(__file__))
        self.bg_image = customtkinter.CTkImage(Image.open(current_path + "/images/bg.png"), size=(self.width, self.height))
        self.bg_image_label = customtkinter.CTkLabel(self, image=self.bg_image)
        self.bg_image_label.grid(row=0, column=0)

        #MAIN FRAME
        self.MAIN_frame = customtkinter.CTkFrame(self, corner_radius=50)
        self.MAIN_frame.grid(row=0, column=0, sticky="ns")
        self.MAIN_label = customtkinter.CTkLabel(self.MAIN_frame, text="Jakecherry's Launcher", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.MAIN_label.grid(row=0, column=0, padx=30, pady=(150, 15))
        self.username_entry = customtkinter.CTkEntry(self.MAIN_frame, width=200, placeholder_text="¿Usuario?")
        self.username_entry.grid(row=1, column=0, padx=30, pady=(15, 15))
        combobox_frame = RoundedComboboxFrame(self.MAIN_frame, width=210, height=31, corner_radius=10)
        combobox_frame.grid(row=2, column=0, padx=30, pady=(15, 15))
        self.combobox_version = tkinter.ttk.Combobox(self.MAIN_frame, values=todas_las_versiones, width=30)
        self.combobox_version.set("¿Cual version seria?")
        self.combobox_version['values'] = todas_las_versiones
        self.combobox_version.bind('<KeyRelease>', self.actualizar_sugerencias)
        self.combobox_version.grid(row=2, column=0, padx=30, pady=(15, 15))
        self.launch_button = customtkinter.CTkButton(self.MAIN_frame, text="Ejecutar", command=self.launch_event, width=200, height=32)
        self.launch_button.grid(row=3, column=0, padx=30, pady=(15, 15))
        self.install_button = customtkinter.CTkButton(self.MAIN_frame, text="Instalar", command=self.install_minecraft, width=200, height=32)
        self.install_button.grid(row=4, column=0, padx=30, pady=(15, 15))
        labelimain = customtkinter.CTkLabel(self.MAIN_frame, text=f"Jakecherry's Launcher\nHecho por JakeDev098/G047 & Jacobdev")
        labelimain.grid(row=11, column=0)

        #ICON
        image_path = os.path.join(current_path, "images", "icon.ico")
        bg_image = customtkinter.CTkImage(Image.open(image_path), size=(245, 254))
        image_label = customtkinter.CTkLabel(self.MAIN_frame, image=bg_image, text="")
        image_label.grid(row=0, column=0, sticky="nsew")

        #INSTALL MINECRAFT
        self.ins_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.ins_frame.grid_columnconfigure(0, weight=1)
        self.ins__label = customtkinter.CTkLabel(self.ins_frame, text="Jakecherry's\nInstalacion de minecraft", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.ins__label.grid(row=0, column=0, padx=30, pady=(30, 15))
        labelinst = customtkinter.CTkLabel(self.ins_frame, text="¡Se esta instalando la version de Minecraft que pediste!, Por favor espera.")
        labelinst.grid(row=4, column=0)
        self.back_button_ins = customtkinter.CTkButton(self.ins_frame, text="Back", command=self.men_event, width=200)
        self.back_button_ins.grid(row=9, column=0, padx=30, pady=(15, 15))

#RUN DOS RUN!
if __name__ == "__main__":
    app = App()
    app.mainloop()
