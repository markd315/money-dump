import json
import anvil.google.auth
import anvil.server
from anvil import HtmlPanel

from ..HeaderPanel import HeaderPanel


class FinancialShitForm(HtmlPanel):

    def __init__(self, **properties):
        #self.init_components(**properties)

        header_panel = HeaderPanel()
        self.add_component(header_panel)

        login = anvil.google.auth.login()
        print(login)
        self.addHandlers()
