import MarkovDecisionProblem


class ValueIteration():

    def __init__(self, mdp=MarkovDecisionProblem.MarkovDecisionProblem(), deterministic=False, discount=0.9,
                 prob=None, rewards=None):

        if prob is None:
            prob = [0.7, 0.2, 0.1, 0]

        if rewards is None:
            rewards = [-0.04, 1, -1]

        self.mdp = mdp
        if deterministic:
            mdp.setDeterministic()
        else:
            mdp.setStochastic()

        self.discount = discount
        self.prob = prob
        self.rewards = rewards
        self.height = self.mdp.height
        self.width = self.mdp.width

        self.world = [[mdp.getReward(h, w) for w in range(self.width)] for h in range(self.height)]

        self.policy = []
        for h in range(self.height):
            self.policy.append([0] * self.width)

    def execute(self, iterations):
        for i in range(iterations):
            self.updateStates()
        self.updateAction()

    def updateAction(self):
        for height in range(self.height):
            for width in range(self.width):
                up = self.nextValue(height, width, 'u')
                down = self.nextValue(height, width, 'd')
                left = self.nextValue(height, width, 'l')
                right = self.nextValue(height, width, 'r')
                best = max(up, down, left, right)
                if best == up:
                    self.policy[height][width] = 'u'
                elif best == down:
                    self.policy[height][width] = 'd'
                elif best == left:
                    self.policy[height][width] = 'l'
                elif best == right:
                    self.policy[height][width] = 'r'

    def updateStates(self):
        newWorld = self.world.copy()
        for height in range(self.height):
            for width in range(self.width):
                if self.mdp.world[height][width] == 'e':
                    qValues = self.newStates(height, width)
                    self.updateValue(qValues[0], qValues[1], qValues[2], qValues[3], height, width, newWorld)
        self.world = newWorld.copy()

    def updateValue(self, up, down, left, right, height, width, newWorld):
        best = max(up, down, left, right)
        if best == up:
            newWorld[height][width] = up
            self.policy[height][width] = 'u'
        elif best == down:
            newWorld[height][width] = down
            self.policy[height][width] = 'd'
        elif best == left:
            newWorld[height][width] = left
            self.policy[height][width] = 'l'
        elif best == right:
            newWorld[height][width] = right
            self.policy[height][width] = 'r'

    def newStates(self, height, width):
        qValues = [0, 0, 0, 0]

        # u
        qValues[0] = self.prob[0] * (
                self.nextField(height - 1, width, 'u') + self.discount * self.nextValue(height, width, 'u'))
        + \
            self.prob[1] * (
                self.nextField(height - 1, width, 'l') + self.discount * self.nextValue(height, width,'l')) + self.prob[
            1] * (
                self.nextField(height - 1, width, 'r') + self.discount * self.nextValue(height, width,'r')) + self.prob[
            2] * (
                self.nextField(height - 1, width, 'd') + self.discount * self.nextValue(height, width,'d'))
        # l
        qValues[2] = self.prob[1] * (
                self.nextField(height - 1, width, 'u') + self.discount * self.nextValue(height, width, 'u')) + \
                     self.prob[0] * (
                             self.nextField(height - 1, width, 'l') + self.discount * self.nextValue(height, width,
                                                                                                     'l')) + \
                     self.prob[2] * (
                             self.nextField(height - 1, width, 'r') + self.discount * self.nextValue(height, width,
                                                                                                     'r')) + \
                     self.prob[1] * (
                             self.nextField(height - 1, width, 'd') + self.discount * self.nextValue(height, width,
                                                                                                     'd'))
        # r
        qValues[3] = self.prob[1] * (
                self.nextField(height - 1, width, 'u') + self.discount * self.nextValue(height, width, 'u')) + \
                     self.prob[2] * (
                             self.nextField(height - 1, width, 'l') + self.discount * self.nextValue(height, width,
                                                                                                     'l')) + \
                     self.prob[0] * (
                             self.nextField(height - 1, width, 'r') + self.discount * self.nextValue(height, width,
                                                                                                     'r')) + \
                     self.prob[1] * (
                             self.nextField(height - 1, width, 'd') + self.discount * self.nextValue(height, width,
                                                                                                     'd'))
        # d
        qValues[1] = self.prob[2] * (
                self.nextField(height - 1, width, 'u') + self.discount * self.nextValue(height, width, 'u')) + \
                     self.prob[1] * (
                             self.nextField(height - 1, width, 'l') + self.discount * self.nextValue(height, width,
                                                                                                     'l')) + \
                     self.prob[1] * (
                             self.nextField(height - 1, width, 'r') + self.discount * self.nextValue(height, width,
                                                                                                     'r')) + \
                     self.prob[0] * (
                             self.nextField(height - 1, width, 'd') + self.discount * self.nextValue(height, width,
                                                                                                     'd'))

        return qValues

    def nextField(self, height, width, action):
        if width < 0 or width > self.width or height < 0 or height > self.height:
            if action == 'u':
                val = self.mdp.getReward(height + 1, width)
                return val
            elif action == 'd':
                val = self.mdp.getReward(height - 1, width)
                return val
            elif action == 'l':
                val = self.mdp.getReward(height, width + 1)
                return val
            elif action == 'r':
                val = self.mdp.getReward(height, width - 1)
                return val
        else:
            val = self.mdp.getReward(height, width)
            return val

    def nextValue(self, height, width, action):
        if width < 0 or width > self.width or height < 0 or height > self.height:
            if action == 'u':
                return self.world[height + 1][width]
            elif action == 'd':
                return self.world[height - 1][width]
            elif action == 'l':
                return self.world[height][width + 1]
            elif action == 'r':
                return self.world[height][width - 1]
        else:
            return self.world[height][width]

    # statefield = reward of next state, result of (w, h, action), using rewards[]
    # statevalue = returns the value of the next state (according to action), returns current state if next value is
    # out of bounds cell, or if current state is goal
