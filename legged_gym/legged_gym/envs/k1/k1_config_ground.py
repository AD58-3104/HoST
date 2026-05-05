from legged_gym.envs.base.legged_robot_config import LeggedRobotCfg, LeggedRobotCfgPPO


# Booster Robotics K1 (22 DoF humanoid)
# Joint inventory:
#   Head (2):   AAHead_yaw, Head_pitch
#   Arms (8):   A{Left,Right}_Shoulder_Pitch, {Left,Right}_Shoulder_Roll,
#               {Left,Right}_Elbow_Pitch,     {Left,Right}_Elbow_Yaw
#   Legs (12):  {Left,Right}_Hip_{Pitch,Roll,Yaw}, {Left,Right}_Knee_Pitch,
#               {Left,Right}_Ankle_{Pitch,Roll}
# K1 has no waist joint, so style_waist_deviation is omitted.
class K1Cfg( LeggedRobotCfg ):
    class init_state( LeggedRobotCfg.init_state ):
        pos = [0.0, 0.0, 0.4] # x,y,z [m] - lying-down spawn height
        rot = [0.0, -1, 0, 1.0] # x,y,z,w [quat] - rotated so robot starts on its back
        target_joint_angles = { # = target angles [rad] when action = 0.0
            # head
            'AAHead_yaw': 0.0,
            'Head_pitch': 0.0,
            # left arm (target a slightly outward shoulder so arms don't tangle)
            'ALeft_Shoulder_Pitch': 0.0,
            'Left_Shoulder_Roll': 0.3,
            'Left_Elbow_Pitch': 0.0,
            'Left_Elbow_Yaw': -0.5,
            # right arm
            'ARight_Shoulder_Pitch': 0.0,
            'Right_Shoulder_Roll': -0.3,
            'Right_Elbow_Pitch': 0.0,
            'Right_Elbow_Yaw': 0.5,
            # left leg (slight crouch as standing target)
            'Left_Hip_Pitch': -0.3,
            'Left_Hip_Roll': 0.0,
            'Left_Hip_Yaw': 0.0,
            'Left_Knee_Pitch': 0.6,
            'Left_Ankle_Pitch': -0.3,
            'Left_Ankle_Roll': 0.0,
            # right leg
            'Right_Hip_Pitch': -0.3,
            'Right_Hip_Roll': 0.0,
            'Right_Hip_Yaw': 0.0,
            'Right_Knee_Pitch': 0.6,
            'Right_Ankle_Pitch': -0.3,
            'Right_Ankle_Roll': 0.0,
        }

        default_joint_angles = {
            'AAHead_yaw': 0.0,
            'Head_pitch': 0.0,
            'ALeft_Shoulder_Pitch': 0.0,
            'Left_Shoulder_Roll': 0.0,
            'Left_Elbow_Pitch': 0.0,
            'Left_Elbow_Yaw': 0.0,
            'ARight_Shoulder_Pitch': 0.0,
            'Right_Shoulder_Roll': 0.0,
            'Right_Elbow_Pitch': 0.0,
            'Right_Elbow_Yaw': 0.0,
            'Left_Hip_Pitch': -0.3,
            'Left_Hip_Roll': 0.0,
            'Left_Hip_Yaw': 0.0,
            'Left_Knee_Pitch': 0.6,
            'Left_Ankle_Pitch': -0.3,
            'Left_Ankle_Roll': 0.0,
            'Right_Hip_Pitch': -0.3,
            'Right_Hip_Roll': 0.0,
            'Right_Hip_Yaw': 0.0,
            'Right_Knee_Pitch': 0.6,
            'Right_Ankle_Pitch': -0.3,
            'Right_Ankle_Roll': 0.0,
        }

    class env(LeggedRobotCfg.env):
        # observation = 4 (base ang vel:3 + height:1) + 3 (proj gravity)
        #             + 22 (dof_pos) + 22 (dof_vel) + 22 (last action) + 3 (commands?) -> use 76
        # Following G1's 76-dim layout (G1 has 23 DoF -> 76 obs); for K1 22 DoF use 73.
        num_one_step_observations = 73
        num_actions = 22
        num_dofs = 22
        num_actor_history = 6
        num_observations = num_actor_history * num_one_step_observations
        episode_length_s = 10
        unactuated_timesteps = 30

    class control( LeggedRobotCfg.control ):
        control_type = 'P'
        # K1 motor limits (effort): hip-pitch 30, hip-roll 35, hip-yaw 20,
        # knee 40, ankle 20, shoulder 14, elbow 14, head 6.
        # PD gains tuned smaller than H1 (which is heavier) but proportional.
        stiffness = {
            'Hip_Pitch': 100,
            'Hip_Roll': 100,
            'Hip_Yaw': 60,
            'Knee': 150,
            'Ankle': 30,
            'Shoulder': 50,
            'Elbow': 50,
            'Head': 20,
        }  # [N*m/rad]
        damping = {
            'Hip_Pitch': 3,
            'Hip_Roll': 3,
            'Hip_Yaw': 2,
            'Knee': 4,
            'Ankle': 1.5,
            'Shoulder': 2,
            'Elbow': 2,
            'Head': 1,
        }  # [N*m*s/rad]
        action_scale = 0.25
        decimation = 4

    class terrain:
        mesh_type = 'plane'
        horizontal_scale = 0.1
        vertical_scale = 0.005
        border_size = 25
        curriculum = True
        static_friction = 0.8
        dynamic_friction = 0.7
        restitution = 0.3
        measure_heights = True
        measured_points_x = [-0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0., 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
        measured_points_y = [-0.5, -0.4, -0.3, -0.2, -0.1, 0., 0.1, 0.2, 0.3, 0.4, 0.5]
        selected = False
        terrain_kwargs = None
        max_init_terrain_level = 5
        terrain_length = 8.
        terrain_width = 8.
        num_rows = 1
        num_cols = 20
        terrain_proportions = [1, 0., 0, 0, 0]
        slope_treshold = 0.75

    class asset( LeggedRobotCfg.asset ):
        file = '{LEGGED_GYM_ROOT_DIR}/resources/robots/k1/K1_22dof.urdf'
        name = "k1"

        # body-name substring matching (case-sensitive)
        left_foot_name = "left_foot_link"
        right_foot_name = "right_foot_link"
        foot_name = "foot_link"
        left_knee_name = 'Left_Shank'
        right_knee_name = 'Right_Shank'
        left_shoulder_name = 'Left_Arm_1'
        right_shoulder_name = 'Right_Arm_1'

        penalize_contacts_on = ["Hip", "Shank", "Arm"]
        terminate_after_contacts_on = []

        # exact-name DoF lookups
        left_leg_joints = ['Left_Hip_Pitch', 'Left_Hip_Roll', 'Left_Hip_Yaw',
                           'Left_Knee_Pitch', 'Left_Ankle_Pitch', 'Left_Ankle_Roll']
        right_leg_joints = ['Right_Hip_Pitch', 'Right_Hip_Roll', 'Right_Hip_Yaw',
                            'Right_Knee_Pitch', 'Right_Ankle_Pitch', 'Right_Ankle_Roll']

        # In HoST conventions, *_hip_joints holds the hip-yaw DoF
        left_hip_joints = ['Left_Hip_Yaw']
        right_hip_joints = ['Right_Hip_Yaw']
        left_hip_roll_joints = ['Left_Hip_Roll']
        right_hip_roll_joints = ['Right_Hip_Roll']
        left_hip_pitch_joints = ['Left_Hip_Pitch']
        right_hip_pitch_joints = ['Right_Hip_Pitch']

        left_shoulder_roll_joints = ['Left_Shoulder_Roll']
        right_shoulder_roll_joints = ['Right_Shoulder_Roll']

        left_knee_joints = ['Left_Knee_Pitch']
        right_knee_joints = ['Right_Knee_Pitch']

        left_arm_joints = ['ALeft_Shoulder_Pitch', 'Left_Shoulder_Roll',
                           'Left_Elbow_Pitch', 'Left_Elbow_Yaw']
        right_arm_joints = ['ARight_Shoulder_Pitch', 'Right_Shoulder_Roll',
                            'Right_Elbow_Pitch', 'Right_Elbow_Yaw']
        waist_joints = []  # K1 has no waist DoF
        knee_joints = ['Left_Knee_Pitch', 'Right_Knee_Pitch']
        ankle_joints = ['Left_Ankle_Pitch', 'Left_Ankle_Roll',
                        'Right_Ankle_Pitch', 'Right_Ankle_Roll']

        keyframe_name = "keyframe"
        head_name = 'keyframe_head'

        trunk_names = ["Trunk", "torso_link"]
        base_name = 'Trunk'

        # body-name substring lists for body-position rewards
        left_upper_body_names = ['Left_Arm_1', 'Left_Arm_3']
        right_upper_body_names = ['Right_Arm_1', 'Right_Arm_3']
        left_lower_body_names = ['Left_Hip_Pitch', 'left_foot_link', 'Left_Shank']
        right_lower_body_names = ['Right_Hip_Pitch', 'right_foot_link', 'Right_Shank']

        left_ankle_names = ['left_foot_link']
        right_ankle_names = ['right_foot_link']

        density = 0.001
        angular_damping = 0.01
        linear_damping = 0.01
        max_angular_velocity = 1000.
        max_linear_velocity = 1000.
        armature = 0.01
        thickness = 0.01
        self_collisions = 1  # 1 = disable self-collisions (small linkages can jitter)
        flip_visual_attachments = False

    class rewards( LeggedRobotCfg.rewards ):
        soft_dof_pos_limit = 0.9
        soft_dof_vel_limit = 0.9
        # K1 standing trunk height ≈ 0.51 m, top-of-head ≈ 0.89 m.
        base_height_target = 0.50
        only_positive_rewards = False
        orientation_sigma = 1
        is_gaussian = True
        target_head_height = 0.85
        target_head_margin = 0.85
        target_base_height_phase1 = 0.18  # ≈35% of standing trunk height
        target_base_height_phase2 = 0.18
        target_base_height_phase3 = 0.36  # ≈70% of standing trunk height
        orientation_threshold = 0.99
        left_foot_displacement_sigma = -2
        right_foot_displacement_sigma = -2
        target_dof_pos_sigma = -0.1
        tracking_sigma = 0.25

        reward_groups = ['task', 'regu', 'style', 'target']
        num_reward_groups = len(reward_groups)
        reward_group_weights = [2.5, 0.1, 1, 1]

        class scales:
            task_orientation = 1
            task_head_height = 1

    class constraints( LeggedRobotCfg.rewards ):
        is_gaussian = True
        target_head_height = 0.85
        target_head_margin = 0.85
        orientation_height_threshold = 0.9
        target_base_height = 0.50

        left_foot_displacement_sigma = -2
        right_foot_displacement_sigma = -2
        hip_yaw_var_sigma = -2
        target_dof_pos_sigma = -0.1
        post_task = False

        class scales:
            # regularization reward
            regu_dof_acc = -2.5e-7
            regu_action_rate = -0.01
            regu_smoothness = -0.01
            regu_torques = -2.5e-6
            regu_joint_power = -2.5e-5
            regu_dof_vel = -1e-3
            regu_joint_tracking_error = -0.00025
            regu_dof_pos_limits = -100.0
            regu_dof_vel_limits = -1

            # style reward (style_waist_deviation omitted: K1 has no waist)
            style_hip_yaw_deviation = -10
            style_hip_roll_deviation = -10
            style_shoulder_roll_deviation = -2.5
            style_left_foot_displacement = 2.5
            style_right_foot_displacement = 2.5
            style_knee_deviation = -0.25
            style_shank_orientation = 10
            style_ground_parallel = 20
            style_feet_distance = -10
            style_style_ang_vel_xy = 1

            # post-task reward
            target_ang_vel_xy = 10
            target_lin_vel_xy = 10
            target_feet_height_var = 2.5
            target_target_upper_dof_pos = 10
            target_target_orientation = 10
            target_target_base_height = 10

    class domain_rand:
        use_random = True

        randomize_actuation_offset = use_random
        actuation_offset_range = [-0.05, 0.05]

        randomize_motor_strength = use_random
        motor_strength_range = [0.9, 1.1]

        randomize_payload_mass = use_random
        payload_mass_range = [-1, 3]

        randomize_com_displacement = use_random
        com_displacement_range = [-0.03, 0.03]

        randomize_link_mass = use_random
        link_mass_range = [0.8, 1.2]

        randomize_friction = use_random
        friction_range = [0.1, 1]

        randomize_restitution = use_random
        restitution_range = [0.0, 1.0]

        randomize_kp = use_random
        kp_range = [0.85, 1.15]

        randomize_kd = use_random
        kd_range = [0.85, 1.15]

        randomize_initial_joint_pos = True
        initial_joint_pos_scale = [0.9, 1.1]
        initial_joint_pos_offset = [-0.1, 0.1]

        push_robots = False
        push_interval_s = 10
        max_push_vel_xy = 0.5

        delay = use_random
        max_delay_timesteps = 5

    class curriculum:
        pull_force = True
        # K1 ≈ 19 kg, weight ≈ 186 N -> 60% ≈ 112 N upward assistance.
        force = 110
        dof_vel_limit = 300
        base_vel_limit = 20
        threshold_height = 0.80
        no_orientation = False

    class sim:
        dt = 0.005
        substeps = 1
        gravity = [0., 0., -9.81]
        up_axis = 1

        class physx:
            num_threads = 10
            solver_type = 1
            num_position_iterations = 8
            num_velocity_iterations = 1
            contact_offset = 0.01
            rest_offset = 0.0
            bounce_threshold_velocity = 0.5
            max_depenetration_velocity = 1.0
            max_gpu_contact_pairs = 2**23
            default_buffer_size_multiplier = 5
            contact_collection = 2


class K1CfgPPO( LeggedRobotCfgPPO ):
    runner_class_name = 'OnPolicyRunner'

    class policy:
        init_noise_std = 0.8
        actor_hidden_dims = [512, 256, 128]
        critic_hidden_dims = [512, 256]

    class algorithm( LeggedRobotCfgPPO.algorithm ):
        entropy_coef = 0.01
        value_smoothness_coef = 0.1
        smoothness_upper_bound = 1.0
        smoothness_lower_bound = 0.1

    class runner( LeggedRobotCfgPPO.runner ):
        run_name = ''
        save_interval = 500
        experiment_name = 'k1_ground'
        algorithm_class_name = 'PPO'
        init_at_random_ep_len = True
        max_iterations = 12000
