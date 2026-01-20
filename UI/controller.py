import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_create_graph(self, e):
        try:
            self._view.txt_result.controls.clear()
            n_alb = int(self._view.txtNumAlbumMin.value)
            if n_alb < 0:
                self._view.show_alert(f'Valore inserito non valido')
            else:
                self._model.load_all_artists(n_alb=n_alb)
                nodi,archi = self._model.build_graph()
                self._view.txt_result.controls.append(ft.Text(f'Grafo creato: {nodi} nodi (artistti), {archi} archi'))
                self.populate_dd()
                self._view.ddArtist.disabled = False
                self._view.btnArtistsConnected.disabled = False
                self._view.update_page()

        except ValueError:
            self._view.show_alert(f'Valore inserito non valido')

    def populate_dd(self):
        self._view.ddArtist.options.clear()
        if self._model._artists:
            for artist_id in self._model._artists:

                artista = self._model._artists[artist_id]
                self._view.ddArtist.options.append(ft.dropdown.Option(text=artista.name, key=artist_id))
            self._view.update_page()

    def handle_connected_artists(self, e):
        try:
            artist_id = int(self._view.ddArtist.value)
            collegati = self._model.artisti_collegati(artist_id)
            for conesso,peso in collegati:

                self._view.txt_result.controls.append(ft.Text(f'{conesso.id}, {conesso.name} numero generi in comune {peso}'))
            self._view.txtMinDuration.disabled = False
            self._view.txtMaxArtists.disabled = False
            self._view.btnSearchArtists.disabled = False
            self._view.update_page()

        except ValueError:
            self._view.show_alert(f'Valore inserito non valido')

    def handle_ricerca(self,e):
        try:
            durata = float(self._view.txtMinDuration.value)
            artist_id = int(self._view.txtMaxArtists.value)
            num_art= int(self._view.txtMaxArtists.value)
            if num_art < 0 or num_art>len(self._model._artists):
                self._view.show_alert(f'Valore inserito non valido')
            self._view.txt_result.controls.clear()
            sol = self._model.ricerca_cammino(durata,num_art,artist_id)
            for i in sol:
                self._view.txt_result.controls.append(ft.Text(f'{i}'))
        except ValueError:
            self._view.show_alert(f'Valore inserito non valido')
