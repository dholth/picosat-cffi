# Python binding copyright (c) 2013 Daniel Holth
#
# PicoSAT copyright (c) 2006 - 2012, Armin Biere, Johannes Kepler University.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

__all__ = ['PicoSAT', 'ffi']

import os.path
import cffi

from picosat import docstrings

# preprocessed picosat.h
picosat_h = """
#define PICOSAT_API_VERSION ...
#define PICOSAT_UNKNOWN ...
#define PICOSAT_SATISFIABLE ...
#define PICOSAT_UNSATISFIABLE ...

typedef struct PicoSAT PicoSAT;

// Not implemented:
// const char *picosat_version (void);
// const char *picosat_config (void);

// For picosat-cffi checks:
int picosat_get_state(PicoSAT *picosat);

const char *picosat_copyright (void);
typedef void * (*picosat_malloc)(void *, size_t);
typedef void * (*picosat_realloc)(void*, void *, size_t, size_t);
typedef void (*picosat_free)(void*, void*, size_t);
PicoSAT * picosat_init (void);

// Probably not very useful from Python:
// PicoSAT * picosat_minit (void * state,
//     picosat_malloc,
//     picosat_realloc,
//     picosat_free);

void picosat_reset (PicoSAT *);
void picosat_set_output (PicoSAT *, FILE *);
void picosat_measure_all_calls (PicoSAT *);
void picosat_set_prefix (PicoSAT *, const char *);
void picosat_set_verbosity (PicoSAT *, int new_verbosity_level);
void picosat_set_plain (PicoSAT *, int new_plain_value);
void picosat_set_global_default_phase (PicoSAT *, int);
void picosat_set_default_phase_lit (PicoSAT *, int lit, int phase);
void picosat_reset_phases (PicoSAT *);
void picosat_reset_scores (PicoSAT *);
void picosat_remove_learned (PicoSAT *, unsigned percentage);
void picosat_set_more_important_lit (PicoSAT *, int lit);
void picosat_set_less_important_lit (PicoSAT *, int lit);
void picosat_message (PicoSAT *, int verbosity_level, const char * fmt, ...);
void picosat_set_seed (PicoSAT *, unsigned random_number_generator_seed);
int picosat_enable_trace_generation (PicoSAT *);
void picosat_set_incremental_rup_file (PicoSAT *, FILE * file, int m, int n);
void picosat_save_original_clauses (PicoSAT *);
int picosat_inc_max_var (PicoSAT *);
int picosat_push (PicoSAT *);
int picosat_failed_context (PicoSAT *, int lit);
int picosat_context (PicoSAT *);
int picosat_pop (PicoSAT *);
void picosat_simplify (PicoSAT *);
void picosat_adjust (PicoSAT *, int max_idx);
int picosat_variables (PicoSAT *);
int picosat_added_original_clauses (PicoSAT *);
size_t picosat_max_bytes_allocated (PicoSAT *);
double picosat_time_stamp (void);
void picosat_stats (PicoSAT *);
unsigned long long picosat_propagations (PicoSAT *);
unsigned long long picosat_decisions (PicoSAT *);
unsigned long long picosat_visits (PicoSAT *);
double picosat_seconds (PicoSAT *);
int picosat_add (PicoSAT *, int lit);
int picosat_add_arg (PicoSAT *, ...);
int picosat_add_lits (PicoSAT *, int * lits);
void picosat_print (PicoSAT *, FILE *);
void picosat_assume (PicoSAT *, int lit);
void picosat_add_ado_lit (PicoSAT *, int);
int picosat_sat (PicoSAT *, int decision_limit);
void picosat_set_propagation_limit (PicoSAT *, unsigned long long limit);
int picosat_res (PicoSAT *);
int picosat_deref (PicoSAT *, int lit);
int picosat_deref_toplevel (PicoSAT *, int lit);
int picosat_deref_partial (PicoSAT *, int lit);
int picosat_inconsistent (PicoSAT *);
int picosat_failed_assumption (PicoSAT *, int lit);
const int * picosat_failed_assumptions (PicoSAT *);
const int * picosat_mus_assumptions (PicoSAT *, void *,
                                     void(*)(void*,const int*),int);
const int * picosat_maximal_satisfiable_subset_of_assumptions (PicoSAT *);
const int *
picosat_next_maximal_satisfiable_subset_of_assumptions (PicoSAT *);
const int *
picosat_next_minimal_correcting_subset_of_assumptions (PicoSAT *);
const int *
picosat_humus (PicoSAT *,
               void (*callback)(void * state, int nmcs, int nhumus),
        void * state);
int picosat_changed (PicoSAT *);
int picosat_coreclause (PicoSAT *, int i);
int picosat_corelit (PicoSAT *, int lit);
void picosat_write_clausal_core (PicoSAT *, FILE * core_file);
void picosat_write_compact_trace (PicoSAT *, FILE * trace_file);
void picosat_write_extended_trace (PicoSAT *, FILE * trace_file);
void picosat_write_rup_trace (PicoSAT *, FILE * trace_file);
int picosat_usedlit (PicoSAT *, int lit);
"""

