#include "calc_c.h"

#include <cmath>

// calculate skalar product between two vectors
double calc_skalar(double * v1, double * v2){
    double skalar = 0.0;
    for(int i = 0; i < 3; i++){
        skalar += v1[i] * v2[i];
    }
    return skalar;
}

// calculate norm of a vector
double calc_norm(double * v1){
    double sum = 0.0;
    for(int i = 0; i < 3; i++){
        sum += v1[i] * v1[i];
    }
    return sqrt(sum);
}

// calculate vector from pos1 to pos2
double* calc_dist_vec(double * pos1, double * pos2){
    double* v = new double[3];
    for(int i = 0; i < 3; i++){
        v[i] = pos2[i] - pos1[i];
    }
    return v;
}


//calculate angle between three points
double calc_angle(double * pos1, double * pos2, double * pos3){
    double * v1 = calc_dist_vec(pos2, pos1);
    double * v2 = calc_dist_vec(pos2, pos3);
    double angle = calc_skalar(v1, v2) / (calc_norm(v1) * calc_norm(v2));
    angle = acos(angle);
    angle = angle / M_PI * 180.0;
    return angle;
}
