## 这是一个使用Django开发的博客系统
### Python版本和依赖库
- python3.6
- Django 1.11.6
- Markdown 2.6.9
- Pygments 2.1.3
- pytz 2017.3
- django-haystack 2.6.1
- jieba 0.39
- Whoosh 2.7.4

### 安装依赖库
```shell
pip install -r requirements.txt
```

### 同步数据库
```shell
python manage.py migrate
```

### 启动项目
```shell
python manage.py runserver
```