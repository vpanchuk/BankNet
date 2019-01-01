import os
import json
import random
import numpy as np
from django.db.models import Max, Min
from .libraries.KohonenNet import KohonenNet

class Method():
    __method = None
    __ratio_step = None
    __upper_random = 0.3
    __lower_random = -0.3
    __criteria_length = 5
    __test_sample_max = None
    __ratio_upper_limit = None
    __ratio_lower_limit = None
    __project_dir = os.getcwd() + os.sep + 'bankproject' + os.sep + 'data' + os.sep
    __statuses = {
        0: 'Не установлен',
        1: 'В состоянии дефолта ',
        2: 'Очень высокий кредитный риск',
        3: 'В высокой степени спекулятивный',
        4: 'Обязательства высокого качества'
    }
            
    @staticmethod
    def get_weight():
        with open(Method.__project_dir + Method.__method + 'Result.json') as data_file:    
            weight = json.load(data_file)
        return weight
            
    @staticmethod
    def set_weight(weight, points):
        solver = KohonenNet()
        solver.method = Method.__method
        for ratio in np.arange(Method.__ratio_upper_limit, Method.__ratio_lower_limit, -Method.__ratio_step):
            solver.ratio = ratio
            weight = solver.solve(points[:Method.__test_sample_max], weight)
        with open(Method.__project_dir + Method.__method + 'Result.json', 'w') as outfile:
            json.dump(weight, outfile)
        return True

    @staticmethod
    def make_retings(ratings, method):
        try:
            solver = KohonenNet()
            Method.__method = method
            weight = Method.get_weight()
            solver.method = Method.__method
            points = Method.normalize_ratings(ratings)
            for index, rating in enumerate(ratings):
                distance = []
                for claster in weight:
                    if Method.__method == 'byEuclid':
                        distance.append(solver.distance([a_i-b_i for a_i, b_i in zip(points[index], claster)]))
                    elif Method.__method == 'byAngle':
                        distance.append(solver.angle(points[index], claster))
                    else:
                        break
                rating.rating = Method.__statuses[distance.index(min(distance))]
            return ratings
        except Exception:
            return False
            
    @staticmethod
    def normalize_ratings(ratings):
        points = []
        normalize = lambda min, max, number: (number - min) / (max - min)
        term_min = ratings.aggregate(Min('term'))['term__min']
        term_max = ratings.aggregate(Max('term'))['term__max']
        volume_min = ratings.aggregate(Min('volume'))['volume__min']
        volume_max = ratings.aggregate(Max('volume'))['volume__max']
        risk_level_min = ratings.aggregate(Min('risk_level'))['risk_level__min']
        risk_level_max = ratings.aggregate(Max('risk_level'))['risk_level__max']
        wages_min = ratings.aggregate(Min('wages'))['wages__min']
        wages_max = ratings.aggregate(Max('wages'))['wages__max'] 
        for rating in ratings:
            points.append([
                normalize(term_min, term_max, rating.term),
                normalize(volume_min, volume_max, rating.volume),
                normalize(risk_level_min, risk_level_max, rating.risk_level),
                int(rating.credit_history),
                normalize(wages_min, wages_max, rating.wages)
            ])            
        return points
    
    @staticmethod    
    def save(ratings, samples_count, ratio_upper_limit, ratio_lower_limit, ratio_step, method):
        try:
            Method.__method = str(method)
            Method.__ratio_step = float(ratio_step)
            Method.__test_sample_max = int(samples_count)
            Method.__ratio_upper_limit = float(ratio_upper_limit)
            Method.__ratio_lower_limit = float(ratio_lower_limit)
            weight = [
                [random.uniform(Method.__lower_random, Method.__upper_random) for _ in range(Method.__criteria_length)]
                for _ in range(Method.__criteria_length)
            ]
            Method.set_weight(weight, Method.normalize_ratings(ratings))
        except Exception:
            return False
        return True