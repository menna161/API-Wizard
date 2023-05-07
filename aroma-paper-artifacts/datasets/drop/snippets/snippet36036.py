from django.contrib.auth.models import User
from django.test import TestCase
from auvsi_suas.models import mission_config
from auvsi_suas.models import mission_evaluation
from auvsi_suas.models import test_utils
from auvsi_suas.proto import interop_admin_api_pb2


def test_air_drop(self):
    'Test the air drop scoring.'
    judge = self.eval.feedback.judge
    air = self.eval.score.air_drop
    mission_evaluation.score_team(self.eval)
    self.assertAlmostEqual(0.25, air.drop_accuracy)
    self.assertAlmostEqual(0, air.drive_to_location)
    self.assertAlmostEqual(0.125, air.score_ratio)
    judge.air_drop_accuracy = interop_admin_api_pb2.MissionJudgeFeedback.WITHIN_05_FT
    judge.ugv_drove_to_location = True
    mission_evaluation.score_team(self.eval)
    self.assertAlmostEqual(1, air.drop_accuracy)
    self.assertAlmostEqual(1, air.drive_to_location)
    self.assertAlmostEqual(1, air.score_ratio)
    judge.air_drop_accuracy = interop_admin_api_pb2.MissionJudgeFeedback.WITHIN_15_FT
    judge.ugv_drove_to_location = True
    mission_evaluation.score_team(self.eval)
    self.assertAlmostEqual(0.5, air.drop_accuracy)
    self.assertAlmostEqual(1, air.drive_to_location)
    self.assertAlmostEqual(0.75, air.score_ratio)