class StateError(Exception):
    """PicoSAT is in the wrong state for this API call."""

class PicoSAT(object):
    # Return codes for get_state():
    STATE_RESET = 0
    STATE_READY = 1
    STATE_SAT = 2
    STATE_UNSAT = 3
    STATE_UNKNOWN = 4
    
    def __init__(self):
        self._picosat = _picosat.picosat_init()

    def __del__(self):
        _picosat.picosat_reset(self._picosat)

    def pop(self):
        assert self.context() > 0 # or library aborts
        return _picosat.picosat_pop(self._picosat)

    def print_(self, f):
        return _picosat.picosat_print(self._picosat, ffi.cast("FILE*", f))
    
    def add_clause(self, literals):
        """
        Add an entire clause from a Python iterable yielding 
        (non-zero-terminated) integers. add_clause appends the
        terminating 0.
        """
        for lit in literals:
            self.add(lit)
        return self.add(0)
        
    def add_clauses(self, clauses):
        """
        Call add_clause(clause) for clause in clauses. Return result of final 
        add_clause() call or None if clauses was empty.
        """
        rc = None
        for clause in clauses:
            rc = self.add_clause(clause)
        return rc
    
    def get_solution(self):
        """
        If state is PicoSAT.STATE_SAT, return solution as a list()
        """
        if self.get_state() != self.STATE_SAT:
            raise StateError()
        return [self.deref(i)*i for i in range(1, self.variables()+1)]

def _init():
    """Create cffi binding."""
    global _picosat, ffi

    here = os.path.join(os.path.dirname(__file__), '..')
    lib = str(os.path.normpath(os.path.join(here, "picosat-956")))
    source = str(os.path.normpath(os.path.join(lib, "picosat.c")))
    ffi = cffi.FFI()
    ffi.cdef(picosat_h)
    _picosat = ffi.verify(""" 
            #include <picosat.h> 
            // To be able to check before calling certain methods...
            int picosat_get_state(PicoSAT *picosat) {
                typedef enum State { RESET, READY, SAT, UNSAT, UNKNOWN } State;
                return ((State*)picosat)[0];
            }
            """,
            library_dirs=[lib],
            include_dirs=[lib],
            sources=[source])

    picosat_type = ffi.typeof("PicoSAT *")
    # picosat returns zero-terminated lists as int *
    int_p = ffi.typeof("const int *")
    
    def returns_ztl(f):
        def ztl_to_list(*args):
            """
            Return Python list from a zero-terminated list.
            """
            result = []
            ztl = f(*args)
            i = 0
            while ztl[i] != 0:
                i += 1
                result.append(ztl[i])
            return result
        return ztl_to_list

    def genfn(f, f_type, name, docstring=None):
        if f_type.result == int_p:
            f = returns_ztl(f)
        def pico(self, *args):
            return f(self._picosat, *args)
        pico.func_name = name
        pico.__doc__ = docstring
        return pico
    
    def genstatic(f, f_type, name, docstring=None):
        def picostatic(*args):
            return f(*args)
        picostatic.func_name = name
        picostatic.__doc__ = docstring
        return staticmethod(picostatic)
    
    # Add all functions taking PicoSAT * as their first argument as methods 
    # of PicoSAT; add other picosat_ functions as static methods.
    prefix = 'picosat_'
    for fname in (n for n in dir(_picosat) if n.startswith(prefix)):
        func = getattr(_picosat, fname)
        func_type = ffi.typeof(func)
        short_name = fname[len(prefix):]
        if short_name == "print":
            short_name = "print_"
        if (hasattr(PicoSAT, short_name)
                or not func_type.args
                or func_type.args[0] != picosat_type):
            new_func = genstatic(func, func_type, short_name, 
                                 docstrings.doc.get(fname))
        else:
            new_func = genfn(func, func_type, short_name, 
                             docstrings.doc.get(fname)) 
        setattr(PicoSAT, short_name, new_func)

    const_prefix = 'PICOSAT_'
    for cname in (n for n in dir(_picosat) if n.startswith(const_prefix)):
        setattr(PicoSAT, cname[len(const_prefix):], getattr(_picosat, cname))

_init()
