# xiaohongshu_spider
爬取小红书相关评论
注:本代码仅为兴趣爱好探究，请勿进行商业利用或非法研究，负责后果自负，与创作者无关

## 一.总体概述

爬取的数据包括

```
评论者昵称，id，评论级别，评论内容
```

先上个图

![image-20240209122147148](https://gitee.com/yuejinjianke/tuchuang/raw/master/image/image-20240209122147148.png)





## 二.爬虫过程

![image-20240208112541353](https://gitee.com/yuejinjianke/tuchuang/raw/master/image/image-20240208112541353.png)

打开小红书页面，f12大法查看xhr请求，找到对应内容

![image-20240209122031074](https://gitee.com/yuejinjianke/tuchuang/raw/master/image/image-20240209122031074.png)

内容都在comments后面，翻页通过cursor翻页，逻辑如下

```python
 next_cursor = json_text['data']['cursor']

 if page == 1:
    url = 'https://edith.xiaohongshu.com/api/sns/web/v2/comment/page?note_id={}&cursor=&top_comment_id=&image_formats=jpg,webp,avif'.format(note_id)
 else:
    print(colorama.Fore.GREEN + "[info] 进入下一轮循环")
    url = 'https://edith.xiaohongshu.com/api/sns/web/v2/comment/page?note_id={}&cursor={}&top_comment_id=&image_formats=jpg,webp,avif'.format(note_id,next_cursor)
```

如何确定爬取完成？

![image-20240209122855262](https://gitee.com/yuejinjianke/tuchuang/raw/master/image/image-20240209122855262.png)

这个参数为true就证明可以继续爬取



数据处理过程在这里

![image-20240209123048799](https://gitee.com/yuejinjianke/tuchuang/raw/master/image/image-20240209123048799.png)



如何节约时间并发爬取呢

![image-20240209124738104](https://gitee.com/yuejinjianke/tuchuang/raw/master/image/image-20240209124738104.png)





整体效果如下

![image-20240209131356340](https://gitee.com/yuejinjianke/tuchuang/raw/master/image/image-20240209131356340.png)

![image-20240209131817005](https://gitee.com/yuejinjianke/tuchuang/raw/master/image/image-20240209131817005.png)



完整代码连接放在github上了，有需自取



## 三.readme

config文件里面填入自己的cookie

小红书具有反爬机制，因此需要自己寻找对应的note_id进行爬取

![image-20240209174346194](https://gitee.com/yuejinjianke/tuchuang/raw/master/image/image-20240209174346194.png)

进行keyword搜索后f12大法进行获取note_id，建议默认点击最热，这样爬取的评论数才可以足够满足数据爬取的需要

获取成功后在主函数这里进行初始化
![image-20240209174603533](https://gitee.com/yuejinjianke/tuchuang/raw/master/image/image-20240209174603533.png)



