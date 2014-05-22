from __future__ import division
import math
import numpy as np
import matplotlib.pyplot as plt


def load_train_data(train_x,train_y):
	file_x="usps_digital/tr_X.txt";
	train_xc=np.loadtxt(file_x,delimiter=',');
	
	for i in range(train_x.shape[0]):
		for j in range(train_x.shape[1]):
			train_x[i,j]=int(train_xc[i,j]);
	
	
	file_y="usps_digital/tr_y.txt";
	train_yc=np.loadtxt(file_y);
	
	for i in range(train_y.shape[0]):
		train_y[i,0]=int(train_yc[i]);
		
	print "Loaded training data....."
	
	return;

def load_test_data(test_x,test_y):
	file_x="usps_digital/te_X.txt";
	test_xc=np.loadtxt(file_x,delimiter=',');
	
	for i in range(test_x.shape[0]):
		for j in range(test_x.shape[1]):
			test_x[i,j]=int(test_xc[i,j]);
			
	file_y="usps_digital/te_y.txt";
	test_yc=np.loadtxt(file_y);
	
	for i in range(test_y.shape[0]):
		test_y[i]=int(test_yc[i]);
	
	print "Loaded Test data......"
	return;

def prob_yk(data_x,wt_vec,example,col_no,n_classes):
	num=0;
	den=0;
	num=math.exp(np.dot(data_x[example,:],wt_vec[:,col_no]));
	for j in range(n_classes):
		den+=math.exp(np.dot(data_x[example,:],wt_vec[:,j]));
		
	return num/den;
	
	
def calc_log_like(train_y,train_x,wt_vec):
	n_train_ex=train_y.shape[0];
	n_classes=wt_vec.shape[1];
	
	log_like=0;
	
	for example in range(n_train_ex):
		col_no= int(train_y[example])-1;
	
		p_yk=prob_yk(train_x,wt_vec,example,col_no,n_classes);
		log_like+=math.log(p_yk);
	
	return log_like;

def calc_acc(train_y,train_x,wt_vec):
	n_classes=wt_vec.shape[1];
	n_examples=train_y.shape[0];
	#n_examples=10;
	correct_ex=0;
	max_prob=0;
	max_index=0;
	
	for example in range(n_examples):
		#reset
		max_prob=0;
		max_index=0;
		
		for K in range(n_classes):
			p_yk=prob_yk(train_x,wt_vec,example,K,n_classes);
			if(p_yk>max_prob):
				max_prob=p_yk;
				max_index=K;
		#print max_prob;
		if(max_index+1)==int(train_y[example]):
			correct_ex+=1;
		#print correct_ex;
			
	return correct_ex/n_examples;


def update_weights(train_y,train_x,wt_vec,learn_rate,lamda,epsilon):
	n_classes=wt_vec.shape[1];
	n_features=wt_vec.shape[0];
	n_train_ex=train_y.shape[0];
	
	del_wt=np.zeros((n_features,n_classes));
	
	
	for K in range(n_classes-1):
		log_min=np.zeros((1,n_features));
		for example in range(n_train_ex):
			p_yk=prob_yk(train_x,wt_vec,example,K,n_classes);
			log_min=log_min+(-train_x[example,:]*p_yk);
			if train_y[example]==(K+1):
				log_min=log_min+train_x[example,:];
	
		for index in range(n_features):		
			del_wt[index,K]=-lamda*wt_vec[index,K]+log_min[0,index];
	#print del_wt[0,:]	
	
	for i in range(wt_vec.shape[0]):
		for j in range(wt_vec.shape[1]):
			wt_vec[i,j]=wt_vec[i,j]+learn_rate*del_wt[i,j];#Update	
	
	print np.amax(np.absolute(del_wt));
	if np.amax(np.absolute(del_wt))<epsilon:
		stop=True;
		print np.amax(np.absolute(del_wt));
	else:
		stop=False;
	return stop;
	
	
def writetofile(x_data,y_data,filename):
	file1=open(filename,'w');
	N=len(x_data);
	N1=len(y_data);
	if N!=N1:
		print "X and Y lists not equal in length";
	for index in range(N):
		str_index=str(x_data[index])+"\t"+str(y_data[index])+"\n";
		file1.write(str_index);
	file1.close();
	return;
	

def main():
	#Parameters
	learn_rate=0.0002;
	lamda=0;
	n_train_ex=6000;
	n_test_ex=5000;
	n_features=256;
	n_classes=10;
	
	iter_no=[];
	train_acc=[];
	test_acc=[];
	log_like=[];
	
	wt_vec=np.zeros((n_features,n_classes));#K=9 rows and d=256 columns
	#init_weights(wt_vec);#initialize weights with random values
	train_x=np.zeros((n_train_ex,n_features));
	test_x=np.zeros((n_test_ex,n_features));
	train_y=np.zeros((n_train_ex,1));
	test_y=np.zeros((n_test_ex,1));
	
	load_train_data(train_x,train_y);
	load_test_data(test_x,test_y);
	
	epsilon=0.5;#Stopping criterion of testing accuracy
	
	acc_improve=1;
	counter=0;
	fig=plt.figure();
	plt.ion();
	plt.show();
	stop=False;
	#while (~stop):
	for i in range(1000):
		counter+=1;
		iter_no.append(counter);
		log_like.append(calc_log_like(train_y,train_x,wt_vec));
		#print log_like[-1];
		plt.plot(iter_no,log_like,'ro');
		plt.draw();
		train_acc.append(calc_acc(train_y,train_x,wt_vec));
		#print train_acc[-1];
		
		test_acc.append(calc_acc(test_y,test_x,wt_vec));

		stop=update_weights(train_y,train_x,wt_vec,learn_rate,lamda,epsilon);
		#print wt_vec[0,:]
		print str(counter)+". Accuracy: "+str(test_acc[-1]);
		
	writetofile(iter_no,log_like,"log_like.txt");
	writetofile(iter_no,train_acc,"train_acc.txt");
	writetofile(iter_no,test_acc,"test_acc.txt");
	plt.close()		
			
	
if __name__ == "__main__":
	main()
