#
from videoText import RbbWeather

# Tonight and tomorrow
print("Wetter: ")

textHeute = RbbWeather(162, False)
print(textHeute.content)
print("")
print("Aussichten: ")
textAussichten = RbbWeather(163, True)
print(textAussichten.content)
