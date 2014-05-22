from __future__ import division

def main():
	P_X1=0.2;
	P_Y1=0.8;
	P_X0=1.-P_X1;
	P_Y0=1.-P_Y1;
	

	P_Z1gX1Y1=0.95;
	P_Z1gX0Y1=0.8;
	P_Z1gX1Y0=0.8;
	P_Z1gX0Y0=0.1;


	P_Z1uY1=P_Z1gX1Y1*P_X1*P_Y1+P_Z1gX0Y1*P_X0*P_Y1;

	P_Z1uY0=P_Z1gX1Y0*P_Y0*P_X1+P_Z1gX0Y0*P_Y0*P_X0;

	P_Z1uX1=P_Z1gX1Y1*P_X1*P_Y1 + P_Z1gX1Y0*P_X1*P_Y0;

	P_Z1=P_Z1uY1+P_Z1uY0;

	print "P_Z1= "+str(P_Z1);

	P_Z1gX1=P_Z1uX1/P_Z1;

	P_X1gZ1=P_Z1uX1/P_Z1;

	print "P_X1gZ1= "+str(P_X1gZ1);

	P_X1uY1uZ1=P_X1*P_Y1*P_Z1gX1Y1;

	P_X1gY1Z1=P_X1uY1uZ1/P_Z1uY1;

	print "P_X1gY1Z1= "+str(P_X1gY1Z1); 

if __name__ == "__main__":
	main()
