Welcome to the neural_snake_project!

# Змейка
Предполагаемый функционал программы:
1. Player only - Различные игровые моды только для игрока
* Standart - Базовая игра
* Infinity - Игра на бесконечном поле 
* Walls - Мод игры со стенами
* Back
2. AI mod - Часть игры про нейронную сеть
* AI_only - Наблюдение за игрой обученного ИИ
* AI VS Player - Соревновательная игра
* Learning - Наблюдение за обучением ИИ
* Back
3. PvP - Многопользовательская игра. Будет реализована не в этой 
* Play - Активна только при полной комплектации сервера.
При выходе из игры через ecs привязка к серверу остается, однако игра продолжается.
При начале игры сервер не ждет всех игроков, а начинает игру.
* Run server - создание сервера на N игроков, где N задается ползунком снизу
Для начала игры сервер будет ждать именно N игроков.
* Stop server - Остановить сервер
* Find server - поиск игрового сервера.
4. Settings - Настройки. Пока что пустая кнопка.
5. Exit - Завершение игровой сессии 

Игра включает в себя различные игровые моды.
Для одиночной игры доступны модификации:
1. Игра в коробке: Standart - границы поля являются опасностями для змеи
2. Infinity - Игра на бесконечном поле: при пересечении границы змея появляетс я на другом конце поля.
3. Walls - Для данной модификаций существуют различные карты разных уровней сложностей -
различная  расстановка стен. Везде в этом моде стены непроходимы, а границы как в infinity

В моде про нейронную сеть существуют различные возможности:
1. AI_only - запускает наблюдение за игрой обученного ИИ. 
Уровень обученности этого ИИ регулируется ползунком внизу экрана
2. AI VS Player - Соревновательная игра и ИИ. Запускается два поля -
Левым управляет бот, правым человек.
3. Learning - Наблюдение за обучением ИИ. В данном виде Игры ИИ следуют одна за другой без остановки
На графике представляются результаты обучения. Сначала змея не умная, но учится. 

Мод PvP в этой версии пока не реализован