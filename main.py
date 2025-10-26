from flask import Flask, render_template, request

app = Flask(__name__)

def result_calculate(size, lights, device, transport_type, food_type):
    # Общий углеродный след в кг CO₂ в месяц.
    
    # I. Энергия (Дом)
    # Средний коэффициент выбросов CO2 на 1 кВт⋅ч (для России/СНГ примерно 0.4 кг)
    CO2_COEF_PER_KWH = 0.4  
    
    home_kwh = 100 * size
    light_kwh = 0.04 * lights
    devices_kwh = 5 * device
    
    # Расчет CO2 от энергии
    co2_energy = (home_kwh + light_kwh + devices_kwh) * CO2_COEF_PER_KWH 
    
    # II. Транспорт
    # Условные выбросы в кг CO2 в месяц, исходя из выбора (1 - минимум, 3 - максимум)
    transport_co2 = 0 
    if transport_type == 1:
        transport_co2 = 50 
    elif transport_type == 2:
        transport_co2 = 250
    elif transport_type == 3:
        transport_co2 = 700
            
    # III. Питание
    # Условные выбросы в кг CO2 в месяц, исходя из рациона
    food_co2 = 0
    if food_type == 1:
        food_co2 = 50
    elif food_type == 2:
        food_co2 = 200
    elif food_type == 3:
        food_co2 = 550
        
    # Общий след
    total_co2 = co2_energy + transport_co2 + food_co2
    
    return (round(total_co2, 2), 
            round(co2_energy, 2), 
            round(transport_co2, 2), 
            round(food_co2, 2))


# Первая страница
@app.route('/')
def index():
    return render_template('index.html')

# Вторая страница
@app.route('/<size>')
def lights(size):
    return render_template(
                            'lights.html', 
                            size=size
                           )

# Третья страница
@app.route('/<size>/<lights>')
def electronics(size, lights):
    return render_template(
                            'electronics.html',                           
                            size = size, 
                            lights = lights                           
                           )

# Выбор транспорта
@app.route('/<size>/<lights>/<device>')
def transport(size, lights, device):
    return render_template('transport.html', size=size, lights=lights, device=device)

# Выбор питания
@app.route('/<size>/<lights>/<device>/<transport>')
def food(size, lights, device, transport):
    return render_template('food.html', size=size, lights=lights, device=device, transport=transport)


@app.route('/<size>/<lights>/<device>/<transport>/<food>')
def end(size, lights, device, transport, food):
    total_co2, co2_energy, transport_co2, food_co2 = result_calculate(
                                                            int(size),
                                                            int(lights), 
                                                            int(device),
                                                            int(transport), 
                                                            int(food)
                                                            )
    return render_template('end.html', 
                            result=total_co2,
                            energy=co2_energy,
                            transport=transport_co2,
                            food=food_co2,
                            form_url = '/form'
                            )


@app.route('/form')
def form():
    return render_template('form.html')

# Результаты формы
@app.route('/submit', methods=['POST'])
def submit_form():
    name = request.form['name']
    email = request.form['email']
    address = request.form['address']
    date = request.form['date']

    with open('form.txt', 'a', encoding='utf-8') as f:
            f.write(f'Имя: {name}\n')
            f.write(f'E-mail: {email}\n')
            f.write(f'Адрес: {address}\n')
            f.write(f'Date: {date}\n')
            f.write('----------------\n')
    
    return render_template('form_result.html', 
                           name=name,
                           email=email,
                           address=address,
                           date=date
                           )
    

if __name__ == '__main__':
    app.run(debug=True)