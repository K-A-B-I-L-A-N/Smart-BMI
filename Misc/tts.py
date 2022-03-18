import gtts as gt 
import os      

TamilText="தயவு செய்து நேராக நின்று ஒரு நாணயத்தைச் செருகவும்"
tts = gt.gTTS(text=TamilText, lang='ta')
tts.save("insertcoin_tamil.mp3")
os.system("insertcoin_tamil.mp3")