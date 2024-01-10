from django.shortcuts import render
import joblib
from .forms import *
# Create your views here.

    
    
def detect_text(request):
    context = {}
    
    if request.method == 'POST':
        form = DetectionForm(request.POST, request.FILES)
        
        if form.is_valid():
            text = form.cleaned_data['text']
            
            if 'file' in request.FILES:
                file = request.FILES['file']
                
                try:
                    text = file.read().decode('utf-8')
                except UnicodeDecodeError:
                    text = file.read().decode('iso-8859-1')
            else:
                text = request.POST.get('text', '')
            
            # Reste du traitement...
            
            vectorizer = joblib.load("vectorizer")
            text_processed = vectorizer.transform([text])
            model = joblib.load("Model_final")   # Instancie votre modèle de détection
            proba = model.predict_proba(text_processed)  # Remodeler le tableau en ajoutant des crochets autour de `text`
            probabilities = {
            	'Chat-GPT': round(100*proba[0][1], 2),
                'Humain': round(100*proba[0][0], 2)
            } 
            context = {'probabilities': probabilities, 'text': text}
    else:
        form = DetectionForm()
    
    context['form'] = form
    return render(request, 'result.html', context)
