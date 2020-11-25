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
        double cut1, double cut2, double angle, const double * cell);
int hbonds(py::array_t<const double>& array1, py::array_t<const double>& array2,
        double cut1, double cut2, double angle, py::array_t<const double>& cell);



int hbonds_number(const double* array1, int len1, const double* array2, int len2,
        double cut1, double cut2, double angle, const double * cell){
    // follows Luzar, Chandler: J. Chem. Phys. 98, 8160 (1993), A. Luzar and D. Chandler, Nature London 379, 55 (1996)
    //         Dawson, Gygi: J. Chem. Phys. 148, 124501 (2018)
    // Review: Kumar et al.: J. Chem. Phys. 126, 204107 (2007)
    int counter = 0;
    double center[3], neighbor1[3], neighbor2[3];

    double * pbc1 = pbc_apply3x3(array1, len1, cell);
    double * pbc2 = pbc_apply3x3(array2, len2, cell);
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
                            if(dist12 < dist21){
                                angle121 = calc_angle(neighbor2, center, neighbor1);
                            } else {
                                angle121 = calc_angle(neighbor2, neighbor1, center);
                            }
                            //angle121 = calc_angle(center, neighbor2, neighbor1);
                            //cout << angle121 << "\n";
                            //cout << center[0] << " " << center[1] << " " << center[2] << " "  << neighbor2[0] << " " << neighbor2[1] << " " << neighbor2[2] << " "  << neighbor1[0] << " " << neighbor1[1] << " " << neighbor1[2] << "\n";
                            if(angle121 < angle){
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
        double cut1, double cut2, double angle, py::array_t<const double>& cell){
    py::buffer_info buf1 = array1.request();
    py::buffer_info buf2 = array2.request();
    py::buffer_info buf3 = cell.request();
    if (buf1.ndim != 1 || buf2.ndim != 1 || buf3.ndim != 1)
    {
        throw std::runtime_error("numpy.ndarray dims must be 1!");
    }
    int number = 0;
    const double* ptr1 = (const double*)buf1.ptr;
    const double* ptr2 = (const double*)buf2.ptr;
    const double * ptr3 = (const double *)buf3.ptr;
    //for(int i = 0; i < buf1.size / 3; i++){
    //    cout << ptr1[3 * i] << " " << ptr1[3 * i + 1] << " " << ptr1[3 * i + 2] << "\n";
    //}
    number = hbonds_number(ptr1, buf1.size / 3, ptr2, buf2.size / 3, cut1, cut2, angle, ptr3);
    return number;
}

PYBIND11_MODULE(hbonds_c, m){
    m.doc() = R"pbdoc(
        paw_structure.hbonds_c
        ----------------------

        .. currentmodule:: paw_structure.hbonds_c

        .. _pybind11: https://pybind11.readthedocs.io/en/stable/

        C++ code which is connected to the program using pybind11_.

        Speed up calculation of the hydrogen bond number which requires fast loop execution.

        .. _Sphinx: https://www.sphinx-doc.org/en/master/

        XXX REFERENCE TO ALGORITHM EXPLAINATION XXX

        Note:
            Documentation especially for internal C++ routines might be incomplete or show wrong argument types.

            This is because Sphinx_ constructs the documentation from the installed Python module.


        Dependencies:
            :py:mod:`numpy`
            :py:mod:`pybind11`
            :mod:`calc_c.cpp`
            :mod:`pbc_c.cpp`

        .. autosummary::

            calc_angle_c
            calc_dist_vec_c
            calc_norm_c
            hbonds
            hbonds_number
            pbc_apply3x3_c
    )pbdoc"; // optional module docstring

    m.def("hbonds_number", &hbonds_number, R"pbdoc(
            Count hydrogen bonds.

            Args:
                array1 (double *): contains atomic positions of oxygen atoms
                len1 (int): length of first array
                array2 (double *): contains atomic positions of hydrogen atoms
                len2 (int): length of second array
                cut1 (double): maximum oxygen - oxygen distance
                cut2 (double): maximum oxygen - hydrogen distance
                angle (float): minimum angle criterion
                cell (array): unit cell of the system for periodic boundary conditions

            Returns:
                int: number of hydrogen bonds found
        )pbdoc", py::arg("array1"), py::arg("len1"), py::arg("array2"), py::arg("len2"),
        py::arg("cut1"), py::arg("cut2"), py::arg("angle"), py::arg("cell")
    );

    m.def("hbonds", &hbonds, R"pbdoc(
            Count hydrogen bonds.

            Mostly handles connection to Python code. Actual calculation performed in :func:`.hbonds_x.hbonds_number`

            Args:
                array1 (ndarray[float]): contains atomic positions of oxygen atoms
                array2 (ndarray[float]): contains atomic positions of hydrogen atoms
                cut1 (float): maximum oxygen - oxygen distance
                cut2 (float): maximum oxygen - hydrogen distance
                angle (float): minimum angle criterion
                cell (ndarray[float]): unit cell of the system for periodic boundary conditions

            Returns:
                int: number of hydrogen bonds found
        )pbdoc", py::arg("array1"), py::arg("array2"), py::arg("cut1"), py::arg("cut2"), py::arg("angle"), py::arg("cell")
    );

    m.def("pbc_apply3x3_c", &pbc_apply3x3, R"pbdoc(
            Apply periodic boundary conditions to obtain 3x3 unit cell.

            Args:
                pos (double *): pointer on array with atomic positions
                len (int): number of atoms in pos
                cell (double *): pointer on array with unit cell of the system

            Returns:
                double *: pointer on array with atomic position of 3x3 unit cell

            Note:
                C++ only.

                Source code in file :mod:`pbc_c.cpp`.
        )pbdoc", py::arg("pos"), py::arg("len"), py::arg("cell")
    );

    m.def("calc_dist_vec_c", &calc_dist_vec, R"pbdoc(
            Calculate difference between two vectors.

            Args:
                pos1 (double *): pointer on array with position of atom 1
                pos2 (double *): pointer on array with position of atom 2

            Returns:
                double *: pointer on array with vector between both positions

            Note:
                C++ only.

                Source code in file :mod:`calc_c.cpp`.
        )pbdoc", py::arg("pos1"), py::arg("pos2")
    );

    m.def("calc_norm_c", &calc_norm, R"pbdoc(
            Calculate norm of a vector.

            Args:
                vec (double *): pointer on array with 3 entries

            Returns:
                float: euclidean norm of the vector

            Note:
                C++ only.

                Source code in file :mod:`calc_c.cpp`.
        )pbdoc", py::arg("vec")
    );

    m.def("calc_angle_c", &calc_angle, R"pbdoc(
            Calculate angle between three given points.

            Args:
                pos1 (double *): pointer on array with 3 entries
                pos2 (double *): pointer on array with 3 entries
                pos3 (double *): pointer on array with 3 entries

            Returns:
                float: angle between points pos1-pos2-pos3

            Note:
                C++ only.

                Source code in file :mod:`calc_c.cpp`.
        )pbdoc", py::arg("pos1"), py::arg("pos2"), py::arg("pos3")
    );

#ifdef VERSION_INFO
m.attr("__version__") = VERSION_INFO;
#else
m.attr("__version__") = "dev";
#endif
}



