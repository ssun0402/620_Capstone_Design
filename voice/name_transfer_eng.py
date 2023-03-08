# 분리된 텍스트 중 이름 부분을 영어로 변경

text = ['물건', '강명현', '명현', '혜선', '태언', '희웅', '613']
name = ['강명현', '명현', '태언', '혜선', '희웅']

for i, word in enumerate(text) :
    if word in name :
        if (word == '명현')  | (word == '강명현') :
            text[i] = 'myung hyun'
            
        elif word == '혜선' :
            text[i] = 'hye seon'
            
        elif word == '태언' :
            text[i] = 'tae eon'
            
        elif word == '희웅' :
            text[i] = 'hee ung'

print(text)
            
        