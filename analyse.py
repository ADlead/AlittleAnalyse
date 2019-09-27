import jieba
import wordcloud
import re
import pandas as pd
import numpy as np
from PIL import Image

from pyecharts import Map, Bar



# 根据文本生成词云图
def generatewordcloud(filename):
    # 文字字体
    font = 'msyh.ttc'

    # 读取背景图片
    img = Image.open('data/image.jpg')
    img_array = np.array(img)

    # 读取文本
    f = open(filename, 'r', encoding='utf-8')
    content = f.read().replace(' ','').strip()
    # print(content)
    words = jieba.lcut(content)
    words = ' '.join(words)

    wc = wordcloud.WordCloud(
        background_color='white',
        mask=img_array,
        font_path=font
    )

    wc.generate_from_text(words)
    wc.to_file('dazhong-五山.png')




class AlittleAnalyse:
    def __init__(self):
        self.df = pd.read_csv('alittle.csv', encoding='gbk')
        self.df = self.df.dropna(axis=0, how='all')
        # print(self.df)
        self.address = list(self.df.address)
        # print(self.address)
        self.districts_list = [each[:3] for each in self.address]
        districts_counts = pd.value_counts(self.districts_list)
        self.areas = districts_counts.index
        self.value = list(districts_counts)

    def generatemap(self):

        # 制作地图，关于一点点在广州各个区的分布，先建立列表，根据每个区
        map = Map('一点点在广州市的分布', width=1200, height=1000)
        map.add('一点点在广州市的分布', self.areas, self.value, maptype='广州', visual_range=[min(self.value), max(self.value)],
                is_map_symbol_show=False,
                is_label_show=True, is_visualmap=True, label_text_color='#509')
        # map.show_config()
        map.render('一点点在广州市的分布.html')

    def generatebar(self):
        # 每个区的一点点数量的柱形图
        bar = Bar('广州各个区一点点的对比',width=1000,height=800)
        bar.add('广州各个区一点点数量的对比',self.areas, self.value,
                is_label_show=True, 
                mark_line=['min','max'], mark_point=['average'],
                xaxis_interval=0, 
                xaxis_rotate=30,yaxis_rotate=30,

                )

        bar.render('广州各个区一点点数量的对比.html')

    def rank_bar(self):
        bar = Bar('评分前10的一点点', width=1000, height=900)
        pd_rank = self.df['rank']
        pd_title = self.df['title']
        # print(pd_rank)
        rank_series = pd.Series(data=list(pd_rank), index=pd_title)
        # print(rank_series.sort_values(ascending=False))
        rank_ten = rank_series[:10]

        bar.add('评分前10的一点点', rank_ten.index, rank_ten,
                is_label_show=True, 
                xaxis_interval=0,  
                xaxis_rotate=20, yaxis_rotate=20,  

                )

        bar.render('评分前10的一点点.html')
        pass

    def comments_rank(self):
        bar = Bar('评论数最高前10的一点点', width=1000, height=900)
        pd_comments_num = self.df['comments_num']
        pd_title = self.df['title']

        comments_num_series = pd.Series(data=list(pd_comments_num), index=pd_title)
        comments_num_series = comments_num_series.sort_values(ascending=False)

        rank_ten = comments_num_series[:10]
        bar.add('评论数最高前10的一点点', rank_ten.index, rank_ten,
                is_label_show=True,  
                xaxis_interval=0,  
                xaxis_rotate=20, yaxis_rotate=20,  
                

                )

        bar.render('评论数最高前10的一点点.html')

        pass


if __name__ == '__main__':
    # generatewordcloud('comment-五山.txt')
    alittle = AlittleAnalyse()
    alittle.generatemap()
    # alittle.generatebar()
    # alittle.rank_bar()
    # alittle.comments_rank()

    pass




