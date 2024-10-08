from django.contrib.auth.models import User
from django.test import TestCase
from posts.models import Post


class BlogTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        testuser1 = User.objects.create_user(
            username='testuser1',
            password='abc123',


        )
        testuser1.save()

        test_post = Post.objects.create(
            title='testpost',
            content='content',
            autor=testuser1,
        )
        test_post.save()

    def test_create_content(self):
        post = Post.objects.get(id=1)
        autor = f'{post.autor}'
        title = f'{post.title}'
        content = f'{post.content}'
        self.assertEqual(autor, 'testuser1')
        self.assertEqual(title, 'testpost')
        self.assertEqual(content, 'content')

