from __future__ import division
import math
import heapq

class MAP_prob:
	def __init__(self):
		self.c_ij=0.;
		self.p_ij=0.;

class MLE_prob:
	def __init__(self):
		self.n_ij=0.;
		self.p_ij=0.;
		
def countlines(fname):
	counter=0;
	for line in fname:
		counter+=1;
	return counter;
		

def trainexamples(A,Proby,row_size,col_size,alpha,label,data):
	line_num=0;
	data_docid=0;
	data_wordid=0;
	data_count=0;
	data_line=data.readline();
	[data_docid,data_wordid,data_count]=[int(x) for x in data_line.split()];

	#find no. of occurances of each word
	for line in label:
		line_num+=1;
		docid=line_num;
		col_no=int(line)-1;
		(Proby[col_no]).n_ij+=1;			
		while (data_docid==docid):
			row_no=data_wordid-1;
			#print str(row_no)+","+str(col_no);#Debug
			(A[row_no][col_no]).c_ij+=data_count;
			data_line=data.readline();
			if(len(data_line)==0):#end of file
				break;
			[data_docid,data_wordid,data_count]=[int(x) for x in data_line.split()];
		if(len(data_line)==0):
			break;
	
	
	#add alpha to each element
	for i in range(row_size):
		for j in range(col_size):
			(A[i][j]).c_ij+=alpha-1.;
	
	#calculate MAP probabilities
	for j in range(col_size):
		tot_words=0;
		for i in range(row_size):
			tot_words+=(A[i][j]).c_ij;
			
		for i in range(row_size):
			(A[i][j]).p_ij=float((A[i][j]).c_ij)/float(tot_words);


	
	#Calculate MLE probabilities
	tot_examples=0;
	for x in Proby:
		tot_examples+=x.n_ij;
	for x in Proby:
		x.p_ij=float(x.n_ij)/float(tot_examples);		

def print_conf(conf_mat):
	for x in conf_mat:
		print x;
	return;

	
def maxindex(P_yx):
	maxp=0;
	for i in range(len(P_yx)):
		if(P_yx[i]>P_yx[maxp]):
			maxp=i;
	return maxp;
		
def testexamples(conf_mat,A,Proby,testfiles,testlabel):
	line_num=0;
	data_docid=0;
	data_wordid=0;
	data_count=0;
	data_line=testfiles.readline();
	[data_docid,data_wordid,data_count]=[int(x) for x in data_line.split()];
	col_size=len(Proby);

	P_yx=[math.log(x.p_ij) for x in Proby];
	tot_examples=0;
	right_examples=0;
	
	for line in testlabel:
		P_yx=[math.log(x1.p_ij) for x1 in Proby];
		line_num+=1;
		test_no=line_num;
		actual_label=int(line);
		while (test_no==data_docid):
			for i1 in range(col_size):
				P_yx[i1]+=data_count*math.log((A[data_wordid-1][i1]).p_ij);
			data_line=testfiles.readline();
			if(len(data_line)==0):
				break;
			[data_docid,data_wordid,data_count]=[int(x) for x in data_line.split()];
		predicted_label=maxindex(P_yx)+1;
		
		#Right or wrong
		tot_examples+=1;
		if(predicted_label==actual_label):
			right_examples+=1;
		else:
			conf_mat[predicted_label-1][actual_label-1]+=1;
		if(len(data_line)==0):
			break;

	accurate_perc=(float(right_examples)/float(tot_examples))*100.;
	return 	accurate_perc;
			

def entropy_Y(Proby):
    Hs=0;
    for px in Proby:
        Hs-=px*math.log(px);
    return Hs;

class indexpair:
    def __init__(self,a,b):
        self.val=a;
        self.index=b;
    def __lt__(self,other):
        return self.val<other.val;

def smallest_100(H_Y_X,smallest_index):
    h=[];
    N=len(H_Y_X);
    for i in range(N):
        A=indexpair(H_Y_X[i],i);
        heapq.heappush(h,A);
    
    for num in range(100):
        B=heapq.heappop(h);
        smallest_index.append(B.index);
    return;
    
    
								
