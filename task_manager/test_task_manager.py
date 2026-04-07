import unittest
from task_model import Task
from user_model import User


class TestTaskManager(unittest.TestCase):

    # Use Case 1: Task Creation
    def test_task_initialisation(self):
        new_task = Task(
            "Mike",
            "Test Title",
            "Test Desc",
            "01 Jan 2026",
            "05 Jan 2026",
            "No",
        )
        self.assertEqual(new_task.username, "Mike")
        self.assertEqual(new_task.completed, "No")

    # Use Case 2: User Validation
    def test_user_credentials(self):
        test_user = User("admin", "password123")
        # Testing valid match
        self.assertEqual(test_user.username, "admin")
        self.assertEqual(test_user.password, "password123")
        # Testing invalid match
        self.assertFalse(test_user.username == "admin")
        self.assertFalse(test_user.password == "wrong_pass")

    # Use Case 3: Marking a task complete
    def test_mark_complete(self):
        task = Task("admin", "T", "D", "Date", "Date", "No")
        task.completed = "Yes"
        self.assertEqual(task.completed, "Yes")

    # Use Case 4: String Representation (Encapsulation)
    def test_task_string_format(self):
        task = Task("admin", "Clean", "Desc", "Date", "Date", "No")
        # Checks if the __str__ method actually contains the title
        self.assertIn("Clean", str(task))


if __name__ == '__main__':
    unittest.main()
