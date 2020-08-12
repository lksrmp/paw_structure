#include <iostream>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>

#include "calc_c.h"
#include "pbc_c.h"


using namespace std;
namespace py = pybind11;

py::array_t<double> radial(py::array_t<double> array1, py::array_t<double> array2, double cut, py::array_t<double> cell);
vector<double> * radial_calculate(const double * array1, int len1, const double * array2, int len2, double cut, const double * cell);



py::array_t<double> radial(py::array_t<double> array1, py::array_t<double> array2, double cut, py::array_t<double> cell){
    py::buffer_info buf1 = array1.request(), buf2 = array2.request(), buf3 = cell.request();
    if(buf1.ndim != 1 || buf2.ndim != 1 || buf3.ndim != 1)
        throw runtime_error("Number of dimensions must be 1.");
    const double * ptr1 = (const double *)buf1.ptr;
    const double * ptr2 = (const double *)buf2.ptr;
    const double * ptr3 = (const double *)buf3.ptr;
    vector<double> * distances = radial_calculate(ptr1, buf1.size / 3, ptr2, buf2.size/3, cut, ptr3);
    py::array_t<double> dist = py::cast(distances);
    distances->clear();
    return dist;

}

vector<double> * radial_calculate(const double * array1, int len1, const double * array2, int len2,
        double cut, const double * cell){
    vector<double> * distances = new vector<double>;
    double * pbc2 = pbc_apply3x3(array2, len2, cell);
    double center[3], neighbor[3], dist;
    for(int i = 0; i < len1; i++){
        center[0] = array1[3 * i];
        center[1] = array1[3 * i + 1];
        center[2] = array1[3 * i + 2];
        for(int j = 0; j < 27 * len2; j++){
            neighbor[0] = pbc2[3 * j];
            neighbor[1] = pbc2[3 * j + 1];
            neighbor[2] = pbc2[3 * j + 2];
            double * v = calc_dist_vec(center, neighbor);
            dist = calc_norm(v);
            delete [] v;
            if(dist < cut && dist > 0.01){
                distances->push_back(dist);
            }
        }
    }
    return distances;
}


PYBIND11_MODULE(radial_c, m){
    m.doc() = R"pbdoc(
        paw_structure.radial_c
        ----------------------

        .. currentmodule:: paw_structure.radial_c

        Dependencies:
        :py:mod:`numpy`
        :mod:`.pbc`

        .. autosummary::

            radial
            radial_calculate
    )pbdoc"; // optional module docstring

    m.def("radial", &radial, py::return_value_policy::move, R"pbdoc(
        Calculate scalar.

        Args:
            v1 (double *): pointer on 3-dim. vector
            v2 (double *): pointer on 3-dim. vector

        Returns:
            double
    )pbdoc");

    m.def("radial_calculate", &radial_calculate);


#ifdef VERSION_INFO
m.attr("__version__") = VERSION_INFO;
#else
m.attr("__version__") = "dev";
#endif
}
