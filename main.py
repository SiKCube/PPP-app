import random
from datetime import datetime
import sqlite3 as sql
from kivy.storage.jsonstore import JsonStore
from kivymd.app import MDApp
from kivymd.toast import toast
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty, ListProperty
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivy.uix.spinner import Spinner
from kivymd.uix.button import MDFillRoundFlatIconButton
from kivymd.uix.list import IconRightWidget, ThreeLineRightIconListItem
from kivymd.uix.expansionpanel import MDExpansionPanelThreeLine, MDExpansionPanel


def notificar(text):
    return toast(text)


ads_on = False


class MainWid(ScreenManager):
    # datos de las etiquetas
    partidas = StringProperty('')
    victorias = StringProperty('')
    derrotas = StringProperty('')
    abandonos = StringProperty('')
    dl = StringProperty('')
    tr = StringProperty('')
    ac = StringProperty('')
    r_dl = StringProperty('')
    r_tr = StringProperty('')
    r_victorias = StringProperty('')
    r_derrotas = StringProperty('')

    # datos de los spinners
    lista_de_nombres = ListProperty([])

    # top data list
    top_name = StringProperty('')

    # datos de los puntajes
    score_a = 0
    score_r = 0

    # hizo el tripe o doble?
    dobles = []
    triples = []
    aces = []

    def delete(self, instance):
        dialog = MDDialog(title=f"Eliminar partida?",
                          text="No se van recuperar los datos",
                          md_bg_color="#281332",
                          buttons=[
                              MDRaisedButton(text="ELIMINAR",
                                             on_press=lambda *args: (eliminar(), dialog.dismiss())),
                              MDRaisedButton(text="Cancelar",
                                             on_press=lambda *args: dialog.dismiss())
                          ])
        dialog.open()

        def eliminar():
            conn = sql.connect("score_front_ppp.db")
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM data_partidas")
            datos = cursor.fetchall()
            parent = instance.parent.parent.parent

            parent.parent.remove_widget(parent)

            for i in datos:
                if i[18] == instance.parent.parent.text:
                    cursor.execute(
                        f"DELETE FROM data_partidas WHERE fecha='{instance.parent.parent.text}'")
            conn.commit()
            conn.close()

    def random_vs(self):
        delantero_t1 = self.ids.lista_t1_p1
        trasero_t1 = self.ids.lista_t1_p2
        delantero_t2 = self.ids.lista_t2_p1
        trasero_t2 = self.ids.lista_t2_p2

        seleccionados = [delantero_t1.text, trasero_t1.text,
                         delantero_t2.text, trasero_t2.text]

        if "Delantero?" in seleccionados or "Zaguero?" in seleccionados:
            notificar("Falta data")

        else:
            listo = False

            while not listo:
                delantero_t1.text = seleccionados[random.randint(
                    0, len(seleccionados) - 1)]
                trasero_t1.text = seleccionados[random.randint(
                    0, len(seleccionados) - 1)]
                delantero_t2.text = seleccionados[random.randint(
                    0, len(seleccionados) - 1)]
                trasero_t2.text = seleccionados[random.randint(
                    0, len(seleccionados) - 1)]

                sel_final = [delantero_t1.text, trasero_t1.text,
                             delantero_t2.text, trasero_t2.text]
                if len(sel_final) == len(set(sel_final)):
                    listo = True

    def change_screen(self, screen):
        self.transition.direction = 'down'
        self.current = screen

    def menu_sel(self):
        menu = self.ids.menu_drop
        menu.values = self.lista_de_nombres
        entrada = self.ids.player_name

        entrada.text = menu.text

    def menu_res(self):
        menu = self.ids.menu_drop
        entrada = self.ids.player_name

        entrada.text = ""
        menu.text = ""

    def lista_on(self):
        lista = self.ids.lista
        conn = sql.connect("score_front_ppp.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM data_partidas")
        datos = cursor.fetchall()
        lista.clear_widgets()

        self.top_name = f"Canchas: {len(datos)}"

        for i in datos:
            drop = ThreeLineRightIconListItem(
                text=f"{i[18]}",
                secondary_text=f"Dobles: {i[4] + i[5]} | Triples: {i[8] + i[9]} | ACES: {i[12] + i[13]}",
                tertiary_text=f"Dobles: {i[6] + i[7]} | Triples: {i[10] + i[11]} | ACES: {i[14] + i[15]}",
            )

            drop.add_widget(IconRightWidget(
                icon="delete", on_release=self.delete))

            lista.add_widget(MDExpansionPanel(
                icon="logo.png",
                content=drop,
                panel_cls=MDExpansionPanelThreeLine(
                    text=f"{i[16]} / {i[17]}",
                    secondary_text=f"{i[0]} | {i[1]}",
                    tertiary_text=f"{i[2]} | {i[3]}"
                )
            ))

    def limpiar_jugadores(self):
        dialog = MDDialog(title="Vaciar jugadores?", text="No se van a recuperar los datos",
                          buttons=[
                              MDRaisedButton(text="Limpiar",
                                             on_press=lambda *args: (eliminar(), dialog.dismiss())),
                              MDRaisedButton(text="Cancelar",
                                             on_press=lambda *args: dialog.dismiss())
                          ])
        dialog.open()

        def eliminar():
            delantero_t1 = self.ids.lista_t1_p1
            trasero_t1 = self.ids.lista_t1_p2
            delantero_t2 = self.ids.lista_t2_p1
            trasero_t2 = self.ids.lista_t2_p2

            conn = sql.connect("score_front_ppp.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM jugadores")
            conn.commit()
            conn.close()

            self.lista_de_nombres.clear()
            self.seleccionar_equipos()

            delantero_t1.values = self.lista_de_nombres
            trasero_t1.values = self.lista_de_nombres
            delantero_t2.values = self.lista_de_nombres
            trasero_t2.values = self.lista_de_nombres

            delantero_t1.text = "delantero?"
            trasero_t1.text = "trasero?"
            delantero_t1.text = "delantero?"
            trasero_t2.text = "trasero?"

        return dialog

    def limpiar_partidas(self):
        dialog = MDDialog(title="Vaciar Partidas?", text="No se van a recuperar los datos",
                          buttons=[
                              MDRaisedButton(text="Vaciar",
                                             on_press=lambda *args: (eliminar(), dialog.dismiss())),
                              MDRaisedButton(text="Cancelar",
                                             on_press=lambda *args: dialog.dismiss())
                          ])
        dialog.open()

        def eliminar():
            conn = sql.connect("score_front_ppp.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM data_partidas")
            conn.commit()
            conn.close()

        return dialog

    # crear base de datos
    def crear_db(self):
        try:
            self.players = JsonStore('players.json')
            self.games = JsonStore('games.json')
        except Exception as e:
            print(e)
        try:
            conn = sql.connect("score_front_ppp.db")
            cursor = conn.cursor()
            cursor.execute(""" CREATE TABLE IF NOT EXISTS jugadores (
                Nombre TEXT PRIMARY KEY,
                Partidas INTEGER,
                Victorias INTEGER,
                Derrotas INTEGER,
                Abandonos INTEGER,
                Dobles INTEGER,
                Triples INTEGER,
                Aces INTEGER)""")

            cursor.execute(""" CREATE TABLE IF NOT EXISTS data_partidas (
                delantero_t1 TEXT,
                trasero_t1 TEXT, 
                delantero_t2 TEXT,
                trasero_t2 TEXT,
                delantero_t1_dl INTEGER,
                trasero_t1_dl INTEGER,
                delantero_t2_dl INTEGER,
                trasero_t2_dl INTEGER,
                delantero_t1_tr INTEGER,
                trasero_t1_tr INTEGER,
                delantero_t2_tr INTEGER,
                trasero_t2_tr INTEGER,
                delantero_t1_ac INTEGER,
                trasero_t1_ac INTEGER,
                delantero_t2_ac INTEGER,
                trasero_t2_ac INTEGER,
                puntos_t1 INTEGER,
                puntos_t2 INTEGER,    
                fecha)""")
            conn.commit()
            conn.close()
            self.seleccionar_equipos()
            self.current = 'nav'
            self.transition.direction = 'left'
        except sql.Error as e:
            notificar(str(e))

    def iniciar_cancelar(self):
        tb_a = self.ids.tablero_a
        tb_r = self.ids.tablero_r
        p_a = self.ids.poit_a
        p_r = self.ids.poit_r
        p_r_neg = self.ids.poit_r_neg
        p_a_neg = self.ids.poit_a_neg
        delantero_t1 = self.ids.lista_t1_p1
        trasero_t1 = self.ids.lista_t1_p2
        delantero_t2 = self.ids.lista_t2_p1
        trasero_t2 = self.ids.lista_t2_p2
        i_c = self.ids.iniciar_cancelar
        r_b = self.ids.random_b

        if i_c.icon == "racquetball":
            seleccionados = [delantero_t1.text, trasero_t1.text,
                             delantero_t2.text, trasero_t2.text]

            if delantero_t1.text == 'Delantero?' or delantero_t2.text == 'Delantero?' or trasero_t1.text == 'Zaguero?' or trasero_t2.text == 'Zaguero?':
                notificar('Falta introducir datos')
            elif not len(seleccionados) == len(set(seleccionados)):
                notificar('Un jugador esta repetido')
            else:
                tb_a.disabled = False
                tb_r.disabled = False
                p_r.disabled = False
                p_a.disabled = False
                p_r_neg.disabled = False
                p_a_neg.disabled = False
                delantero_t1.disabled = True
                trasero_t1.disabled = True
                delantero_t2.disabled = True
                trasero_t2.disabled = True
                i_c.icon = "cancel"
                r_b.disabled = True

        elif i_c.icon == "cancel":
            tb_r.disabled = True
            tb_a.disabled = True
            p_r.disabled = True
            p_a.disabled = True
            p_a_neg.disabled = True
            p_r_neg.disabled = True
            delantero_t1.disabled = False
            trasero_t1.disabled = False
            delantero_t2.disabled = False
            trasero_t2.disabled = False
            i_c.icon = "racquetball"
            r_b.disabled = False

            self.score_a = 0
            self.score_r = 0
            tb_r.text = '0'
            tb_a.text = '0'
            self.triples.clear()
            self.dobles.clear()
            self.aces.clear()
        else:
            notificar("ERROR de inicio")

    def punto_a(self):
        tb_a = self.ids.tablero_a
        tb_r = self.ids.tablero_r
        r_b = self.ids.random_b
        i_c = self.ids.iniciar_cancelar

        cas = self.ids.casual

        self.score_a += 1
        tb_a.text = str(self.score_a)

        if cas.active:
            const = 18
        else:
            const = 21

        if self.score_a >= const:
            self.score_a = const
            self.puntos_victoria(self.score_r, self.score_a)
            notificar(f'El equipo azul gano a {self.score_a} a {self.score_r}')

            self.score_a = 0
            self.score_r = 0
            tb_a.disabled = True
            tb_r.disabled = True
            r_b.disabled = False
            tb_r.text = '0'
            tb_a.text = '0'

            i_c.icon = "racquetball"

    def neg_punto_a(self):
        tb_a = self.ids.tablero_a
        self.score_a -= 1
        tb_a.text = str(self.score_a)
        if self.score_a <= 0:
            self.score_a = 0
            tb_a.text = str(self.score_a)
            notificar('Como que quieres que esten en negativos?!')

    def punto_r(self):
        tb_a = self.ids.tablero_a
        tb_r = self.ids.tablero_r
        r_b = self.ids.random_b
        i_c = self.ids.iniciar_cancelar

        cas = self.ids.casual

        self.score_r += 1
        tb_r.text = str(self.score_r)

        if cas.active:
            const = 18
        else:
            const = 21

        if self.score_r >= const:
            self.score_r = const
            self.puntos_victoria(self.score_r, self.score_a)
            notificar(f'El equipo rojo gano a {self.score_a} a {self.score_r}')

            self.score_r = 0
            self.score_a = 0
            tb_a.disabled = True
            tb_r.disabled = True
            r_b.disabled = False
            tb_a.text = '0'
            tb_r.text = '0'
            i_c.icon = "racquetball"

    def neg_punto_r(self):
        tb_r = self.ids.tablero_r
        self.score_r -= 1
        tb_r.text = str(self.score_r)
        if self.score_r <= 0:
            self.score_r = 0
            tb_r.text = str(self.score_r)
            notificar('Como que quieres que esten en negativos?!')

    def doble(self):
        tb_a = self.ids.tablero_a
        tb_r = self.ids.tablero_r

        delantero_t1 = self.ids.lista_t1_p1
        trasero_t1 = self.ids.lista_t1_p2
        delantero_t2 = self.ids.lista_t2_p1
        trasero_t2 = self.ids.lista_t2_p2

        jugando = [delantero_t1.text, trasero_t1.text,
                   delantero_t2.text, trasero_t2.text]

        mar_d = MDFillRoundFlatIconButton(icon="numeric-2-box", text="+",
                                          on_release=lambda *args: anotar_dle())

        mar_t = MDFillRoundFlatIconButton(icon="numeric-3-box", text="+",
                                          on_release=lambda *args: anotar_tr())

        aces_b = MDFillRoundFlatIconButton(icon="cards-playing", text="+",
                                           on_press=lambda *args: anotar_aces())

        menu = Spinner(text="Quien lo hizo?", values=jugando)

        dialogo1 = MDDialog(
            title="Que tipo de punto?",
            type="custom",
            md_bg_color="#281332",
            content_cls=MDBoxLayout(
                menu,
                padding=20,
                orientation='vertical',
                size_hint_y=None,
                height='60dp'
            ),
            buttons=[aces_b, mar_t, mar_d]
        )
        dialogo1.open()

        def anotar_dle():
            if not menu.text == "Quien lo hizo?":
                self.dobles.append(menu.text)
                dialogo1.dismiss()

                if delantero_t1.text == menu.text or trasero_t1.text == menu.text:
                    tb_a.text = str(self.score_a + 2)
                    self.score_a += 2
                    notificar(f"{menu.text} metio un doble!")
                    menu.text = "Quien lo hizo?"

                elif delantero_t2.text == menu.text or trasero_t2.text == menu.text:
                    tb_r.text = str(self.score_r + 2)
                    self.score_r += 2
                    notificar(f"{menu.text} metio un doble!")

            else:
                notificar('Falta quien hizo el doble?')

        def anotar_tr():
            if not menu.text == "Quien lo hizo?":
                self.triples.append(menu.text)
                dialogo1.dismiss()

                if delantero_t1.text == menu.text or trasero_t1.text == menu.text:
                    tb_a.text = str(self.score_a + 3)
                    self.score_a += 3
                    notificar(f"{menu.text} metio un triple!")
                    menu.text = "Quien lo hizo?"

                elif delantero_t2.text == menu.text or trasero_t2.text == menu.text:
                    tb_r.text = str(self.score_r + 3)
                    self.score_r += 3
                    notificar(f"{menu.text} metio un triple!")
                    menu.text = "Quien lo hizo?"

            else:
                notificar('Quien hizo el triple?!')

        def anotar_aces():
            if not menu.text == "Quien lo hizo?":
                self.aces.append(menu.text)
                dialogo1.dismiss()

                if delantero_t1.text == menu.text or trasero_t1.text == menu.text:
                    tb_a.text = str(self.score_a + 1)
                    self.score_a += 1
                    notificar(f"{menu.text} A la primera!")
                    menu.text = "Quien lo hizo?"

                elif delantero_t2.text == menu.text or trasero_t2.text == menu.text:
                    tb_r.text = str(self.score_r + 1)
                    self.score_r += 1
                    notificar(f"{menu.text} A la primera!")
                    menu.text = "Quien lo hizo?"

            else:
                notificar('Quien hizo ACES!?')

        return dialogo1

    # datos de partidas
    def puntos_victoria(self, entrada_r, entrada_a):
        delantero_t1 = self.ids.lista_t1_p1
        trasero_t1 = self.ids.lista_t1_p2
        delantero_t2 = self.ids.lista_t2_p1
        trasero_t2 = self.ids.lista_t2_p2

        p_r_neg = self.ids.poit_r_neg
        p_a_neg = self.ids.poit_a_neg

        seleccionados = [delantero_t1.text, trasero_t1.text,
                         delantero_t2.text, trasero_t2.text]

        ganadores = []
        perdedores = []

        if entrada_r > entrada_a or entrada_r < entrada_a:
            if entrada_r > entrada_a:
                ganadores = [delantero_t2.text, trasero_t2.text]
                perdedores = [delantero_t1.text, trasero_t1.text]
            elif entrada_a > entrada_r:
                ganadores = [delantero_t1.text, trasero_t1.text]
                perdedores = [delantero_t2.text, trasero_t2.text]

            conn = sql.connect('score_front_ppp.db')
            cursor = conn.cursor()

            for i in seleccionados:
                data = self.players.get(i)
                self.players.put(data.get('name'),
                                 partidas=data.get('partidas') + 1)

            for i in ganadores:
                data = self.players.get(i)
                self.players.put(data.get('name'),
                                 victorias=data.get('victorias') + 1)
            ganadores.clear()

            for i in perdedores:
                data = self.players.get(i)
                self.players.put(data.get('name'),
                                 derrotas=data.get('derrotas') + 1)
            perdedores.clear()

            delantero_t1_dl = 0
            trasero_t1_dl = 0
            delantero_t2_dl = 0
            trasero_t2_dl = 0

            for i in self.dobles:
                data = self.players.get(i)
                self.players.put(data.get('name'),
                                 dobles=data.get('dobles') + 1)
                if i == delantero_t1.text:
                    delantero_t1_dl += 1
                elif i == trasero_t1.text:
                    trasero_t1_dl += 1
                elif i == delantero_t2.text:
                    delantero_t2_dl += 1
                elif i == trasero_t2.text:
                    trasero_t2_dl += 1

            delantero_t1_tr = 0
            trasero_t1_tr = 0
            delantero_t2_tr = 0
            trasero_t2_tr = 0

            for i in self.triples:
                data = self.players.get(i)
                self.players.put(data.get('name'),
                                 triples=data.get('triples') + 1)
                if i == delantero_t1.text:
                    delantero_t1_tr += 1
                elif i == trasero_t1.text:
                    trasero_t1_tr += 1
                elif i == delantero_t2.text:
                    delantero_t2_tr += 1
                elif i == trasero_t2.text:
                    trasero_t2_tr += 1

            delantero_t1_ac = 0
            trasero_t1_ac = 0
            delantero_t2_ac = 0
            trasero_t2_ac = 0

            for i in self.aces:
                data = self.players.get(i)
                self.players.put(data.get('name'), aces=data.get('aces') + 1)
                if i == delantero_t1.text:
                    delantero_t1_ac += 1
                elif i == trasero_t1.text:
                    trasero_t1_ac += 1
                elif i == delantero_t2.text:
                    delantero_t2_ac += 1
                elif i == trasero_t2.text:
                    trasero_t2_ac += 1
            perdedores.clear()

            _i = 1
            while True:
                if _i in self.players:
                    _i += 1
                else:
                    break
            self.games.put(_i,
                           delantero_equipo1=delantero_t1.text,
                           trasero_equipo1=trasero_t1.text,
                           delantero_equipo2=delnatero_t2.text,
                           trasero_equipo2=trasero_t2.text,
                           delantero_equipo1_dobles=delantero_t1_dl,
                           trasero_equipo1_dobles=trasero_t1_dl,
                           delantero_equipo2_dobles=delantero_t2_dl,
                           trasero_equipo2_dobles=trasero_t2_dl,
                           delantero_equipo1_triples=delantero_t1_tr,
                           trasero_equipo1_triples=trasero_t1_tr,
                           delantero_equipo2_triples=delantero_t2_tr,
                           trasero_equipo2_triples=trasero_t2_tr,
                           delantero_equipo1_aces=trasero_t1_ac,
                           trasero_equipo1_aces=trasero_t1_ac,
                           delantero_equipo2_aces=delantero_t2_ac,
                            
                           )
            instruccion = f"""INSERT INTO data_partidas VALUES (
                            '{delantero_t1.text}',
                            '{trasero_t1.text}',
                            '{delantero_t2.text}',
                            '{trasero_t2.text}',
                            {delantero_t1_dl},
                            {trasero_t1_dl},
                            {delantero_t2_dl},
                            {trasero_t2_dl},
                            {delantero_t1_tr},
                            {trasero_t1_tr},
                            {delantero_t2_tr},
                            {trasero_t2_tr},
                            {delantero_t1_ac},
                            {trasero_t1_ac},
                            {delantero_t2_ac},
                            {trasero_t2_ac},
                            {entrada_a},
                            {entrada_r},
                            '{datetime.today().strftime('%d/%m/%Y %H:%M')}')"""
            cursor.execute(instruccion)

            conn.commit()
            conn.close()

            tb_r = self.ids.poit_r
            tb_a = self.ids.poit_a

            delantero_t1.disabled = False
            delantero_t2.disabled = False
            trasero_t1.disabled = False
            trasero_t2.disabled = False
            tb_a.disabled = True
            tb_r.disabled = True
            p_r_neg.disabled = True
            p_a_neg.disabled = True

        else:
            notificar('No estan permitidos los empates')

    # nuevo jugador
    def nuevo_jugador(self):
        entrada = self.ids.player_name

        if entrada.text == '' or ' ' in entrada.text:
            notificar('Los espacios en blanco no estan permitidos')

        elif len(entrada.text) >= 10:
            notificar('Pasaste el limite de caracteres!')

        else:
            if not entrada.text in self.players:

                self.players.put(entrada.text, name=entrada.text, partidas=0,
                                 victorias=0, derrotas=0, abandonos=0, dobles=0, triples=0, aces=0)

                self.seleccionar_equipos()
                notificar(f"{entrada.text} entro al juego!")
            else:
                notificar(f'El jugador {entrada.text} ya existe')
            entrada.text = ""

    # renombrar jugador
    def renombrar_jugador(self):
        entrada = self.ids.player_name

        if entrada.text == '' or ' ' in entrada.text:
            notificar('Los espacios en blanco no estan permitidos')
        else:
            if entrada.text in self.players:
                renombrar_b = MDRaisedButton(text="Renombrar",
                                             on_release=lambda *args: anotar_ren())
                cancelar_b = MDRaisedButton(text="Cancelar",
                                            on_release=lambda *args: dialogo1.dismiss())

                ren_entrada = MDTextField(
                    hint_text=f"Nuevo nombre de {entrada.text}")

                dialogo1 = MDDialog(
                    title="Nuevo nombre?",
                    type="custom",
                    md_bg_color="#281332",
                    content_cls=MDBoxLayout(
                        ren_entrada,
                        orientation='vertical',
                        size_hint_y=None,
                        height='60dp'
                    ),

                    buttons=[renombrar_b, cancelar_b]

                )
                dialogo1.open()

                def anotar_ren():
                    if ren_entrada.text == '' or ' ' in ren_entrada.text:
                        notificar(
                            'Los espacios en blanco no estan permitidos')
                    elif ren_entrada.text == entrada.text:
                        notificar(
                            "Porque quieres renombrar al mismo nombre?!")
                    else:
                        if not ren_entrada.text in self.players:
                            transf = self.players.get(entrada.text)
                            self.players.delete(entrada.text)
                            self.players.put(ren_entrada.text,
                                             name=ren_entrada.text,
                                             partidas=transf.get('name'),
                                             victorias=transf.get('victorias'),
                                             derrotas=transf.get('derrotas'),
                                             abandonos=transf.get('abandonos'),
                                             dobles=transf.get('dobles'),
                                             triples=transf.get('triples'),
                                             aces=transf.get('aces'))
                            dialogo1.dismiss()
                            notificar(
                                f'Se renombro a {entrada.text} a {ren_entrada.text}')
                            entrada.text = ""
                        else:
                            notificar(
                                'El nombre seleccionado ya existe')

                        self.seleccionar_equipos()

                return dialogo1
            else:
                notificar(f'No esta un tal {entrada.text}')

    # eliminar un jugador
    def eliminar_jugador(self):
        entrada = self.ids.player_name

        dialog = MDDialog(title=f"Eliminar a {entrada.text}",
                          text="No se podra recuperar el perfil",
                          md_bg_color="#281332",
                          buttons=[
                              MDRaisedButton(text="ELIMINAR",
                                             on_press=lambda *args: (eliminar(), dialog.dismiss())),
                              MDRaisedButton(text="Cancelar",
                                             on_press=lambda *args: dialog.dismiss())
                          ])
        dialog.open()

        def eliminar():
            self.players.delete(entrada.text)

            self.seleccionar_equipos()
            entrada.text = ""

        return dialog

    # sumar un reporte
    def reportar(self):
        entrada = self.ids.player_name.text

        dialog = MDDialog(title="Reportar?", text=f"eguro que quieres reportar a {entrada}",
                          buttons=[
                              MDRaisedButton(text="Reportar",
                                             on_press=lambda *args: (report(), dialog.dismiss())),
                              MDRaisedButton(text="Cancelar",
                                             on_press=lambda *args: dialog.dismiss())
                          ])
        dialog.open()

        def report():
            if entrada in self.players:
                bad = self.players.get(entrada)['abandonos']
                self.players.put(entrada, abandonos=bad + 1)

                self.seleccionar_equipos()
                notificar(f'Se a sumado un abandono a: {entrada}')
            else:
                notificar('No hay a quien reportar')

        return dialog

    # enseñar datos del perfil
    def perfil_info(self):
        entrada = self.ids.player_name.text

        if not ' ' in entrada:
            if entrada is self.players:
                self.ids.fondo_icon.opacity = 1
                self.ids.datas.opacity = 0
            else:
                self.ids.fondo_icon.opacity = 0
                self.ids.datas.opacity = 1
                p = self.partidas.get(entrada)['partidas']
                self.partidas = f"Partidas echas: {p}"

                v = self.partidas.get(entdraa)['victorias']
                self.victorias = f"Victorias echas: {v}"

                d = self.partidas.get(entrada)['derrotas']
                self.derrotas = f"Derrotas echas: {d}"

                if v == 0:
                    self.r_victorias = "FALTA DATA"
                else:
                    self.r_victorias = f"{round(v / p, 2)}"
                if d == 0:
                    self.r_derrotas = "FALTA DATA"
                else:
                    self.r_derrotas = f"{round(d / p, 2)}"

                self.abandonos = f"Partidas abandonadas: {self.partidas.get(entrada)['abandonos']}"

                self.dl = f"Doble anotados: {self.partidas.get(entrada)['dobles']}"

                self.tr = f"Triples anotados: {self.partidas.get(entrada)['triples']}"

                self.ac = f"ACES anotados: {self.partidas.get(entrada)['aces']}"
