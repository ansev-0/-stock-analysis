from abc import ABCMeta, abstractmethod, abstractproperty, abstractclassmethod
import numpy as np

class EpsilonDecay(metaclass=ABCMeta):

    @abstractmethod
    def step(self):
        pass

    @abstractmethod
    def _decrement(self):
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractproperty
    def count(self):
        pass


class EpsilonLinear(EpsilonDecay):

    def __init__(self, min_epsilon, initial_epsilon, slope):
        self._count = None
        self.epsilon_is_min = None
        self.epsilon = None
        self.min_epsilon = min_epsilon
        self.initial_epsilon = initial_epsilon
        self.slope = slope
        self.reset()

    @property
    def count(self):
        return self._count


    def reset(self):
        self._count = 0
        self.epsilon_is_min = False
        self.epsilon = self.initial_epsilon

    def step(self):

        
        if not self.epsilon_is_min:
            self._decrement()

            if self.epsilon <= self.min_epsilon:
                self.epsilon = self.min_epsilon
                self.epsilon_is_min = True
        self._count +=1       
        return self.epsilon
            


    def _decrement(self):
        self.epsilon -= self.slope 


class EpsilonPower(EpsilonDecay):

    def __init__(self, min_epsilon, initial_epsilon, factor):
        self._count = None
        self.epsilon_is_min = None
        self.epsilon = None
        self.min_epsilon = min_epsilon
        self.initial_epsilon = initial_epsilon
        self.factor = factor
        self.reset()

    @property
    def count(self):
        return self._count

    def reset(self):
        self._count = 0
        self.epsilon_is_min = False
        self.epsilon = self.initial_epsilon

    def step(self):
        if not self.epsilon_is_min:
            self._decrement()

            if self.epsilon <= self.min_epsilon:
                self.epsilon = self.min_epsilon
                self.epsilon_is_min = True
        self._count +=1       
        return self.epsilon
            


    def _decrement(self):
        self.epsilon *= self.factor



class EpsilonExp(EpsilonDecay):

    def __init__(self, min_epsilon, initial_epsilon, tau):
        self._count = None
        self.epsilon_is_min = None
        self.epsilon = None
        self.min_epsilon = min_epsilon
        self.initial_epsilon = initial_epsilon
        self.tau = tau
        self.reset()

    @property
    def count(self):
        return self._count

    @property
    def initial_epsilon(self):
        return self._initial_epsilon

    @initial_epsilon.setter
    def initial_epsilon(self, initial_epsilon):
        self._initial_epsilon = initial_epsilon
        self._update_b()

    @property
    def min_epsilon(self):
        return self._min_epsilon

    @min_epsilon.setter
    def min_epsilon(self, min_epsilon):
        self._min_epsilon = min_epsilon
        self._update_b()

    def reset(self):
        self._count = 0
        self.epsilon_is_min = False
        self.epsilon = self.initial_epsilon

    def step(self):

        if not self.epsilon_is_min:

            self._decrement()
            if self.epsilon <= self.min_epsilon:
                self.epsilon = self.min_epsilon
                self.epsilon_is_min = True

        self._count += 1 
        return self.epsilon


    def _decrement(self):
        self.epsilon = self.min_epsilon + self._b * np.exp(-self.tau * self._count)
        self._count += 1

    def _update_b(self):
        self._b = self._initial_epsilon - self._min_epsilon




    
decay = EpsilonPower(min_epsilon=0.1, initial_epsilon=1, factor=0.99)
