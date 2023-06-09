import numpy as np
from collections import Counter
import time

class Utilities:
   
    def __init__(self, max_N, k, mesh_X, mesh_Y, pool_P, target_class_mesh):
        self.max_N = max_N
        self.K = k
        self.mesh_X = mesh_X
        self.mesh_Y = mesh_Y
        self.mesh_X_flat = mesh_X.flatten()
        self.mesh_Y_flat = mesh_Y.flatten()
        # self.mesh_X_Y = np.stack((self.mesh_X_flat, self.mesh_Y_flat), axis= -1)
        self.mesh_X_Y = pool_P[:,:2]
        self.pool_P = pool_P
        self.target_class_mesh = target_class_mesh
        self.target_class_mesh_flat = target_class_mesh.flatten().astype(int)
        
    # Take the one x,y coordinate, determine its class given a list of points and with labelled classes in the pool
    def knn(self, k, predicted_x, predicted_y, pool):
        predicted_dp = np.array([predicted_x, predicted_y])
        distances = predicted_dp - pool[:,:2] # predicted_dp will be broadcasted onto the right array during subtraction
        distances = np.power(distances, 2)
        # distances = distances[:,0:2] 
        distances = np.sum(distances, axis=1)
        # distances = np.sqrt(distances) # Unnecessary for correct computation
        vote_pool_indices = np.argsort(distances)[:k]
        vote_pool_classes = [int(pool[i][2]) for i in vote_pool_indices]
        
        vote_result = Counter(vote_pool_classes).most_common()
        return int(vote_result[0][0])
    
    def disagreement_func_ex(self, pool_D):

        classify_func = lambda xy: self.knn(self.K, xy[0], xy[1], pool_D)
        res = np.array(list(map(classify_func, self.mesh_X_Y)))
       
        res_diff = np.bitwise_xor(self.target_class_mesh_flat, res)
        
        return (np.mean(res_diff), pool_D, res) if len(pool_D) <= self.max_N else (np.inf, pool_D, res)