from gym.envs.registration import register

register(
    id='guessthenumber-v0',
    entry_point='gym_guessthenumber.envs:guessthenumber',
)