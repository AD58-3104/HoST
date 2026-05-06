from legged_gym.envs.base.legged_robot_config import LeggedRobotCfg, LeggedRobotCfgPPO


class K1Cfg( LeggedRobotCfg ):
    class init_state( LeggedRobotCfg.init_state ):
        pos = [0.0, 0.0, 0.25] # x,y,z [m] - lying flat on ground
        rot = [0.0, 1, 0, 1.0] # x,y,z,w [quat] - prone position (on belly)
        target_joint_angles = { # = target angles [rad] when action = 0.0
            # head
            'AAHead_yaw': 0.0,
            'Head_pitch': 0.0,
            # left arm
            'ALeft_Shoulder_Pitch': 0.0,
            'Left_Shoulder_Roll': 0.3,
            'Left_Elbow_Pitch': 0.0,
            'Left_Elbow_Yaw': -0.5,
            # right arm
            'ARight_Shoulder_Pitch': 0.0,
            'Right_Shoulder_Roll': -0.3,
            'Right_Elbow_Pitch': 0.0,
            'Right_Elbow_Yaw': 0.5,
            # left leg
            'Left_Hip_Pitch': -0.1,
            'Left_Hip_Roll': 0.0,
            'Left_Hip_Yaw': 0.0,
            'Left_Knee_Pitch': 0.3,
            'Left_Ankle_Pitch': -0.2,
            'Left_Ankle_Roll': 0.0,
            # right leg
            'Right_Hip_Pitch': -0.1,
            'Right_Hip_Roll': 0.0,
            'Right_Hip_Yaw': 0.0,
            'Right_Knee_Pitch': 0.3,
            'Right_Ankle_Pitch': -0.2,
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
            'Left_Hip_Pitch': -0.1,
            'Left_Hip_Roll': 0.0,
            'Left_Hip_Yaw': 0.0,
            'Left_Knee_Pitch': 0.3,
            'Left_Ankle_Pitch': -0.2,
            'Left_Ankle_Roll': 0.0,
            'Right_Hip_Pitch': -0.1,
            'Right_Hip_Roll': 0.0,
            'Right_Hip_Yaw': 0.0,
            'Right_Knee_Pitch': 0.3,
            'Right_Ankle_Pitch': -0.2,
            'Right_Ankle_Roll': 0.0,
        }

    class env(LeggedRobotCfg.env):
        num_one_step_observations = 73  # K1 has 22 DoF (no waist)
        num_actions = 22
        num_dofs = 22
        num_actor_history = 6
        num_observations = num_actor_history * num_one_step_observations
        episode_length_s = 10 # episode length in seconds
        unactuated_timesteps = 30

    class control( LeggedRobotCfg.control ):
        # PD Drive parameters:
        control_type = 'P'
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
            'Knee': 5,
            'Ankle': 1,
            'Shoulder': 2,
            'Elbow': 2,
            'Head': 1,
        }  # [N*m/rad]
        # action scale: target angle = actionScale * action + defaultAngle
        action_scale = 1
        # decimation: Number of control action updates @ sim DT per policy DT
        decimation = 4

    class terrain:
        mesh_type = 'plane' # "heightfield" # none, plane, heightfield or trimesh
        horizontal_scale = 0.1 # [m]
        vertical_scale = 0.005 # [m]
        border_size = 25 # [m]
        curriculum = True
        static_friction = 0.8
        dynamic_friction = 0.7
        restitution = 0.3
        # rough terrain only:
        measure_heights = True
        measured_points_x = [-0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0., 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
        measured_points_y = [-0.5, -0.4, -0.3, -0.2, -0.1, 0., 0.1, 0.2, 0.3, 0.4, 0.5]
        selected = False # select a unique terrain type and pass all arguments
        terrain_kwargs = None # Dict of arguments for selected terrain
        max_init_terrain_level = 5 # starting curriculum state
        terrain_length = 8.
        terrain_width = 8.
        num_rows = 1 # number of terrain rows (levels)
        num_cols = 20 # number of terrain cols (types)
        # terrain types: [smooth slope, rough slope, stairs up, stairs down, discrete]
        terrain_proportions = [1, 0., 0, 0, 0]
        # trimesh only:
        slope_treshold = 0.75 # slopes above this threshold will be corrected to vertical surfaces

    class asset( LeggedRobotCfg.asset ):
        file = '{LEGGED_GYM_ROOT_DIR}/resources/robots/k1/K1_22dof.urdf'
        name = "k1"
        left_foot_name = "Left_Ankle_Pitch"
        right_foot_name = "Right_Ankle_Pitch"
        left_knee_name = 'Left_Knee_Pitch'
        right_knee_name = 'Right_Knee_Pitch'
        left_thigh_name = 'Left_Hip_Pitch'
        right_thigh_name = 'Right_Hip_Pitch'
        foot_name = "Ankle_Roll"
        penalize_contacts_on = ["Elbow", 'Shoulder', 'Knee', 'Hip']
        terminate_after_contacts_on = []
        self_collisions = 0 # 1 to disable, 0 to enable...bitwise filter
        flip_visual_attachments = False

        left_leg_joints = ['Left_Hip_Pitch', 'Left_Hip_Roll', 'Left_Hip_Yaw', 'Left_Knee_Pitch', 'Left_Ankle_Pitch', 'Left_Ankle_Roll']
        right_leg_joints = ['Right_Hip_Pitch', 'Right_Hip_Roll', 'Right_Hip_Yaw', 'Right_Knee_Pitch', 'Right_Ankle_Pitch', 'Right_Ankle_Roll']
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

        left_arm_joints = ['ALeft_Shoulder_Pitch', 'Left_Shoulder_Roll', 'Left_Elbow_Pitch', 'Left_Elbow_Yaw']
        right_arm_joints = ['ARight_Shoulder_Pitch', 'Right_Shoulder_Roll', 'Right_Elbow_Pitch', 'Right_Elbow_Yaw']
        knee_joints = ['Left_Knee_Pitch', 'Right_Knee_Pitch']
        ankle_joints = ['Left_Ankle_Pitch', 'Left_Ankle_Roll', 'Right_Ankle_Pitch', 'Right_Ankle_Roll']

        density = 0.001
        angular_damping = 0.01
        linear_damping = 0.01
        max_angular_velocity = 1000.
        max_linear_velocity = 1000.
        armature = 0.01
        thickness = 0.01

    class rewards( LeggedRobotCfg.rewards ):
        soft_dof_pos_limit = 0.9
        soft_dof_vel_limit = 0.9
        base_height_target = 0.65
        base_height_sigma = 0.25
        tracking_dof_sigma = 0.25
        only_positive_rewards = False
        orientation_sigma = 1
        is_gaussian = True
        target_head_height = 1
        target_head_margin = 1
        target_base_height_phase1 = 0.35
        target_base_height_phase2 = 0.45
        target_base_height_phase3 = 0.65
        orientation_threshold = 0.99
        left_foot_displacement_sigma = -2
        right_foot_displacement_sigma = -2
        target_dof_pos_sigma = -0.1
        tracking_sigma = 0.25

        reward_groups = ['task', 'regu', 'style', 'target']
        num_reward_groups = len(reward_groups)
        reward_group_weights = [1, 0.1, 1, 1]

        class scales:
            task_orientation = 1
            task_head_height = 1

    class constraints( LeggedRobotCfg.rewards ):
        is_gaussian = True
        target_head_height = 1
        target_head_margin = 1
        orientation_height_threshold = 0.9
        target_base_height = 0.45

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

            # style reward
            style_hip_yaw_deviation = -10
            style_hip_roll_deviation = -10
            style_hip_pitch_deviation = -10
            style_shoulder_roll_deviation = -2.5
            style_left_foot_displacement = 2.5
            style_right_foot_displacement = 2.5
            style_knee_deviation = -0.25
            style_thigh_ori = 10
            style_feet_distance = -10
            style_style_ang_vel_xy = 25

            # post-task reward
            target_ang_vel_xy = 10
            target_lin_vel_xy = 10
            target_feet_height_var = 2.5
            target_target_upper_dof_pos = 10
            target_lower_body_deviation = 10
            target_target_orientation = 10
            target_target_base_height = 10

    class domain_rand:
        use_random = True

        randomize_actuation_offset = use_random
        actuation_offset_range = [-0.05, 0.05]

        randomize_motor_strength = use_random
        motor_strength_range = [0.9, 1.1]

        randomize_payload_mass = use_random
        payload_mass_range = [-2, 5]

        randomize_com_displacement = use_random
        com_displacement_range = [-0.03, 0.03]

        randomize_link_mass = use_random
        link_mass_range = [0.8, 1.2]

        randomize_friction = use_random
        friction_range = [0.1, 1]

        randomize_restitution = use_random
        restitution_range = [0.0, 1.0]

        randomize_kp = use_random
        kp_range = [0.85, 1.25]

        randomize_kd = use_random
        kd_range = [0.85, 1.25]

        randomize_initial_joint_pos = True
        initial_joint_pos_scale = [0.9, 1.1]
        initial_joint_pos_offset = [-0.1, 0.1]

        push_robots = False
        push_interval_s = 10
        max_push_vel_xy = 0.5

    class normalization:
        class obs_scales:
            lin_vel = 2.0
            ang_vel = 0.25
            dof_pos = 1.0
            dof_vel = 0.05
            height_measurements = 5.0

        clip_observations = 100.
        clip_actions = 100.

class K1CfgPPO( LeggedRobotCfgPPO ):
    class runner( LeggedRobotCfgPPO.runner ):
        experiment_name = 'k1_ground_prone'
        run_name = ''
        load_run = -1
        checkpoint = -1

    class policy( LeggedRobotCfgPPO.policy ):
        init_noise_std = 1.0
        actor_hidden_dims = [512, 256, 128]
        critic_hidden_dims = [512, 256, 128]

    class algorithm( LeggedRobotCfgPPO.algorithm ):
        entropy_coef = 0.01
        learning_rate = 1.e-3
        num_learning_epochs = 5
        num_mini_batches = 4 # mini batch size = num_envs*num_steps / num_mini_batches
        gamma = 0.99
        lam = 0.95
        num_env_steps = 50 # number of steps before updating
        ppo_clip_range = 0.2
        value_loss_coef = 1.0
        use_clipped_value_loss = True
        clip_val = True
        momentum_loss_coef = 0.0