# 음성 인식 후 텍스트 인식률 높인 코드 (강제로)
jetson1 = "잭슨, 넥슨, 넥센"
text = "620 4로 가줘, 태연한테 명 현한테 물건을 어디로 갖다줘"

jetson = ["잭슨", "넥슨", "넥센"]
place = ['620 4']
tae_eon = ['태연', '태현']
myung_hyun = ['명 현', '영현', '영 현']

#for p in place :
#    if p in text :
#        text = text.replace(p, '620')
        
#for t in tae_eon :
#    if t in text :
#        text = text.replace(t, '태언')
        
#print(text)

for i in jetson :
    if i in jetson1 :
        jetson1 = jetson1.replace(i, '젯슨')
        
print(jetson1)

#for word in place + tae_eon + myung_hyun :
#    if word in text :
#        if word in place :
#            text = text.replace(word, '620호')
            
#        elif word in tae_eon :
#            text = text.replace(word, '태언')
            
#        elif word in myung_hyun :
#            text = text.replace(word, '명현')

#print(text)

def recognition_rate(text, place, tae_eon, myung_hyun):
    for word in place + tae_eon + myung_hyun:
        if word in text:
            if word in place:
                text = text.replace(word, '620')
            elif word in tae_eon:
                text = text.replace(word, '태언')
            elif word in myung_hyun :
                text = text.replace(word, '명현')
    return text

text = recognition_rate(text, place, tae_eon, myung_hyun)
print(text)
