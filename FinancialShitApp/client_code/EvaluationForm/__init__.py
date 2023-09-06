import json
import anvil.google.auth
import anvil.server
from anvil import HtmlPanel, Label, RadioButtonGroup, Button, alert

from ..HeaderPanel import HeaderPanel


class EvaluationForm(HtmlPanel):

    def __init__(self, **properties):
        #self.init_components(**properties)

        header_panel = HeaderPanel()
        self.add_component(header_panel)
        self.questions = [
            {
                'text': 'On a scale of 1 to 5, how confident are you in understanding the basics of personal finance (budgeting, saving, investing, etc.)?',
                'type': 'proficiency',
                'score_mapping': {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5}
            },
            {
                'text': 'How familiar are you with the term "compound interest," and could you explain its importance in investing or debt repayment?',
                'type': 'proficiency',
                'score_mapping': {'Completely unfamiliar': 0, 'I\'ve heard of it but can\'t explain': 1, 'I understand it somewhat': 2, 'I can explain it clearly': 3}
            },
            {
                'text': 'Do you actively contribute to any retirement accounts (e.g., 401(k), IRA)?',
                'type': 'proficiency',
                'score_mapping': {'Yes': 2, 'No': 0, 'I plan to in the near future': 1}
            },
            {
                'text': 'How often do you review and adjust your budget?',
                'type': 'proficiency',
                'score_mapping': {'Weekly': 4, 'Monthly': 3, 'Quarterly': 2, 'Annually': 1, 'I don\'t have a budget': 0}
            },
            {
                'text': 'Do you understand the terms and conditions associated with your credit cards, including interest rates and fees?',
                'type': 'proficiency',
                'score_mapping': {'Yes': 2, 'Somewhat': 1, 'No': 0}
            },
            {
                'text': 'Are you currently carrying any credit card debt?',
                'type': 'needs',
                'score_mapping': {'Yes, and I\'m struggling to make payments': -2, 'Yes, but I\'m managing it': -1, 'No': 0}
            },
            # ... Add all questions here following the same format
        ]

        for q in self.questions:
            lbl = Label(text=q['text'])
            self.add_component(lbl)

            radio = RadioButtonGroup(items=list(q['score_mapping'].keys()))
            self.add_component(radio)

            q['radio_group'] = radio

        self.submit_button = Button(text='Submit', role='primary')
        self.submit_button.click += self.calculate_score
        self.add_component(self.submit_button)

    def calculate_score(self, **event_args):
        score = 0

        for q in self.questions:
            selected_value = q['radio_group'].selected_value
            score += q['score_mapping'].get(selected_value)

        # Display the score
        alert(f"Your financial proficiency score is: {score}")