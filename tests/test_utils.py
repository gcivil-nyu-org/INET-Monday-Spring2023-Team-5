from django.test import TestCase
from neighborhood.utils import get_title, get_slug


class UtilsTest(TestCase):
    def test_get_title(self):
        # Test basic functionality
        self.assertEqual(get_title("hello-world"), "Hello World")
        self.assertEqual(get_title("this-is-a-test"), "This Is A Test")

        # Test that it doesn't modify an already title-cased string
        self.assertEqual(get_title("Hello World"), "Hello World")
        self.assertEqual(get_title("This Is A Test"), "This Is A Test")

    def test_get_slug(self):
        # Test basic functionality
        self.assertEqual(get_slug("Hello World"), "hello-world")
        self.assertEqual(get_slug("This Is A Test"), "this-is-a-test")

        # Test that it doesn't modify an already slug-formatted string
        self.assertEqual(get_slug("hello-world"), "hello-world")
        self.assertEqual(get_slug("this-is-a-test"), "this-is-a-test")
