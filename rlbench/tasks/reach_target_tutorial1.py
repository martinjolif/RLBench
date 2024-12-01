from typing import List
from rlbench.backend.task import Task
from pyrep.objects import ProximitySensor, Shape
from rlbench.backend.conditions import DetectedCondition
from rlbench.const import colors
from rlbench.backend.spawn_boundary import SpawnBoundary
import numpy as np

class ReachTargetTutorial1(Task):

    def init_task(self) -> None:
        # TODO: This is called once when a task is initialised.
        self.target = Shape('target')
        self.distractor0 = Shape('distractor0')
        self.distractor1 = Shape('distractor1')
        self.boundary = Shape('boundary')
        success_sensor = ProximitySensor('success')
        self.register_success_conditions([
            DetectedCondition(self.robot.arm.get_tip(), success_sensor)
        ])

    def init_episode(self, index: int) -> List[str]:
        # TODO: This is called at the start of each episode.
        color_name, color_rgb = colors[index]
        color_choices = np.random.choice(list(range(index)) + list(
            range(index+1, len(colors))), size=2, replace=False)
        for ob, i in zip([self.distractor0, self.distractor1],
                color_choices):
            ob.set_color(colors[i][1])
        self.target.set_color(color_rgb)
        b = SpawnBoundary([self.boundary])
        for ob in [self.target, self.distractor0, self.distractor1]:
            b.sample(ob, min_distance=0.2, min_rotation=(0, 0, 0),
                    max_rotation=(0, 0, 0))
        return ['reach the %s target' % color_name,
                'reach the %s thing' % color_name]

    def variation_count(self) -> int:
        # TODO: The number of variations for this task.
        return len(colors)

    def base_rotation_bounds(self):
        return [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]

    def is_static_workspace(self):
        return True