def entropy_Y_X(Proby,A):
    col_size=len(Proby); #this is k=20, the no. of newsgroups
    row_size=len(A);# this is the no. of words in vocab,|V|=10^5
    
    P_Xj=[0 for i in range(row_size)]; #This is: P(Xj=1)
    
    for i in range(row_size):# This is: P(Xj=1)=P(Xj=1|Y=yk)*P(Y=yk)
        for j in range(col_size):
            P_Xj[i]=P_Xj[i]+A[i][j].p_ij*Proby[j].p_ij;
            
    #Calculate P(Y=yk|Xj=1) inside the calculation for H, so as not to store all values
    
    H_Y_Xj_1=[0 for i in range(row_size)];
    H_Y_Xj_0=[0 for i in range(row_size)];

    for i in range(row_size):
        for j in range(col_size):
            P_Y_X=(A[i][j].p_ij)*Proby[j].p_ij/P_Xj[i];#P(Y=Yk|Xj=1)=P(Xj=1|Y=yk)*P(Y=yk)/P(Xj=1)
            H_Y_Xj_1[i]=H_Y_Xj_1[i]-P_Y_X*math.log(P_Y_X);# sum(k) P(Y=yk|Xj=1)log P(Y=yk|Xj=1) 

    for i in range(row_size):
        for j in range(col_size):
            P_Y_X_0=(1-A[i][j].p_ij)*Proby[j].p_ij/(1-P_Xj[i]);
            H_Y_Xj_0[i]=H_Y_Xj_0[i]-P_Y_X_0*math.log(P_Y_X_0);


    H_Y_X=[0 for i in range(row_size)];
    for i in range(row_size):
        H_Y_X[i]=P_Xj[i]*H_Y_Xj_1[i]+(1-P_Xj[i])*H_Y_Xj_0[i];
    
    smallest_index=[];
    smallest_100(H_Y_X,smallest_index);
    
    return smallest_index;

def write_100words(filename,vocab_list,smallest_index):
    file1=open(filename,'w');
    for index in smallest_index:
        str1=vocab_list[index];
        str2=str1.replace('\n',"")
        file1.write("%s\t"%str2);
    file1.close();
    return;        

    
    
        				
			

def main():
	#find column size
	newsgrp=open("data/newsgrouplabels.txt",'r');	
	col_size=countlines(newsgrp);
	newsgrp.close();
	#find row size
	vocab=open("data/vocabulary.txt",'r');
	row_size=countlines(vocab);
	vocab.close();
	#set alpha value
	alpha=1.+(1./float(row_size));


	Proby=[MLE_prob() for x in range(col_size)];#list to hold P(y)
	
	A=[[MAP_prob() for j in range(col_size)]for i in range(row_size)];#Declare the matrix
	label=open("data/train.label",'r');
	data=open("data/train.data",'r');
	
	#train
	trainexamples(A,Proby,row_size,col_size,alpha,label,data);
	print "Trained......"
	#printA(A);
	#cleanup
	label.close();
	data.close();

	#test
	testfile=open("data/test.data",'r');
	testlabel=open("data/test.label",'r');

	conf_mat=[[0. for j in range(col_size)] for i in range(col_size)];
	accurate_perc=testexamples(conf_mat,A,Proby,testfile,testlabel);
	print str(accurate_perc)+"%"

	#print_conf(conf_mat);
	smallest_index=entropy_Y_X(Proby,A);
	
	vocablist=[];
	vocab=open("data/vocabulary.txt",'r');
	for line in vocab:
	    vocablist.append(line);
	    
	print(len(vocablist));
	
	for index in smallest_index:
	    print vocablist[index];
	#cleanup
	
	write_100words("100words.txt",vocablist,smallest_index);
	testfile.close();
	testlabel.close();
	vocab.close();
		

if __name__ == "__main__":
    main()
