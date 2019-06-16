from wordcloud import WordCloud, STOPWORDS
import jieba
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
fig,ax=plt.subplots()

with open(r'testarea\a.txt','rb') as f:
    text=f.read()

wsplit=jieba.cut(text)
words="".join(wsplit)

shape=np.array(Image.open(r'testarea\a.jpg'))

mycloudword=WordCloud(scale=1, 
                      margin=2,
                      background_color='black',
                      mask=shape,
                      max_words=1000, 
                      min_font_size=1, 
                      max_font_size=60,
                      stopwords=STOPWORDS, 
                      random_state=50).generate(words)

ax.imshow(mycloudword)
ax.axis("off")
plt.show()

mycloudword.to_file(r"testarea\res.jpg")