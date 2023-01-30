from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import model,AnswersGenerator

# Create your views here.
def index(request):
    return render(request, 'index.html')

def submitquery(request):
    q = request.GET['query']
    try:
        ans = eval(q)
        mydictionary = {
            "q" : q,
            "ans" : ans,
            "error": False
        }
        #return HttpResponse("Error no")
        return render(request, "index.html", context=mydictionary)

    except:
        pass
def model(request):
    """q = request.GET['query']
    try:
        ans = str(AnswersGenerator(q))
        print("llega1")
        
        print(ans)
        mydictionary = {
            "q" : q,
            "ans" : ans,
            "error": False
        }
        print("llega")
        #return HttpResponse("Error no")
        return render(request, "index.html", context=mydictionary)

    except:
        pass"""
    # Get input data from the user
    input_data = request.GET['query']
    # Use the model to process the data
    output = str(AnswersGenerator(input_data))
    #output = model.predict(input_data)
    # Create a context dictionary
    context = {'output': output}
    # Render the template and return the response
    return render(request, "index.html", context)
