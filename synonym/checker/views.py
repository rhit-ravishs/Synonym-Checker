from django.shortcuts import render

from checker.forms import UploadFileForm
from . import SynonymChecker
import json
import string
translator = str.maketrans('','',string.punctuation)

# Create your views here.
def home(request):
    return render(request,'home.html',{})

def synonyms(request):
    if request.method=='POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid:
            fileData = request.FILES['inputfile'].read().decode("utf-8")
            normed_text = SynonymChecker.normalize_and_tokenize(fileData)
            filtered_words = SynonymChecker.filter_words(normed_text)
            synonyms = SynonymChecker.find_synonyms(filtered_words)
            split_data = fileData.split()
            FileWords = {}
            for i in range(len(split_data)):
                FileWords[split_data[i]] = split_data[i].translate(translator).lower()
            #synonyms['FileData'] = split_data
            return render(request,'home.html',{'FileData': split_data, 'FileWords': FileWords,'Words': synonyms.keys(),'Synonyms': synonyms})
    else:
        synonyms = {"fileData":"No data"}
        return render(request,'home.html',synonyms)