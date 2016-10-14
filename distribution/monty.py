from distribution import Distribution, DistGroup

# Monty hall problem

# you have chosen door A. Do you switch to win a car?

# D: 
# Monty opens door B _and_ there is no car there

# H:
# 1: the car is behind door A:
#       p(open A): 0    (we picked A)
#       p(open B): .5
#       p(open C): .5
hypo_1 = Distribution(name='1')
hypo_1.update({'A': 0, 'B': 0.5, 'C': 0.5})

# 2: the car is behind door B:
#       p(open A): 0    
#       p(open B): 0
#       p(open C): 1
hypo_2 = Distribution(name='2')
hypo_2.update({'A': 0, 'B': 0, 'C': 1})

# 3: the car is behind door C:
#       p(open A): 0    
#       p(open B): 1
#       p(open C): 0
hypo_3 = Distribution(name='3')
hypo_3.update({'A': 0, 'B': 1, 'C': 0})

# Priors
doors = DistGroup([hypo_1, hypo_2, hypo_3])

print('{:^5} {:<12} {:<12} {:<12} {:<12}'.format(' ', 'P(H)', 'P(D|H)', 'P(H)*P(D|H)', 'P(H|D)'))
for d in doors:
    prior = doors.P(d.name)
    likelihood = d.P('B')
    print('{:^5} {:<12.5f} {:<12.5f} {:<12.5f} {:<12.5f}'.format(d.name,
                                                                 prior,
                                                                 likelihood,
                                                                 prior * likelihood,
                                                                 prior * likelihood / doors.normalizer('B')))
