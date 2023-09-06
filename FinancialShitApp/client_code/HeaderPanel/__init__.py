from anvil import open_form, ColumnPanel, Button


class HeaderPanel(ColumnPanel):

    def __init__(self, **properties):
        super().__init__(**properties)

        self.button_home = Button(text="Home")
        self.add_component(self.button_home)
        self.button_home.set_event_handler('click', self.button_home_click)

        self.button_evaluation = Button(text="Evaluation")
        self.add_component(self.button_evaluation)
        self.button_evaluation.set_event_handler('click', self.button_evaluation_click)


    def button_home_click(self, **event_args):
        open_form('FinancialShitForm')

    def button_evaluation_click(self, **event_args):
        open_form('EvaluationForm')