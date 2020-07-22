#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <iostream>
#include <vector>

#include "pbc_c.h"
#include "calc_c.h"

using namespace std;
namespace py = pybind11;


// void pbc_apply3x3(const double * pos, int len, double * pbc, double a);
int hbonds_number(const double* array1, int len1, const double* array2, int len2,
        double cut1, double cut2, double angle, double a);
int hbonds(py::array_t<const double>& array1, py::array_t<const double>& array2,
        double cut1, double cut2, double angle, double a);



int hbonds_number(const double* array1, int len1, const double* array2, int len2,
        double cut1, double cut2, double angle, double a){

    int counter = 0;
    double center[3], neighbor1[3], neighbor2[3];

    double * pbc1 = pbc_apply3x3(array1, len1, a);
    double * pbc2 = pbc_apply3x3(array2, len2, a);
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

            double * v11 = calc_dist_vec(center, neighbor1);
            dist11 = calc_norm(v11);
            delete [] v11;

            if(dist11 < cut1 && dist11 > 0.01) {
                for(int k = 0; k < 27 * len2; k++){
                    neighbor2[0] = pbc2[3 * k];
                    neighbor2[1] = pbc2[3 * k + 1];
                    neighbor2[2] = pbc2[3 * k + 2];

                    double * v12 = calc_dist_vec(center, neighbor2);
                    dist12 = calc_norm(v12);
                    delete [] v12;
                    if(dist12 < cut2){
                        double * v21 = calc_dist_vec(neighbor2, neighbor1);
                        dist21 = calc_norm(v21);
                        delete [] v21;
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
    delete [] pbc1;
    delete [] pbc2;
    return counter;
}

int hbonds(py::array_t<const double>& array1, py::array_t<const double>& array2,
        double cut1, double cut2, double angle, double a){
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
    m.doc() = R"pbdoc(
        paw_structure.hbonds_c
        ----------------------

        .. currentmodule:: paw_structure.hbonds_c

        .. autosummary::

            hbonds_number
            hbonds
    )pbdoc"; // optional module docstring

    m.def("hbonds_number", &hbonds_number, R"pbdoc(
            Count hydrogen bonds.

            Args:
                array1 (array): contains atomic positions of oxygen atoms
                len1 (int): length of first array
                array2 (array): contains atomic positions of hydrogen atoms
                len2 (int): length of second array
                cut1 (float): maximum oxygen - oxygen distance
                cut2 (float): maximum oxygen - hydrogen distance
                angle (float): minimum angle criterion
                a (float): unit cell length
        )pbdoc", py::arg("array1"), py::arg("len1"), py::arg("array2"), py::arg("len2"),
        py::arg("cut1"), py::arg("cut2"), py::arg("angle"), py::arg("a")
    );

      //, "A function which adds two numbers", py::arg("array1"), py::arg("len1"), py::arg("array2"),
    //  py::arg("len2"), py::arg("cut"), py::arg("angle"));

    /*
    m.def("calc_dist_vec", &calc_dist_vec);
    m.def("calc_skalar", &calc_skalar, R"pbdoc(
        Calculate scalar.

        Args:
            v1 (double *): pointer on 3-dim. vector
            v2 (double *): pointer on 3-dim. vector

        Returns:
            double
    )pbdoc", py::arg("v1"), py::arg("v2"));
    m.def("calc_norm", &calc_norm);
    m.def("calc_angle", &calc_angle);
    m.def("pbc_apply3x3", &pbc_apply3x3);
     */
    m.def("hbonds", &hbonds);

#ifdef VERSION_INFO
m.attr("__version__") = VERSION_INFO;
#else
m.attr("__version__") = "dev";
#endif
}



