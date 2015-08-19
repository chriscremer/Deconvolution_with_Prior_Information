
import numpy as np


from sklearn.decomposition import PCA
from sklearn.decomposition import NMF
from sklearn.decomposition import FastICA

from numpy.linalg import inv
from numpy.linalg import pinv

import weight_tools as wt

import global_variables as gv

import random

def init_model(init_type, numb_model_subpops, X):


	if init_type == 'Random_Values':
		Z = np.random.rand(numb_model_subpops, len(X[0]))
	elif init_type == 'Random_Samples':
		Z = X[random.sample(range(len(X)), numb_model_subpops)]
	elif init_type == 'PCA':
		pca = PCA(n_components=numb_model_subpops)
		pca.fit(X.T)
		Z = pca.transform(X.T).T		
	elif init_type == 'ICA':
		ica = FastICA(n_components=numb_model_subpops)
		ica.fit(X.T)
		Z = ica.transform(X.T).T
	else:
		print 'WHAT INITIALIZATION IS THIS?'		

	T = np.identity(len(Z))
	TZ = np.dot(T, Z)

	return TZ


def optimize_model(possible_Ws, TZ):

	printed = 0
	for i in range(200):

		#print 'Iter ' + str(i)

		#print 'selecting W'
		# W = select_w(X, possible_Ws, TZ)

		#this is the restricted way
		#W = wt.select_w_parallel(possible_Ws)

		#this is the non-constrained way
		# W = np.dot(pinv(np.dot(TZ,TZ.T)), np.dot(TZ, gv.X.T))
		# W = W.T

		#this is the new way
		W = wt.select_w_parallel_NEW()

		# print W

		#W = np.dot(pinv(np.identity(len(TZ))*0.01 + np.dot(TZ,TZ.T)), np.dot(TZ, gv.X.T))
		#print W.shape


		X_hat = np.dot(W, TZ)
		norm = np.linalg.norm(gv.X - X_hat)
		#print '         	Norm ' + str(norm)



		#print 'optimizig TZ'
		TZ = np.dot(pinv(np.dot(W.T,W)), np.dot(W.T, gv.X))


		# for row in range(len(TZ)):
		# 	for col in range(len(TZ[row])):
		# 		if TZ[row][col] < 0:
		# 			print 'HEGATIVE'

		gv.set_current_TZ(TZ)

		new_X_hat = np.dot(W, TZ)
		new_norm = np.linalg.norm(gv.X - new_X_hat)
		#print '         	Norm ' + str(new_norm)

		if norm == new_norm:
			print '# iters until optimized= ' + str(i)
			printed = 1
			break
	if printed == 0:
		print '# iters went to limit: ' + str(200)
	return W, TZ