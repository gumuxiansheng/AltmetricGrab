# 南方科技大学商学院评价项目

本文档介绍 altmetric.com\plumx\dimensions数据的下载。

## 所需工具

代码基于python语言，主要工具为jupyter。

### Anaconda

Anaconda是一个python集成环境，预安装了很多常用的python包，包括jupyter。网址 https://www.anaconda.com/， 直接下载安装（直接下一步就可），打开后得到如下界面：

![anacondaMain](README/anacondaMain.png)

### jupyter

如上图所示，jupyter已经通过anaconda安装。jupyter是一个类笔记本式python运行环境，可以运行ipynb后缀文件，详细内容可参考其官网：https://jupyter.org/。

jupyter启动后可以通过浏览器访问地址 http://localhost:8888/tree/ 进入（初始端口为8888，若被占用，可能为8889或者其它）。jupyter的起始目录一般为C盘根目录，如果需要切换至其它盘，如E盘，可以修改jupyter程序属性：

![jupyterChange1](README/jupyterChange.png) 
![jupyterChange2](README/jupyterChange2.png)

其运行界面如下：

![jupyterMain](README/jupyterMain.png)

点开ipynb文档后，运行界面如下：

![jupyterOpen](README/jupyterOpen.png)

## 数据下载

目前下载主要为三方数据：altmetric.com、plumx、dimensions，下载的单元为article（文章）。现在代码里下载数据为2014-2018年大概5000多本期刊（ABS：1074， WOS：3890）的所有文章。主要步骤如下：

1. 通过dimensions平台下载所有期刊5年的所有文章基本信息，包括doi，标题，作者等信息。其中doi信息为后续下载其它数据的关键。

2. 通过文章的doi，获取此文章在 altmetric.com和plumx平台的平台id，此平台id为后续下载平台数据的键值。

3. 通过altmetric id下载altmetric.com的详细页面数据，包括'news outlets', 'blogs', 'policy', 'tweeters', 'weibo', 'facebook pages', 'wikipedia', 'redditors', 'f1000', 'video uploader', 'dimensions_citation', 'mendeley', 'citeulike'。

4. 通过plumx id下载plumx平台的详细数据，包括'abstruct_views', 'full_text_views', 'link_click_count', 'link_outs', 'exports_saves', 'reader_count_mendeley', 'reader_count_citeulike', 'cited_by_count_scopus', 'cited_by_count_crossref', 'cited_by_count_pubmed', 'tweets', 'facebook', 'news', 'blogs', 'reference_count_wikipedia', 'comment_count_reddit', 'mention_qa_site_mentions'。
