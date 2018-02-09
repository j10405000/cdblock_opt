#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cmath>
#include <vector>

using namespace std;

void exit_with_help(){
	printf(
	"Usage: ./scale scale-data [src-filename] [dest-filename]\n"
	);
	exit(1);
}

class ScaleCoeff{
	public:
		vector<double> mean, std;
		ScaleCoeff() {
			max_line_len = 1024;
			line = (char*)malloc(sizeof(char) * max_line_len);
		}
		~ScaleCoeff() {free(line);}
		void scale(const char *src, const char *dest);
		void from(const char *src);
		void load(const char *src);
		void dump(const char *dest);
	private:
		vector<int> idx;
		vector<double> val;
		int y, max_line_len;

		char *line;
		char *readline(FILE *input);
		void tofeatvec();
};

char* ScaleCoeff::readline(FILE *input){
	int len;
	if(fgets(line,max_line_len,input) == NULL)
		return NULL;
	while(strrchr(line,'\n') == NULL) {
		max_line_len *= 2;
		line = (char *) realloc(line,max_line_len);
		len = (int) strlen(line);
		if(fgets(line+len,max_line_len-len,input) == NULL)
			break;
	}
	return line;
}

void ScaleCoeff::tofeatvec(){
	char *label, *idx_, *val_, *endptr;
	idx.clear(); val.clear();
	label = strtok(line," \t");
	y = (int) strtol(label,&endptr,10);
	while(1) {
		idx_ = strtok(NULL,":");
		val_ = strtok(NULL," \t");
		if(val_ == NULL) break;
		idx.push_back((int) strtol(idx_,&endptr,10));
		val.push_back(strtod(val_,&endptr));
	}
}


// 1. Normalize to zero-meand and unit-variance, 2. instance-wise scale
void ScaleCoeff::scale(const char *src, const char *dest) { 
	FILE *fin = fopen(src,"r");
	FILE *fout = fopen(dest,"w");
	int l = 0;
	while((readline(fin))!=NULL){
		double len = 0;
		l += 1;
		tofeatvec();
		for(size_t i = 0; i < idx.size(); i++) {
			val[i] = (val[i] - mean[idx[i]])/std[idx[i]];
			len += val[i]*val[i];
		}
		len = sqrt(len);
		fprintf(fout, "%d",y);
		for(size_t i = 0; i < idx.size(); i++)
			fprintf(fout," %d:%.6g", idx[i], val[i]/len);
		fprintf(fout,"\n");
	}
	fclose(fout);
	fclose(fin);
}

// generate scale coefficient from src
void ScaleCoeff::from(const char *src){
	mean.clear(); std.clear();
	FILE *fin = fopen(src,"r");
	int y, l = 0, maxidx = 0;
	while((readline(fin))!=NULL){
		l += 1;
		double len = 0;
		tofeatvec();
		maxidx = idx.back();
		if(mean.size() < maxidx+1) {
			mean.resize(maxidx+1, 0);
			std.resize(maxidx+1, 0);
		}
		for(size_t i = 0; i < idx.size(); i++) {
			mean[idx[i]] += val[i];
			std[idx[i]] += val[i]*val[i];
		}
		if(l % 10000 == 0) {
			putchar('.');
			fflush(stdout);
		}
	}
	for(int i = 0; i <= maxidx; i++) {
		mean[i] /= l;
		std[i] = sqrt(std[i]/l - mean[i]*mean[i]);
	}
	fclose(fin);
}

void ScaleCoeff::dump(const char *src) {
	FILE *fout = fopen(src,"w");
	fprintf(fout,"%ld\n",mean.size());
	for(size_t i = 0; i < mean.size(); i++) {
		fprintf(fout, "%.17g %.17g\n", mean[i], std[i]);
	}
	fclose(fout);
}

void ScaleCoeff::load(const char *src) {
	FILE *fin = fopen(src,"r");
	size_t size = 0;
	fscanf(fin,"%ld", &size);
	mean.resize(size, 0);
	std.resize(size, 0);
	for(size_t i = 0; i < mean.size(); i++)
		fscanf(fin, "%lf %lf", &mean[i], &std[i]);
	fclose(fin);
}

int main(int argc, char* argv[]){
	if((argc != 4) and (argc != 2)) {
		exit_with_help();
	}
	char SCfrom[1024], *src = NULL, *dest = NULL;
	sprintf(SCfrom, "%s.sc", argv[1]);
	src = argv[2];
	if(argc == 4)
		dest = argv[3];

	ScaleCoeff SC;
	FILE *fp = fopen(SCfrom,"r");
	if(fp !=NULL) {
		SC.load(SCfrom);
		fclose(fp);
	} else  {
		SC.from(argv[1]);
		SC.dump(SCfrom);
	}
	if(src and dest)
		SC.scale(src, dest);
	return 0;
}

