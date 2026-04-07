class Task:
    """
    A class to represent a single task in the system.
    """
    def __init__(
        self,
        username,
        title,
        description,
        assigned_date,
        due_date,
        completed="No",
    ):
        self.username = username
        self.title = title
        self.description = description
        self.assigned_date = assigned_date
        self.due_date = due_date
        self.completed = completed

    def __str__(self):
        """
        This defines how the task looks when you print it.
        Matches the format in your current view_all() function.
        """
        return (f"Assigned user:    {self.username}\n"
                f"Task:             {self.title}\n"
                f"Description:      {self.description}\n"
                f"Date Assigned:    {self.assigned_date}\n"
                f"Due Date:         {self.due_date}\n"
                f"Task Completed?:  {self.completed}\n")

    def to_file_line(self):
        """
    Converts the object back into a comma-separated string
    to save it into tasks.txt.
    """
        return (
            f"{self.username}, {self.title}, {self.description}, "
            f"{self.assigned_date}, {self.due_date}, {self.completed}\n"
        )
