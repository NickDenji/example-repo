from django.test import TestCase
from django.urls import reverse
from .models import Note


class NoteModelTest(TestCase):

    def test_note_creation(self):
        note = Note.objects.create(title="Test", content="Hello")
        self.assertEqual(note.title, "Test")

    def test_str_method(self):
        note = Note(title="My Note")
        self.assertEqual(str(note), "My Note")


class NoteViewsTest(TestCase):

    def test_note_list_view(self):
        response = self.client.get(reverse("note_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Notes")

    def test_note_create_view(self):
        response = self.client.post(reverse("note_create"), {
            'title': 'Test Note',
            'content': 'Some content'
        })
        self.assertEqual(response.status_code, 302)
