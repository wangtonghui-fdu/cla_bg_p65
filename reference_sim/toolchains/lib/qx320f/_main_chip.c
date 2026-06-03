#include "timer.h"

extern int main();

int _main(void){
	int mainret;

	u32 start, end, total;
	init_timer();
	start = get_timestamp();
	mainret = main();
	end = get_timestamp();
	total = start - end;

	return mainret;
}