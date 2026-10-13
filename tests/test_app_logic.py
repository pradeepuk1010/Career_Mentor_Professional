import os
import tempfile
import unittest

_tmp = tempfile.TemporaryDirectory()
os.environ["CAREER_MENTOR_DB"] = os.path.join(_tmp.name, "test.db")

import database
from mentor_engine import recommend, ROLE_DATA

class CareerMentorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        database.init_db()

    def test_profile_roundtrip(self):
        p = database.get_profile()
        p["name"] = "Test User"
        p["target_role"] = "Python Developer"
        database.save_profile(p)
        loaded = database.get_profile()
        self.assertEqual(loaded["name"], "Test User")
        self.assertEqual(loaded["target_role"], "Python Developer")

    def test_goal_lifecycle(self):
        goal_id = database.add_goal("Finish SQL", "Technical skill", "2099-01-01", "Complete practice")
        self.assertEqual(len(database.get_goals()), 1)
        database.toggle_goal(goal_id, True)
        self.assertEqual(database.get_goals()[0]["completed"], 1)
        database.delete_goal(goal_id)
        self.assertEqual(database.get_goals(), [])

    def test_reflection_roundtrip(self):
        database.add_reflection("Built a project", "Time", "Practise interview")
        rows = database.get_reflections()
        self.assertEqual(rows[0]["wins"], "Built a project")
        self.assertEqual(rows[0]["next_step"], "Practise interview")

    def test_recommendations_personalized_to_role(self):
        result = recommend({"target_role":"Python Developer", "skills":["Python"], "interests":"APIs", "weekly_hours":6})
        self.assertTrue(result["actions"])
        self.assertEqual(len(result["projects"]), 3)
        self.assertIn("SQL", result["gaps"])

if __name__ == "__main__":
    unittest.main()
