KnowledgeBaseGenerator.py и LearningSetGenerator.py используются для генерации модельной Базы Знаний и генерации модельной выборки (Датасета) соответственно. Для настройки параметров генерации существует файл Config.py.

Программа для генерации Модельной базы знаний KnowledgeBaseGenerator.py имеет флаг -o для обозначения выходного файла.
Пример: 
python KnowledgeBaseGenerator.py -o ./data/model_knowledgebase.json

Программа для генерации Модельной обучающей выборки (Датасета) LearningSetGenerator.py имеет имеет флаги -o для обозначения выходного файла и -i для обозначения входного файла.
Пример: 
python LearningSetGenerator.py -i ./data/model_knowledgebase.json                         -o ./data/learning_set.json
Имена файлов могут быть произвольными. Далее в качестве примера будут использоваться те же имена, что и выше.
Цепочка работы программ следующая:
[ KnowledgeBaseGenerator.py ] -> model_knowledgebase.json -> [ LearningSetGenerator.py   ] -> learning_set.json

