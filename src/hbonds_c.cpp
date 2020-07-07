#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <iostream>
#include <cmath>
#include <vector>

using namespace std;
namespace py = pybind11;


// calculate vector from pos1 to pos2
void calc_dist_vec(double * pos1, double * pos2, double * v){
    for(int i = 0; i < 3; i++){
        v[i] = pos2[i] - pos1[i];
    }
    return;
}

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

//calculate angle between three points
double calc_angle(double * pos1, double * pos2, double * pos3){
    double v1[3], v2[3];
    calc_dist_vec(pos2, pos1, v1);
    calc_dist_vec(pos2, pos3, v2);
    double angle = calc_skalar(v1, v2) / (calc_norm(v1) * calc_norm(v2));
    angle = acos(angle);
    angle = angle / M_PI * 180.0;
    return angle;
}

void pbc_3x3(const double * pos, int len, double * pbc, double a){
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
    return;
}


int hbonds_number(const double* array1, int len1, const double* array2, int len2, double cut1, double cut2, double angle, double a){
    int counter = 0;
    double center[3], neighbor1[3], neighbor2[3], v11[3], v12[3], v21[3];

    double pbc1[27 * len1 * 3];
    double pbc2[27 * len2 * 3];
    pbc_3x3(array1, len1, pbc1, a);
    pbc_3x3(array2, len2, pbc2, a);
    double dist11, dist12, dist21, angle121;
    int center_count = 0;

    for(int i = 0; i < len1; i++){
        center[0] = array1[3 * i];
        center[1] = array1[3 * i + 1];
        center[2] = array1[3 * i + 2];

        for(int j = 0; j < 27 * len1; j++){
            neighbor1[0] = pbc1[3 * j];
            neighbor1[1] = pbc1[3 * j + 1];
            neighbor1[2] = pbc1[3 * j + 2];

            calc_dist_vec(center, neighbor1, v11);
            dist11 = calc_norm(v11);

            if(dist11 < cut1 && dist11 > 0.01) {
                for(int k = 0; k < 27 * len2; k++){
                    neighbor2[0] = pbc2[3 * k];
                    neighbor2[1] = pbc2[3 * k + 1];
                    neighbor2[2] = pbc2[3 * k + 2];

                    calc_dist_vec(center, neighbor2, v12);
                    dist12 = calc_norm(v12);

                    if(dist12 < cut2){
                        calc_dist_vec(neighbor2, neighbor1, v21);
                        dist21 = calc_norm(v21);

                        if(dist21 < cut2){
                            angle121 = calc_angle(center, neighbor2, neighbor1);
                            //cout << angle121 << "\n";
                            //cout << center[0] << " " << center[1] << " " << center[2] << " "  << neighbor2[0] << " " << neighbor2[1] << " " << neighbor2[2] << " "  << neighbor1[0] << " " << neighbor1[1] << " " << neighbor1[2] << "\n";
                            if(angle121 > angle){
                                counter++;
                            }
                        }
                    }
                }
            }
        }
        center_count++;
    }
    return counter;
}

int hbonds(py::array_t<const double>& array1, py::array_t<const double>& array2, double cut1, double cut2, double angle, double a){
    py::buffer_info buf1 = array1.request();
    py::buffer_info buf2 = array2.request();
    if (buf1.ndim != 1 || buf2.ndim != 1)
    {
        throw std::runtime_error("numpy.ndarray dims must be 1!");
    }
    int number = 0;
    const double* ptr1 = (const double*)buf1.ptr;
    const double* ptr2 = (const double*)buf2.ptr;
    //for(int i = 0; i < buf1.size / 3; i++){
    //    cout << ptr1[3 * i] << " " << ptr1[3 * i + 1] << " " << ptr1[3 * i + 2] << "\n";
    //}
    number = hbonds_number(ptr1, buf1.size / 3, ptr2, buf2.size / 3, cut1, cut2, angle, a);
    return number;
}

PYBIND11_MODULE(hbonds_c, m){
m.doc() = "Hydrogen bond number calculation"; // optional module docstring
m.def("hbonds_number", &hbonds_number);  //, "A function which adds two numbers", py::arg("array1"), py::arg("len1"), py::arg("array2"),
//  py::arg("len2"), py::arg("cut"), py::arg("angle"));
m.def("calc_dist_vec", &calc_dist_vec);
m.def("calc_skalar", &calc_skalar);
m.def("calc_norm", &calc_norm);
m.def("calc_angle", &calc_angle);
// m.def("calc_dist", &calc_dist);
m.def("hbonds", &hbonds);
}



