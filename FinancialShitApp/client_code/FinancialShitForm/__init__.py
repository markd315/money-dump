import json
import anvil.google.auth
from _template import FinancialShitTemplate
import anvil.server


class FinancialShitForm(FinancialShitTemplate):

    def __init__(self, **properties):
        login = anvil.google.auth.login()
        print(login)
        self.init_components_base(**properties)
        self.addHandlers()

    def get_lesson_click(self, **event_args):
        results = anvil.server.call('get_lesson', "sampleUnit", "sampleLesson")
        if results['type'] == 'text':
            self.instructional_text.text = results['data']
            self.instructional_text.visible = True
        else:
            self.instructional_text.visible = False
