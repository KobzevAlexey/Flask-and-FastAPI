from flask import Flask
from flask import render_template


app = Flask(__name__)


@app.route('/')
def main():  # put application's code here
    context = {'title': 'Главная',
               "content": "Добро пожаловать в магазин, выберите необходимый раздел"}
    return render_template('main.html', **context)

@app.route('/jackets/')
def jackets():
    _goods = [{'type': 'Кожаная',
                 'text': 'Отличная стильная куртка',
                 'price': '$10'},
                {'type': 'Джинсовая',
                 'text': 'Долговечная крепкая куртка',
                 'price': '$5'},
                {'type': 'Пуховая',
                 'text': 'Защитит вас от любых морозов',
                 'price': '$15'}
                ]
    context = {'title': 'Куртки','about':'Посмотрите на эти прекрасные куртки', 'things': _things}
    return render_template('goods.html', **context)

@app.route('/shoes/')
def shoes():
    _goods = [{'type': 'Кеды три полоски',
                 'text': 'Вернут вам ваш 2007',
                 'price': '$10'},
                {'type': 'Беговые кроссовки',
                 'text': 'Говорят сам Форест Гамп бегал в таких',
                 'price': '$20'},
                {'type': 'Резиновые сапоги',
                 'text': 'И в дождь и в грязь и в лес за грибами',
                 'price': '$25'},
               {'type': 'Валенки',
                 'text': 'Теплые как наши зимние куртки',
                 'price': '$25'}
                ]
    context = {'title': 'Обувь', 'about':'Эта обувь долна быть на ваших ногах', 'things': _things}
    return render_template('goods.html', **context)

@app.route('/jeans/')
def jeans():
    _goods = [{'type': 'Классические джинсы',
                 'text': 'Отличные джинсы, подойдут и к пиджаку и к свитеру и к косухе',
                 'price': '$15'},
                {'type': 'Порезанные джинсы',
                 'text': 'Лучше всего подойдут к кедам "Три полоски"',
                 'price': '$20'},
                {'type': 'Зауженные джинсы',
                 'text': 'Пятки придется намылить, зато стильно',
                 'price': '$25'},
               {'type': 'Ушанка',
                 'text': 'Мы не знаем, как она сюда попала',
                 'price': '$30'}
                ]
    context = {'title': 'Джинсы', 'about':'Джинсы никогда не выходят из моды', 'things': _things}
    return render_template('goods.html', **context)

@app.route('/about/')
def about():
    context = {'title': "Информация"}
    return render_template('about.html', **context)

if __name__ == '__main__':
    app.run(debug= True)