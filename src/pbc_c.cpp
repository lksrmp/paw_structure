#include "pbc_c.h"

double * pbc_apply3x3(const double * pos, int len, double a){
    double * pbc = new double[27 * len * 3];
    int index = 0;
    for(int i = -1; i < 2; i++){
        for(int j = -1; j < 2; j++){
            for(int k = -1; k < 2; k++){
                for(int l = 0; l < len; l++){
                    pbc[3 * (len * index + l) + 0] = pos[3 * l + 0] + a * i;
                    pbc[3 * (len * index + l) + 1] = pos[3 * l + 1] + a * j;
                    pbc[3 * (len * index + l) + 2] = pos[3 * l + 2] + a * k;
                }
                index++;
            }
        }
    }
    return pbc;
}
