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


/* GET DISTANCES FOR RADIAL DISTRIBUTION FUNCTION CALCULATION */
py::array_t<double> radial(py::array_t<double> array1, py::array_t<double> array2, double cut, py::array_t<double> cell){
    py::buffer_info buf1 = array1.request(), buf2 = array2.request(), buf3 = cell.request();
    // check if given numpy arrays have dimension 1 (are flat)
    if(buf1.ndim != 1 || buf2.ndim != 1 || buf3.ndim != 1)
        throw runtime_error("Number of dimensions must be 1.");
    // obtain pointer on arrays
    const double * ptr1 = (const double *)buf1.ptr;
    const double * ptr2 = (const double *)buf2.ptr;
    const double * ptr3 = (const double *)buf3.ptr;
    // obtain distances in array
    vector<double> * distances = radial_calculate(ptr1, buf1.size / 3, ptr2, buf2.size/3, cut, ptr3);
    // cast to be compatible with Python
    py::array_t<double> dist = py::cast(distances);
    // clean memory
    distances->clear();
    return dist;
}


// calculate distances
vector<double> * radial_calculate(const double * array1, int len1, const double * array2, int len2,
        double cut, const double * cell){
    vector<double> * distances = new vector<double>;
    // apply periodic boundary conditions to obtain 3x3 unit cell
    double * pbc2 = pbc_apply3x3(array2, len2, cell);
    double center[3], neighbor[3], dist;
    // loop through center atoms
    for(int i = 0; i < len1; i++){
        center[0] = array1[3 * i];
        center[1] = array1[3 * i + 1];
        center[2] = array1[3 * i + 2];
        // for each center atoms loop through possible neighbor atoms
        for(int j = 0; j < 27 * len2; j++){
            neighbor[0] = pbc2[3 * j];
            neighbor[1] = pbc2[3 * j + 1];
            neighbor[2] = pbc2[3 * j + 2];
            // calculate distance
            double * v = calc_dist_vec(center, neighbor);
            dist = calc_norm(v);
            delete [] v;
            // check if distance is within cutoff and avoid self-interaction
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

        .. _pybind11: https://pybind11.readthedocs.io/en/stable/

        C++ code which is connected to the program using pybind11_.

        Speed up calculation of the radial distribution function which requires fast loop execution.

        .. _Sphinx: https://www.sphinx-doc.org/en/master/

        Note:
            Documentation especially for internal C++ routines might be incomplete or show wrong argument types.

            This is because Sphinx_ constructs the documentation from the installed Python module.

        Dependencies:
            :py:mod:`numpy`
            :py:mod:`pybind11`
            :mod:`calc_c.cpp`
            :mod:`pbc_c.cpp`

        .. autosummary::

            calc_dist_vec_c
            calc_norm_c
            pbc_apply3x3_c
            radial
            radial_calculate
    )pbdoc"; // optional module docstring

    m.def("radial", &radial, py::return_value_policy::move, R"pbdoc(
            Calculate distances from center atoms to possible neighbor atoms which are smaller than a cutoff distance.

            Mostly handles connection to Python code. Actual calculation is performed in :func:`.radial_c.radial_calculate`.

            Args:
                array1 (ndarray[float]): atomic positions for central atoms
                array2 (ndarray[float]): atomic positions for neighbor atoms
                cut (float): cutoff for distance search
                cell (ndarray[float]): unit cell of the system for periodic boundary conditions

            Returns:
                ndarray[float]: distances obtained for the calculation of the RDF
        )pbdoc", py::arg("array1"), py::arg("array2"), py::arg("cut"), py::arg("cell")
    );

    m.def("radial_calculate", &radial_calculate, R"pbdoc(
            Actual calculation of distances.

            Args:
                array1 (double *): pointer on array with atomic positions for central atoms
                len1 (int): number of atoms in array1
                array2 (double *): pointer on array with atomic positions for neighbor atoms
                len2 (int): number of atoms in array2
                cut (double): cutoff for distance search
                cell (double *): pointer on array with unit cell of the system for periodic boundary conditions

            Returns:
                vector<double> *: pointer on double vector with distances obtained for the calculation of the RDF

            Note:
                C++ only
        )pbdoc", py::arg("array1"), py::arg("len1"), py::arg("array2"), py::arg("len2"), py::arg("cut"), py::arg("cell")
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


#ifdef VERSION_INFO
m.attr("__version__") = VERSION_INFO;
#else
m.attr("__version__") = "dev";
#endif
}
