from __future__ import division
import math


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

def print_conf_to_file(conf_mat, fname):
        conf_file=open(fname,'w');
        for x in conf_mat:
            for item in x:
                conf_file.write("%d,"%item);
            conf_file.write("\n");
        conf_file.close();
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
	#print_conf_to_file(conf_mat,"conffile.txt");
	
	mis_categor=[];
	for j in range(col_size):
	    missed=0;
	    for i in range(col_size):
	        missed=missed+conf_mat[i][j];
	    mis_categor.append(missed);
	
	print mis_categor; 
	
	#cleanup
	testfile.close();
	testlabel.close();
	
		

if __name__ == "__main__":
    main()
