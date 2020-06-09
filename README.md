# Тестовое задание для стажёра на backend

__Задание:__ Определить наиболее пригодный для жилья район в г. Москва на основе открытых данных https://data.mos.ru

__Задача min:__

1. Получить данные локально
2. Научиться по адресу определять район в г.Москве
3. Рассчитать метрику качества жизни в некотором районе

Район = Административный округ (АО)

---

### Как запустить

1. Основная задача

Открыть файл Districts_of_Moscow.ipynb в jupyter-notebook или ввести в терминале:

    python3 Districts_of_Moscow.py 

Для успешного запуска и выполнения проекта нужно, чтобы были установлены библиотеки __pandas__ и __numpy__:

    pip3 install numpy
    pip3 install pandas
    
Чтобы просмотреть отчёт (без скачивания), нужно открыть файл Districts_of_Moscow.ipynb или Distinct_of_Moscow.html 


2. Задача определения района по адресу

Ввести в терминале:

    python3 get_district_moscow.py

Для успешного запуска и выполнения проекта нужно, чтобы были установлены библиотеки __json__, __geojson__, __shapely__ и __requests__:

    pip3 install json
	pip3 install geojson
	pip3 install Shapely
	pip3 install requests


