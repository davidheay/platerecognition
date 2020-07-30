from os import environ
from openalpr import Alpr
alpr_dir ='C:/Users/DavidHerrera/AppData/Local/Programs/Python/Python37/openalpr'
environ['PATH'] = alpr_dir + ';' + environ['PATH']
alpr = Alpr('us', alpr_dir + '/openalpr.conf', alpr_dir + '/runtime_data')


if not alpr.is_loaded():
    print("Error loading OpenALPR")
    sys.exit(1)
results = alpr.recognize_file("car.jpg")

print(results["results"][0]["plate"])
alpr.unload()