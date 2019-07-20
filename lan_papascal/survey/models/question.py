from django.db import models

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)

    pub_date = models.DateTimeField('date published')
    deadline_date = models.DateTimeField('date expired')

    is_single_vote = models.BooleanField(("Accept only one option"),default=True)
    is_result_hidden = models.BooleanField(("Hide results from participants"), default=False)
    is_deadline_set = models.BooleanField(("Set a deadline"), default=False)

    def __str__(self):
        return self.question_text