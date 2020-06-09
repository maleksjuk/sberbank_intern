#!/usr/bin/env python
# coding: utf-8

print("""
    Тестовое задание для стажёра на backend
    
    Задание:
        Определить наиболее пригодный для жилья район в г. Москва на основе открытых данных https://data.mos.ru
     
    Задача min:
        1. Получить данные локально
        2. Научиться по адресу определять район в г.Москве
        3. Рассчитать метрику качества жизни в некотором районе
    
    Район = Административный округ (АО)
""")

import numpy as np
import pandas as pd

print("1. Получим данные из открытых источников")
# 
# __Источники:__
# 
# 1. Общественное питание в г.Москва
#     * https://data.mos.ru/opendata/7710881420-obshchestvennoe-pitanie-v-moskve
# 2. Поликлиники в г. Москва (взрослые)
#     * взрослые: https://data.mos.ru/opendata/7707089084-poliklinicheskaya-pomoshch-vzroslym
#     * дети: https://data.mos.ru/opendata/7707089084-poliklinicheskaya-pomoshch-detyam/
# 3. Образовательные учреждения
#     * https://data.mos.ru/opendata/7719028495-obrazovatelnye-uchrejdeniya-goroda-moskvy
# 4. Покрытие городским WIFI
#     * https://data.mos.ru/opendata/7710878000-gorodskoy-wi-fi
# 5. Данные о вызовах пожарно-спасательного гарнизона в г. Москва
#     * https://data.mos.ru/opendata/7710474791-dannye-vyzovov-pojarnoy-slujby-po-ao-goroda-moskvy

# In[2]:


# Данные о точках общественого питания
data_1_food = pd.read_json("data/data_1_food.json", encoding='windows-1251')
print("Общественное питание в г.Москва: OK")

# Данные о поликлиниках для взрослых
data_2_med_adults = pd.read_json("data/data_2_med_adults.json", encoding='windows-1251')
print("Поликлиники в г. Москва (взрослые): OK")

# Данные о детских поликлиниках
data_2_med_childrens = pd.read_json("data/data_2_med_childrens.json", encoding='windows-1251')
print("Поликлиники в г. Москва (дети): OK")

# Данные об образовательных учреждениях
data_3_schools = pd.read_json("data/data_3_school.json", encoding='windows-1251')
print("Образовательные учреждения: OK")

# Данные о точках бесплатного доступа к сети WiFi
# data_4_WiFi = pd.read_json("data/data_4_wifi.json", encoding='windows-1251')

# Данные о вызовах пожарно-спасательного гарнизона
data_5_fire = pd.read_json("data/data_5_fire.json", encoding='windows-1251')
print("Данные о вызовах пожарно-спасательного гарнизона в г. Москва: OK")




print("\n2. Подготовим данные для анализа")
# 
# *Переформулирую задачу, как понял её я:*
# 
# Необходимо подготовить данные для анализа. Данные обо всех учреждениях собрать по административным округам.
# 
# Данные будем собирать в переменную __district_data__. Объединять с новыми данными будем по полю __AdmArea__

# ### Данные о точках общественого питания

# Эти данные имеют столбец __AdmArea__ с указанием административных округов. Сгруппируем по ним все данные и посчитаем количество организаций общественного питания.

# In[13]:


district_data = data_1_food.groupby('AdmArea', as_index=False).agg({'Name': 'count'}).rename(columns={'Name': 'food'})


# In[14]:


district_data


# ### Данные о поликлиниках

# __Поликлиники для взрослого населения__. Информация об административных округов была найдена в столбце __ObjectAddress__ в поле __AdmArea__. Для каждой поликлиники создадим отдельный столбец с указанием АО, в котором поликлиники расположены.

# In[15]:


data_2_med_adults['AdmArea'] = np.array([data_2_med_adults.ObjectAddress[i][0]['AdmArea']
                                         for i in range(data_2_med_adults.shape[0])])
tmp = data_2_med_adults.groupby('AdmArea', as_index=False).agg({'FullName': 'count'}).rename(columns={'FullName': 'med_adults'})
district_data = district_data.join(tmp.set_index('AdmArea'), on='AdmArea')


# In[16]:


# district_data


# __Детские поликлиники__. Данные по расположению аналогичны данным по поликлиникам для взрослого населения. Действия будут те же.

# In[17]:


data_2_med_childrens['AdmArea'] = np.array([data_2_med_childrens.ObjectAddress[i][0]['AdmArea']
                                            for i in range(data_2_med_childrens.shape[0])])
tmp = data_2_med_childrens.groupby('AdmArea', as_index=False).agg({'FullName': 'count'}).rename(columns={'FullName': 'med_childrens'})

district_data = district_data.join(tmp.set_index('AdmArea'), on='AdmArea')


# In[18]:


# district_data


# __Объединим данные__ о поликлиниках в один столбец, поскольку в этом решении нет необходимости использовать данные раздельно.

# In[19]:


