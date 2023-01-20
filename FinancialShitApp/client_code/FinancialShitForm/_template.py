import datetime

import anvil
from anvil import *


class FinancialShitTemplate(HtmlPanel):

    def init_components_base(self, **properties):
        super().__init__()
        self.clear()
        self.html = '@theme:standard-page.html'
        self.content_panel = GridPanel()
        self.add_component(self.content_panel)
        self.title_label = Label(text="Financial Shit", font_size=24)
        self.add_component(self.title_label, slot="title")

        self.card_1 = GridPanel(role="card")
        self.content_panel.add_component(self.card_1, row="D", col_sm=2,
                                         width_sm=8)

        self.main_content = FlowPanel(align="center")
        self.card_1.add_component(self.main_content,
                                  row="A", col_sm=2, width_sm=10)
        self.instructional_text = Label(text="preloaded")
        self.load_instructions = Button(text="Load instructions", role='primary-color')
        self.ctl_all = {self.instructional_text, self.load_instructions}
        for component in self.ctl_all:
            self.addComponent(component)
        self.showAll(self.ctl_all)

    def showAll(self, components):
        for component in self.ctl_all:
            component.visible = False
        for component in components:
            component.visible = True

    def addComponent(self, component):
        try:
            component.remove_from_parent()
        except BaseException:
            pass
        component.visible = True
        self.main_content.add_component(component)

    def addHandlers(self):
        if hasattr(self, "load_instructions"):
            self.load_instructions.set_event_handler('click', self.get_lesson_click)
