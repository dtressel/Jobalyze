print('*************************running test-models.py********************************')
"""Model tests."""

# run these tests with command:
#    python -m unittest test_models.py

import os
from unittest import TestCase

from models import db, User, SavedJob, JobApp, JobHunt, Strategy, app_strategy, datetime

# Use test database:
os.environ['DATABASE_URL'] = "postgresql:///jobalyze_test"

from app import app

# Drop old tables, create new tables:
with app.app_context():
    db.drop_all()
    db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        with app.app_context():
            User.query.delete()
            SavedJob.query.delete()
            JobApp.query.delete()
            JobHunt.query.delete()
            Strategy.query.delete()
            # app_strategy.query.delete()
            db.session.commit()

        self.client = app.test_client()

    # def tearDown(self):
    #     """rollback session after tests."""

    #     with app.app_context():
    #         db.session.rollback()
    #         User.query.delete()
    #         SavedJob.query.delete()
    #         JobApp.query.delete()
    #         JobHunt.query.delete()
    #         Strategy.query.delete()
    #         # app_strategy.query.delete()
    #         db.session.commit()

    def test_user_model(self):
        """something here"""

        with app.app_context():
            user1 = User(
                email="test1@test.com",
                username="testuser1",
                password="HASHED_PASSWORD1"
            )

            user2 = User(
                email="test2@test.com",
                username="testuser2",
                password="HASHED_PASSWORD2"
            )

            db.session.add_all([user1, user2])
            db.session.commit()

            saved_job1 = SavedJob(
                user_id=user1.id,
                company='Google',
                title='Junior Software Engineer'
            )
            saved_job2 = SavedJob(
                user_id=user1.id,
                company='Facebook',
                title='Database Engineer'
            )
            saved_job3 = SavedJob(
                user_id=user2.id,
                company='Microsoft',
                title='Frontend Developer'
            )

            db.session.add_all([saved_job1, saved_job2, saved_job3])
            db.session.commit()

            job_hunt1 = JobHunt(
                job_title_desired='Junior Software Engineer',
                user_id=user1.id
            )
            job_hunt2 = JobHunt(
                job_title_desired='Backend Developer',
                user_id=user2.id
            )

            db.session.add_all([job_hunt1, job_hunt2])
            db.session.commit()

            job_app1 = JobApp(
                id=saved_job1.id,
                job_hunt_id=job_hunt1.id
            )
            job_app2 = JobApp(
                id=saved_job2.id,
                job_hunt_id=job_hunt1.id
            )
            job_app3 = JobApp(
                id=saved_job3.id,
                job_hunt_id=job_hunt2.id
            )

            db.session.add_all([job_app1, job_app2, job_app3])
            db.session.commit()

            strategy1 = Strategy(
                name='wrote coverletter',
                job_hunt_id=job_hunt1.id
            )
            strategy2 = Strategy(
                name='local company',
                job_hunt_id=job_hunt1.id
            )
            strategy3 = Strategy(
                name='resume 1',
                job_hunt_id=job_hunt2.id
            )

            db.session.add_all([strategy1, strategy2])
            db.session.commit()

            job_app1.strategies.extend([strategy1, strategy2])
            job_app2.strategies.append(strategy1)
            job_app3.strategies.append(strategy3)
            db.session.commit()

            db.session.delete(user1)
            db.session.commit()

