//main Startup function

//taking the 0x0 place of data segment to ensure that .data won't be empty.
char _stump[] = "TJ_421";

extern int main();

int _main(void){
	int mainret;

	mainret = main();

	return mainret;
}