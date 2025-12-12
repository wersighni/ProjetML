from django import forms

class PatientForm(forms.Form):

    age = forms.IntegerField(label="🧑 Age")
    gender = forms.ChoiceField(label="👤 Genre",
                               choices=[('M', 'Homme'), ('F', 'Femme')])

    billing = forms.FloatField(label="💰 Montant facturé")

    medical_condition = forms.ChoiceField(label="🩺 Condition médicale",
        choices=[
            ('Cardiology','Cardiology'),
            ('Neurology','Neurology'),
            ('Cancer','Cancer'),
            ('Trauma','Trauma'),
            ('Others','Others'),
        ]
    )

    admission_type = forms.ChoiceField(label="🏥 Type d'admission",
        choices=[
            ('Emergency','Emergency'),
            ('Urgent','Urgent'),
            ('Routine','Routine'),
        ]
    )

    insurance = forms.ChoiceField(label="🛡️ Assurance",
        choices=[
            ('Private','Private'),
            ('Gov','Gov'),
            ('None','None'),
        ]
    )

    test_results = forms.ChoiceField(label="🧪 Résultat test",
        choices=[
            ('Positive','Positive'),
            ('Negative','Negative'),
        ]
    )

    admission_date = forms.DateField(label="📅 Date admission",
                   widget=forms.DateInput(attrs={'type':'date'}))

    discharge_date = forms.DateField(label="📅 Date sortie",
                   widget=forms.DateInput(attrs={'type':'date'}))
