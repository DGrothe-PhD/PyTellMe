#
from videoText import rbbWeather

# Tonight and tomorrow
print("Wetter: ")

textHeute = rbbWeather(162, False)
print(textHeute.content)
print("")
print("Aussichten: ")
textAussichten = rbbWeather(163, True)
print(textAussichten.content)
