# encoding: UTF-8

import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')


def plot_distribution(scores, value, color="#74d336", alpha=1):
    plt.hist(scores[value], color=color, alpha=alpha)