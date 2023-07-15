# 이름만 영어로 추출하는 코드

from hangul_romanize import Transliter
from hangul_romanize.rule import academic

text = "누구에게 혜선한테 613호로 물건을 갖다줘"
location = ['으로', '로', '이에게', '에게', '을', '를', '이한테', '한테', '에', '이']

text = text.split()

v_name = []
v_place = []

for word in text :
    for loc in location :
        if loc in word :
            # location의 단어를 제거한 후 이름 저장
            if loc in ['이에게', '에게', '이한테', '한테', '이']:
                v_name = word.replace('loc', '')#.replace('에게', '').replace('이한테', '').replace('한테', '').replace('이', '')
            # location의 단어를 제거한 후 장소 저장
            elif loc in ['으로', '로', '에']:
                v_place = word.replace('으로', '').replace('로', '').replace('에', '')
            break

print(v_name)
print(v_place)

# 로마자 변환을 위한 Transliter 클래스 객체 생성
trans = Transliter(rule=academic)
# 한글 이름을 로마자로 변환
romanized_name = trans.translit(v_name)
print(romanized_name)

                
r_name = []
r_place = []
            
r_name = romanized_name
r_place = v_place
                
print('이름은', r_name)
print('장소는', r_place)