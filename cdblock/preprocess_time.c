#include <math.h>
#include <time.h>
#include <algorithm>
#include <set>
#include <assert.h>
#include "zlib/zlib.h"
#include "block.h"

#define Malloc(type,n) (type *)malloc((n)*sizeof(type))

int main( int argc, char *argv[] )
{
	
	time_t startload_t;
	double init_load_t=0;
	
	startload_t = time(NULL);
	//sleep(3);
	FILE *fp;
	fp = fopen(argv[1], "r");	
	
    struct problem total_prob;
	
	total_prob.bias = -1;
	
	/*debug
	printf("test: %d\n", strstr(argv[1], "webspam.train"));
	printf("test: %d\n", strstr(argv[1], "epsilon_normalized"));
	printf("test: %d\n", strstr(argv[1], "kddb"));
	*/
	
	//webspam
	if(strstr(argv[1], "webspam.train")!=0)
	{
		total_prob.l = 200000;
		total_prob.n = 16609143;
	}
	
	//epsilon
	else if(strstr(argv[1], "epsilon_normalized")!=0)
	{
		total_prob.l = 400000;
		total_prob.n = 2000;
	}
	
	//kdd
	else if(strstr(argv[1], "kddb")!=0)
	{
		total_prob.l = 19264097;
		total_prob.n = 29890095;
	}
	
	/*debug
	printf("test: %d %d\n", total_prob.l, total_prob.n);
	*/
	
	unsigned long long *offset = Malloc(unsigned long long,total_prob.l+1);

	char *buf = Malloc(char,1000000);
	int i = 0;
	unsigned long long accu = 0;
	while(fgets(buf,1000000,fp) != NULL)
    {
		for(int j=0; j<1000000; j++)
			if(buf[j] == '\n' || buf[j] == '\0')
			{
				offset[i] = accu;
				accu += j+1;
				//if(i%1000000==0)
					//printf("offset[%d]: %llu\n", i, offset[i]);
				break;
			}	
		i++;
	}
	
	
	init_load_t += difftime(time(NULL), startload_t);
	for(int i=0; i<200000; i++)
		printf("offset[%d] = %llu\n",i,offset[i]);

	printf("initial parsing & write time: %f\n",init_load_t);
	
}