# =================================complete this to json!\/\/\/\/\/=========================================================
# =================================#=================================#=================================
# =================================#=================================#=================================
                cursor.execute(f"SELECT * FROM data_partidas")
                datos = cursor.fetchall()

                data_dl = []
                data_tr = []

                for i in datos:
                    if i[0] == entrada:
                        data_dl.append(round((int(i[4]) * 2) / 18, 2))
                        data_tr.append(round((int(i[8]) * 3) / 18, 2))
                    elif i[1] == entrada:
                        data_dl.append(round((int(i[5]) * 2) / 18, 2))
                        data_tr.append(round((int(i[9]) * 3) / 18, 2))
                    elif i[2] == entrada:
                        data_dl.append(round((int(i[6]) * 2) / 18, 2))
                        data_tr.append(round((int(i[10]) * 3) / 18, 2))
                    elif i[3] == entrada:
                        data_dl.append(round((int(i[7]) * 2) / 18, 2))
                        data_tr.append(round((int(i[11]) * 3) / 18, 2))

                count = 0
                result = 0
                for i in data_dl:
                    count += 1
                    result = i + result
                if result <= 0:
                    self.r_dl = "0"
                else:
                    self.r_dl = str(round(result / count, 2))

                count = 0
                result = 0
                for i in data_tr:
                    count += 1
                    result = i + result
                if result <= 0:
                    self.r_tr = "0"
                else:
                    self.r_tr = str(round(result / count, 2))

        else:
            notificar('No se permiten espacios en blanco')

    def seleccionar_equipos(self):
        menu_drop = self.ids.menu_drop

        conn = sql.connect("score_front_ppp.db")
        cursor = conn.cursor()
        cursor.execute("SELECT Nombre FROM jugadores")
        datos = cursor.fetchall()

        self.lista_de_nombres.clear()
        for i in datos:
            self.lista_de_nombres.append(i[0])

        menu_drop.values = self.lista_de_nombres

        conn.commit()
        conn.close()


class MainApp(MDApp):
    seg = 0
    min = 0

    def build(self):
        self.theme_cls.primary_palette = "Teal"

        """['Red', 'Pink', 'Purple', 'DeepPurple', 'Indigo', 'Blue', 'LightBlue', 'Cyan', 'Teal', 'Green', 'LightGreen',
         'Lime', 'Yellow', 'Amber', 'Orange', 'DeepOrange', 'Brown', 'Gray', 'BlueGray']"""

        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.material_style = "M3"

        return MainWid()

    def time_on(self):
        evento = Clock.schedule_interval(self.timer, 1)

        self.seg = 0
        self.min = 0

    def timer(self, xdt):
        self.seg += 1
        if self.seg > 60:
            self.seg = 0
            self.min += 1

        if self.seg <= 9:
            seg_str = f"0{self.seg}"
        else:
            seg_str = self.seg

        if self.min <= 9:
            min_str = f"0{self.min}"
        else:
            min_str = self.min

        root = self.get_running_app().root
        contador = root.ids.corm
        contador.text = f"{min_str}:{seg_str}"


if __name__ == '__main__':
    MainApp().run()
