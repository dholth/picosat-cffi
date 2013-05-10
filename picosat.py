import os.path
import cffi

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
PicoSAT * picosat_minit (void * state,
    picosat_malloc,
    picosat_realloc,
    picosat_free);
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

class PicoSAT(object):
    def __init__(self):
        self._picosat = _picosat.picosat_init()

    def __del__(self):
        _picosat.picosat_reset(self._picosat)

def _init():
    """Create cffi binding."""
    global _picosat, ffi

    here = os.path.relpath(os.path.dirname(os.path.abspath(__file__)))
    lib = str(os.path.join(here, "picosat-956"))
    source = str(os.path.join(lib, "picosat.c"))
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
    
    # Add all functions taking PicoSAT * as their first argument...
    def genfn(f, name):
        def pico(self, *args):
            return f(self._picosat, *args)
        pico.func_name = name
        return pico

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
            continue
        setattr(PicoSAT, short_name, genfn(func, short_name))

    for cname in (n for n in dir(_picosat) if n.startswith('PICOSAT_')):
        setattr(PicoSAT, cname[8:], getattr(_picosat, cname))
        
_init()