district_data['med'] = district_data.med_adults + district_data.med_childrens
district_data.drop(['med_adults', 'med_childrens'], axis=1, inplace=True)


# In[20]:


# district_data


# ### Данные об образовательных учреждениях

# Информация об административных округов была найдена в столбце __InstitutionsAddresses__ в поле __AdmArea__. Аналогично данным о поликлиниках создадим отдельный столбец __AdmArea__.

# In[21]:


data_3_schools['AdmArea'] = np.array([data_3_schools.InstitutionsAddresses[i][0]['AdmArea']
                                      for i in range(data_3_schools.shape[0])])
tmp = data_3_schools.groupby('AdmArea', as_index=False).agg({'FullName': 'count'}).rename(columns={'FullName': 'school'})

district_data = district_data.join(tmp.set_index('AdmArea'), on='AdmArea')


# In[22]:


# district_data


# ### Данные о вызовах пожарно-спасательного гарнизона

# Эти данные содержат информацию не только за 2019 год, поэтому исключим лишние записи.

# In[23]:


data_5_fire = data_5_fire[data_5_fire.Year == 2019]


# Поскольку здесь информация уже разбита по административным округам, нам остаётся только сгруппировать данные по АО и просуммировать количество вызовов.

# In[24]:


data_5_fire = data_5_fire.groupby('AdmArea', as_index=False).agg({'Calls': 'sum'}).rename(columns={'Calls': 'fire_calls'})


# In[25]:


# data_5_fire


# Заметим, что эти данные имеют ошибки в написании АО. Исправим их.

# In[26]:


data_5_fire.iloc[6, 1] = data_5_fire.iloc[5, 1] + data_5_fire.iloc[6, 1] + data_5_fire.iloc[7, 1]
data_5_fire.iloc[5, 1] = 0
data_5_fire.iloc[7, 1] = 0

data_5_fire.iloc[8, 1] = data_5_fire.iloc[8, 1] + data_5_fire.iloc[9, 1]
data_5_fire.iloc[9, 1] = 0

data_5_fire = data_5_fire[data_5_fire.fire_calls > 0].reset_index(drop=True)


# In[27]:


# data_5_fire


# Теперь все строки записаны правильно. Но возникла проблема с новообразованными административными округами столицы: в отличие от __district_data__, в __data_5_fire__ Троицкий (ТАО) и Новомосковский (НАО) административные округа записаны в одной строке. Поскольку недостаточно данных о вызовах пожарно-спасательного гарнизона по каждому из этих округов отдельно, объединим ТАО и НАО в __district_data__.

# In[28]:


district_data.loc[district_data.shape[0]] = np.array(["Троицкий и Новомосковский административные округа", 
                                                      district_data.iloc[3, 1] + district_data.iloc[7, 1],
                                                      district_data.iloc[3, 2] + district_data.iloc[7, 2],
                                                      district_data.iloc[3, 3] + district_data.iloc[7, 3]
                                                     ])


# In[29]:


district_data = district_data.join(data_5_fire.set_index('AdmArea'), on='AdmArea')


# In[30]:


# Удалим строки с неизвестными данными, а также изменим тип значений на целочисленный.
district_data = district_data.dropna().astype({'food': 'int',
                                               'med': 'int',
                                               'school': 'int',
                                               'fire_calls': 'int'
                                              }).reset_index(drop=True)


# In[31]:


print(district_data)


print("\n3. Рассчитаем метрику качества жизни в районах")
# 
# $$ Качество\ жизни = \frac{n_{поликлиники} + n_{ОУ} + n_{питание}}{относительная\ опасность\ района} $$
# 
# $$ относительная\ опасность\ района = \frac{количество\ вызовов\ в\ районе}{общее\ количество\ вызовов\ за\ год} $$
# 
# Здесь $n$ - агрегированное по району значение некоторого показателя, ОУ - образовательные учреждения.

# Пусть агрегированными значениями показателей будут отношения количества организаций к максимальному количеству организаций по каждому показателю.

# In[32]:


district_data.food = district_data.food / np.max(district_data.food)
district_data.med = district_data.med / np.max(district_data.med)
district_data.school = district_data.school / np.max(district_data.school)


# Теперь данные в __district_data__ готовы для расчёта качества жизни.

# In[33]:


# общее количество вызовов пожарно-спасательного гарнизона за год
sum_fire = np.sum(district_data.fire_calls)


# In[34]:


# Качество жизни
district_data['quality'] = (district_data.med + district_data.school + district_data.food) /     (district_data.fire_calls / sum_fire)


# In[35]:


# Посмотрим, как выглядит рейтинг административных округов с коэффициентами
print(district_data.sort_values('quality', ascending=False).reset_index(drop=True))


# #### Ответ на поставленную задачу:

# In[36]:


result = district_data.sort_values('quality', ascending=False).reset_index(drop=True).iloc[0, 0]

print("Наиболее благоприятный административный округ для проживания в городе Москва:", result)

