import json
import random
import time
from os import listdir
from os.path import isfile, join

langDir = "lang"
languages = list(map(lambda x: x.replace(".json", ""),
                     [f for f in listdir(langDir) if isfile(join(langDir, f)) and ".json" in f]))


def get_lang(lang):
    if lang in languages:
        with open("%s/%s.json" % (langDir, lang), mode="r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    else:
        raise FileNotFoundError("The language %s doesn't exist!" % lang)


def get_questions(lang="de-DE"):
    return get_lang(lang)["questions"]


def get_answers(lang="de-DE"):
    return get_lang(lang)["answers"]


def get_topics(lang: str):
    for key in get_questions(lang):
        yield key


def is_topic(topic: str, lang="de-DE"):
    return topic in get_topics(lang)


def random_topic_answer(topic: str, lang="de-DE"):
    answers = get_answers(lang)[topic]
    return answers[random.randint(0, len(answers) - 1)]


def get_answer_from_question(question: str, lang="de-DE", debug=False):
    questions = get_questions(lang)
    answers = get_answers(lang)
    for topic in get_topics(lang):
        for q in questions[topic]:
            if q in question.lower():
                answer = answers[topic][random.randint(0, len(answers[topic]) - 1)]
                if debug:
                    print("----------------")
                    print("Topic: %s, Question: %s" % (topic, q))
                    print(answer)
                return answer


def debugging(iterations=2):
    before = time.time()
    test_phrases = [
        "hi",
        "hallo",
        "bist du schlau?",
        "bist du dumm?",
        "nein",
        "was hältst du von dem smalltalk bot?",
        "was ist deine lieblingsfarbe?",
        "wie heißt du?",
        "was machst du gerade?",
        "tschau",
        "bb",
        "dumm",
        "wie wird das wetter heute?",
        "du bist ein idiot!",
        "scheiße",
        "lol",
        "erzähl mir einen witz!!",
        "yay",
        "echt?",
        "mir ist langweilig :(",
        "NEIN!",
        "WARUM!?",
        "wie alt bist du?",
    ]
    for i in range(iterations):
        for phrase in test_phrases:
            get_answer_from_question(phrase, "de-DE", True)
    print("----------------\n")
    print("Time: %fs" % ((time.time() - before)/iterations/len(test_phrases)))
