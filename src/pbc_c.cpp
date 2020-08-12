#include "pbc_c.h"

double * pbc_apply3x3(const double * pos, int len, const double * cell){
    double * pbc = new double[27 * len * 3];
    int index = 0;
    for(int i = -1; i < 2; i++){
        for(int j = -1; j < 2; j++){
            for(int k = -1; k < 2; k++){
                for(int l = 0; l < len; l++){
                    pbc[3 * (len * index + l) + 0] = pos[3 * l + 0] + i * cell[0] + j * cell[3] + k * cell[6];
                    pbc[3 * (len * index + l) + 1] = pos[3 * l + 1] + i * cell[1] + j * cell[4] + k * cell[7];
                    pbc[3 * (len * index + l) + 2] = pos[3 * l + 2] + i * cell[2] + j * cell[5] + k * cell[8];
                }
                index++;
            }
        }
    }
    return pbc;
}
