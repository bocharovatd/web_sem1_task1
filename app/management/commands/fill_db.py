from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from app.models import *
import random


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        parser.add_argument("ratio", type=int, help="enter ratio which influences the size of created db")

    def handle(self, *args, **options):
        users = []
        questions = []
        answers = []
        tags = []
        questions_likes = []
        answers_likes = []

        self.stdout.write('Creating users...')
        # create ratio users
        for i in range(options["ratio"]):
            user = User.objects.create_user(f'Created user {i}', f'mail{i}@mail.com', f'{i}qwety')
            profile = Profile(user=user)
            users.append(profile)
        Profile.objects.bulk_create(users)

        self.stdout.write('Creating questions...')
        # create ratio * 10 questions
        for i in range(options["ratio"] * 10):
            questions.append(Question(title=f'Question {i}',
                                      text=f'I would like to ask Question {i}',
                                      user=random.choice(users)))
        Question.objects.bulk_create(questions)

        self.stdout.write('Creating answers...')
        # create ratio * 100 answers
        for i in range(options["ratio"] * 100):
            answers.append(Answer(text=f'Answer {i}',
                                  user=random.choice(users),
                                  question=random.choice(questions)))
        Answer.objects.bulk_create(answers)

        self.stdout.write('Creating tags...')
        # create ratio tags
        for i in range(options["ratio"]):
            tags.append(Tag(name=f'Tag {i}'))
        Tag.objects.bulk_create(tags)
        for question in questions:
            for _ in range(random.randint(0, 3)):
                question.tag_set.add(random.choice(tags))

        self.stdout.write('Creating likes...')
        # create ratio * 200 ratings
        questions_likes_questions = []
        questions_likes_users = []
        answers_likes_answers = []
        answers_likes_users = []
        for _ in range(options["ratio"] * 200):
            question = random.choice(questions)
            user = random.choice(users)
            type = 1
            if question not in questions_likes_questions and user not in questions_likes_users:
                questions_likes_questions.append(question)
                questions_likes_users.append(user)
                questions_likes.append(QuestionScore(question=question, user=user, type=type))
            answer = random.choice(answers)
            user = random.choice(users)
            type = 1
            if answer not in answers_likes_answers and user not in answers_likes_users:
                answers_likes_answers.append(answer)
                answers_likes_users.append(user)
                answers_likes.append(AnswerScore(answer=answer, user=user, type=type))
        QuestionScore.objects.bulk_create(questions_likes)
        AnswerScore.objects.bulk_create(answers_likes)

        self.stdout.write(
            self.style.SUCCESS('db successfully created')
        )
