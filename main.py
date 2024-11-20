import random
from collections import Counter

# Список документов
documents = [
    ["Hadoop", "Big Data", "HBase", "Java", "Spark", "Storm", "Cassandra"],
    ["NoSQL", "MongoDB", "Cassandra", "HBase", "Postgres"],
    ["Python", "scikit-learn", "scipy", "numpy", "statsmodels", "pandas"],
    ["R", "Python", "statistics", "regression", "probability"],
    ["machine learning", "regression", "decision trees", "libsvm"],
    ["Python", "R", "Java", "C++", "Haskell", "programming languages"],
    ["statistics", "probability", "mathematics", "theory"],
    ["machine learning", "scikit-learn", "Mahout", "neural networks"],
    ["neural networks", "deep learning", "Big Data", "artificial intelligence"],
    ["Hadoop", "Java", "MapReduce", "Big Data"],
    ["statistics", "R", "statsmodels"],
    ["C++", "deep learning", "artificial intelligence", "probability"],
    ["pandas", "R", "Python"],
    ["databases", "HBase", "Postgres", "MySQL", "MongoDB"],
    ["libsvm", "regression", "support vector machines"]
]

# Параметры модели
K = 4  # Количество тем
random.seed(0)

# Инициализация структур данных
D = len(documents)
document_topic_counts = [Counter() for _ in documents]
topic_word_counts = [Counter() for _ in range(K)]
topic_counts = [0 for _ in range(K)]
document_lengths = list(map(len, documents))
distinct_words = set(word for document in documents for word in document)
W = len(distinct_words)

# Инициализация тем для слов
document_topics = [[random.randrange(K) for _ in document] for document in documents]

# Заполнение начальных счетчиков
for d in range(D):
    for word, topic in zip(documents[d], document_topics[d]):
        document_topic_counts[d][topic] += 1
        topic_word_counts[topic][word] += 1
        topic_counts[topic] += 1


# Функция для случайной выборки индекса по весам
def sample_from(weights):
    total = sum(weights)
    rnd = total * random.random()
    for i, w in enumerate(weights):
        rnd -= w
        if rnd <= 0:
            return i


# Условные вероятности
def p_topic_given_document(topic, d, alpha=0.1):
    return (document_topic_counts[d][topic] + alpha) / (document_lengths[d] + K * alpha)


def p_word_given_topic(word, topic, beta=0.1):
    return (topic_word_counts[topic][word] + beta) / (topic_counts[topic] + W * beta)


def topic_weight(d, word, k):
    return p_word_given_topic(word, k) * p_topic_given_document(k, d)


def choose_new_topic(d, word):
    weights = [topic_weight(d, word, k) for k in range(K)]
    return sample_from(weights)


# Итерации по выборке
for iteration in range(1000):
    for d in range(D):
        for i, (word, topic) in enumerate(zip(documents[d], document_topics[d])):
            # Удаляем текущее слово/тематику из счетчиков
            document_topic_counts[d][topic] -= 1
            topic_word_counts[topic][word] -= 1
            topic_counts[topic] -= 1
            document_lengths[d] -= 1

            # Выбираем новую тематику
            new_topic = choose_new_topic(d, word)
            document_topics[d][i] = new_topic

            # Увеличиваем счетчики с новой тематикой
            document_topic_counts[d][new_topic] += 1
            topic_word_counts[new_topic][word] += 1
            topic_counts[new_topic] += 1
            document_lengths[d] += 1

# Вывод тем и их наиболее значимых слов
topic_names = ["Big Data and programming languages", "Python and statistics", "databases", "machine learning"]

for k, word_counts in enumerate(topic_word_counts):
    print(f"Topic {k}:")
    for word, count in word_counts.most_common(5):
        if count > 0:
            print(f"  {word}: {count}")

# Вывод тем для каждого документа
for document, topic_counts in zip(documents, document_topic_counts):
    print("\nDocument:", document)
    for topic, count in topic_counts.most_common():
        if count > 0:
            print(f"  {topic_names[topic]}: {count}")
