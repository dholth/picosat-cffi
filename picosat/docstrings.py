doc = {'': '', 'picosat_add': 'Add a literal of the next clause.  A zero terminates the clause.  The\nsolver is incremental.  Adding a new literal will reset the previous\nassignment.   The return value is the original clause index to which\nthis literal respectively the trailing zero belong starting at 0.\n ', 'picosat_simplify': "Force immmediate removal of all satisfied clauses and clauses that are\nadded or generated in closed contexts.  This function is called\ninternally if enough units are learned or after a certain number of\ncontexts have been closed.  This number is fixed at compile time\nand defined as MAXCILS in 'picosat.c'.\n\nNote that learned clauses which only involve outer contexts are kept.\n ", 'picosat_add_lits': 'As the previous function but with an at compile time unknown size.\n ', 'picosat_set_more_important_lit': 'Set some variables to be more important than others.  These variables are\nalways used as decisions before other variables are used.  Dually there\nis a set of variables that is used last.  The default is\nto mark all variables as being indifferent only.\n ', 'picosat_remove_learned': 'Reset assignment if in SAT state and then remove the given percentage of\nless active (large) learned clauses.  If you specify 100% all large\nlearned clauses are removed.\n ', 'picosat_changed': "Assume that a previous call to 'picosat_sat' in incremental usage,\nreturned 'SATISFIABLE'.  Then a couple of clauses and optionally new\nvariables were added (a new variable is a variable that has an index\nlarger then the maximum variable added so far).  The next call to\n'picosat_sat' also returns 'SATISFIABLE'. If this function\n'picosat_changed' returns '0', then the assignment to the old variables\ndid not change.  Otherwise it may have changed.   The return value to\nthis function is only valid until new clauses are added through\n'picosat_add', an assumption is made through 'picosat_assume', or again\n'picosat_sat' is called.  This is the same assumption as for\n'picosat_deref'.\n\nTODO currently this function may also return a non zero value even if the\nold assignment did not change, because it only checks whether the\nassignment of at least one old variable was flipped at least once during\nthe search.  In principle it should be possible to be exact in the other\ndirecetion as well by using a counter of variables that have an odd\nnumber of flips.  But this is not implemented yet.\n ", 'picosat_add_arg': 'As the previous function, but allows to add a full clause at once with an\nat compiled time known size.  The list of argument literals has to be\nterminated with a zero literal.  Literals beyond the first zero literal\nare discarded.\n ', 'picosat_inconsistent': 'Returns non zero if the CNF is unsatisfiable because an empty clause was\nadded or derived.\n ', 'picosat_add_ado_lit': "This is an experimental feature for handling 'all different constraints'\n(ADC).  Currently only one global ADC can be handled.  The bit-width of\nall the bit-vectors entered in this ADC (stored in 'all different\nobjects' or ADOs) has to be identical.\n\nTODO: also handle top level assigned literals here.\n ", 'picosat_reset_scores': 'Scores can be erased as well.  Note, however, that even after erasing \nscores and phases, learned clauses are kept.  In addition head tail\npointers for literals are not moved either.  So expect a difference\nbetween calling the solver in incremental mode or with a fresh copy of\nthe CNF.\n ', 'picosat_failed_assumption': "Returns non zero if the literal is a failed assumption, which is defined\nas an assumption used to derive unsatisfiability.  This is as accurate as\ngenerating core literals, but still of course is an overapproximation of\nthe set of assumptions really necessary.  The technique does not need\nclausal core generation nor tracing to be enabled and thus can be much\nmore effective.  The function can only be called as long the current\nassumptions are valid.  See 'picosat_assume' for more details.\n ", 'picosat_deref': "After 'picosat_sat' was called and returned 'PICOSAT_SATISFIABLE', then\nthe satisfying assignment can be obtained by 'dereferencing' literals.\nThe value of the literal is return as '1' for 'true',  '-1' for 'false'\nand '0' for an unknown value.\n ", 'picosat_set_global_default_phase': 'Set default initial phase: \n\n  0 = false\n  1 = true\n  2 = Jeroslow-Wang (default)\n  3 = random initial phase\n\nAfter a variable has been assigned the first time, it will always\nbe assigned the previous value if it is picked as decision variable.\nThe initial assignment can be chosen with this function.\n ', 'picosat_set_default_phase_lit': "Set next/initial phase of a particular variable if picked as decision\nvariable.  Second argument 'phase' has the following meaning:\n\n  negative = next value if picked as decision variable is false\n\n  positive = next value if picked as decision variable is true\n\n  0        = use global default phase as next value and\n             assume 'lit' was never assigned\n\nAgain if 'lit' is assigned afterwards through a forced assignment,\nthen this forced assignment is the next phase if this variable is\nused as decision variable.\n ", 'picosat_enable_trace_generation': "If you ever want to extract cores or proof traces with the current\ninstance of PicoSAT initialized with 'picosat_init', then make sure to\ncall 'picosat_enable_trace_generation' right after 'picosat_init'.   This\nis not necessary if you only use 'picosat_set_incremental_rup_file'.\n\nNOTE, trace generation code is not necessarily included, e.g. if you\nconfigure picosat with full optimzation as './configure -O' or with\n \nyou do not get any results by trying to generate traces.\n\nThe return value is non-zero if code for generating traces is included\nand it is zero if traces can not be generated.\n ", 'picosat_set_output': "Set output file, default is 'stdout'.\n ", 'picosat_measure_all_calls': "Measure all time spent in all calls in the solver.  By default only the\ntime spent in 'picosat_sat' is measured.  Enabling this function may for\ninstance triple the time needed to add large CNFs, since every call to\n'picosat_add' will trigger a call to 'getrusage'.\n ", 'picosat_variables': 'Statistics.\n ', 'picosat_coreclause': "This function determines whether the i'th added original clause is in the\ncore.  The 'i' is the return value of 'picosat_add', which starts at zero\nand is incremented by one after a original clause is added (that is after\n'picosat_add (0)').  For the index 'i' the following has to hold: \n\n  0 <= i < picosat_added_original_clauses ()\n ", 'picosat_res': "Return last result of calling 'picosat_sat' or '0' if not called.\n ", 'picosat_context': 'Returns the literal that assumes the current context or zero if the\nouter context has been reached.\n ', 'picosat_inc_max_var': "This function returns the next available unused variable index and\nallocates a variable for it even though this variable does not occur as\nassumption, nor in a clause or any other constraints.  In future calls to\n'picosat_sat', 'picosat_deref' and particularly for 'picosat_changed',\nthis variable is treated as if it had been used.\n ", 'picosat_write_rup_trace': "Write a RUP trace to a file.  This trace file contains only the learned\ncore clauses while this is not necessarily the case for the RUP file\nobtained with 'picosat_set_incremental_rup_file'.\n ", 'picosat_set_prefix': 'Set the prefix used for printing verbose messages and statistics.\nDefault is "c ".\n ', 'picosat_set_propagation_limit': "As alternative to a decision limit you can use the number of propagations\nas limit.  This is more linearly related to execution time. This has to\nbe called after 'picosat_init' and before 'picosat_sat'.\n ", 'picosat_sat': "Call the main SAT routine.  A negative decision limit sets no limit on\nthe number of decisions.  The return values are as above, e.g.\n'PICOSAT_UNSATISFIABLE', 'PICOSAT_SATISFIABLE', or 'PICOSAT_UNKNOWN'.\n ", 'picosat_deref_partial': "After 'picosat_sat' was called and returned 'PICOSAT_SATISFIABLE' a\npartial satisfying assignment can be obtained as well.  It satisfies all\noriginal clauses.  The value of the literal is return as '1' for 'true',\n'-1' for 'false' and '0' for an unknown value.  In order to make this\nwork all original clauses have to be saved internally, which has to be\nenabled by 'picosat_save_original_clauses' right after initialization.\n ", 'picosat_set_incremental_rup_file': 'You can dump proof traces in RUP format incrementally even without\nkeeping the proof trace in memory.  The advantage is a reduction of\nmemory usage, but the dumped clauses do not necessarily belong to the\nclausal core.  Beside the file the additional parameters denotes the\nmaximal number of variables and the number of original clauses.\n ', 'picosat_adjust': "If you know a good estimate on how many variables you are going to use\nthen calling this function before adding literals will result in less\nresizing of the variable table.  But this is just a minor optimization.\nBeside exactly allocating enough variables it has the same effect as\ncalling 'picosat_inc_max_var'.\n ", 'picosat_failed_context': "This is as 'picosat_failed_assumption', but only for internal variables\ngenerated by 'picosat_push'.\n ", 'picosat_reset_phases': 'You can reset all phases by the following function.\n ', 'picosat_assume': "You can add arbitrary many assumptions before the next 'picosat_sat'.\nThis is similar to the using assumptions in MiniSAT, except that you do\nnot have to collect all your assumptions yourself.  In PicoSAT you can\nadd one after the other before the next call to 'picosat_sat'.\n\nThese assumptions can be seen as adding unit clauses with those\nassumptions as literals.  However these assumption clauses are only valid\nfor exactly the next call to 'picosat_sat'.  And will be removed\nafterwards, e.g. in future calls to 'picosat_sat' after the next one they\nare not assumed, unless they are assumed again trough 'picosat_assume'.\n\nMore precisely, assumptions actually remain valid even after the next\ncall to 'picosat_sat' returns.  Valid means they remain 'assumed' until a\ncall to 'picosat_add', 'picosat_assume', or another 'picosat_sat,\nfollowing the first 'picosat_sat'.  They need to stay valid for\n'picosat_failed_assumption' to return correct values.  \n\nExample:\n\n  picosat_assume (1);        // assume unit clause '1 0'\n  picosat_assume (-2);       // additionally assume clause '-2 0'\n  res = picosat_sat (1000);  // assumes 1 and -2 to hold\n                             // 1000 decisions max.\n\n  if (res == PICOSAT_UNSATISFIABLE) \n    {\n      if (picosat_failed_assumption (1))\n        // unit clause '1 0' was necessary to derive UNSAT\n\n      if (picosat_failed_assumption (-2))\n        // unit clause '-2 0' was necessary to derive UNSAT\n\n      // at least one but also both could be necessary\n\n      picosat_assume (17);  // previous assumptions are removed\n                            // now assume unit clause '17 0' for\n                            // the next call to 'picosat_sat'\n\n      // adding a new clause, actually the first literal of\n      // a clause would also make the assumptions used in the previous\n      // call to 'picosat_sat' invalid.\n\n      // The first two assumptions above are not assumed anymore.  Only\n      // the assumptions, since the last call to 'picosat_sat' returned\n      // are assumed, e.g. the unit clause '17 0'.\n\n      res = picosat_sat (-1);\n    }\n  else if (res == PICOSAT_SATISFIABLE)\n    {\n      // now the assignment is valid and we can call 'picosat_deref'\n\n      assert (picosat_deref (1) == 1));\n      assert (picosat_deref (-2) == 1));\n\n      val = picosat_deref (15);\n\n      // previous two assumptions are still valid\n\n      // would become invalid if 'picosat_add' or 'picosat_assume' is\n      // called here, but we immediately call 'picosat_sat'.  Now when\n      // entering 'picosat_sat' the solver knows that the previous call\n      // returned SAT and it can safely reset the previous assumptions\n\n      res = picosat_sat (-1);\n    }\n  else\n    {\n      assert (res == PICOSAT_UNKNOWN);\n\n      // assumptions valid, but assignment invalid\n      // except for top level assigned literals which\n      // necessarily need to have this value if the formula is SAT\n\n      // as above the solver nows that the previous call returned UNKWOWN\n      // and will before doing anything else reset assumptions\n\n      picosat_sat (-1);\n    }\n ", 'picosat_pop': 'Closes the current context and recycles the literal generated for\nassuming this context.  The return value is the literal for the new\nouter context or zero if the outer most context has been reached.\n ', 'picosat_deref_toplevel': "Same as before but just returns true resp. false if the literals is\nforced to this assignment at the top level.  This function does not\nrequire that 'picosat_sat' was called and also does not internally reset\nincremental usage.\n ", 'picosat_set_verbosity': "Set verbosity level.  A verbosity level of 1 and above prints more and\nmore detailed progress reports on the output file, set by\n'picosat_set_output'.  Verbose messages are prefixed with the string set\nby 'picosat_set_prefix'.\n ", 'picosat_print': 'Print the CNF to the given file in DIMACS format.\n ', 'picosat_set_seed': 'Set a seed for the random number generator.  The random number generator\nis currently just used for generating random decisions.  In our\nexperiments having random decisions did not really help on industrial\nexamples, but was rather helpful to randomize the solver in order to\ndo proper benchmarking of different internal parameter sets.\n ', 'picosat_usedlit': "Keeping the proof trace around is not necessary if an over-approximation\nof the core is enough.  A literal is 'used' if it was involved in a\nresolution to derive a learned clause.  The core literals are necessarily\na subset of the 'used' literals.\n ", 'picosat_added_original_clauses': 'p cnf <m> n ', 'picosat_message': "Allows to print to internal 'out' file from client.\n ", 'picosat_stats': '... in process ', 'nmcs': "Compute the union of all minmal correcting sets, which is called\nthe 'high level union of all minimal unsatisfiable subset sets'.\n\nIt uses 'picosat_next_minimal_correcting_subset_of_assumptions' and\nthe same notes and advices apply.  In particular, this implies that\nafter calling the function once, the current CNF becomes inconsistent,\nand PicoSAT has to be reset.  So even this function internally uses\nPicoSAT incrementally, it can not be used incrementally itself at this\npoint.\n\nThe 'callback' can be used for progress logging and is called after\neach extracted minimal correcting set if non zero.  The 'nhumus'\nparameter of 'callback' denotes the number of assumptions found to be\npart of the HUMUS sofar.\n ", 'picosat_write_compact_trace': 'Write a proof trace in TraceCheck format to a file.\n ', 'picosat_reset': 'constructor ', 'picosat_write_clausal_core': 'Write the clauses that were used in deriving the empty clause to a file\nin DIMACS format.\n ', 'picosat_set_plain': "Disable/Enable all pre-processing, currently only failed literal probing.\n\n new_plain_value != 0    only 'plain' solving, so no preprocessing\n new_plain_value == 0    allow preprocessing\n ", 'picosat_save_original_clauses': "Save original clauses for 'picosat_deref_partial'.  See comments to that\nfunction further down.\n ", 'picosat_push': "Push/pop semantics for PicoSAT.   'picosat_push' opens up a new context.\nAll clauses added in this context are attached to it and discared when\nthe context is closed with 'picosat_pop'.  It is also possible to\nnest contexts.\n\nThe current implementation uses a new internal variable for each context.\nHowever, the indices for these internal variables are shared with\nordinary external variables.  This means that after any call to\n'picosat_push', new variable indices should be obtained with\n'picosat_inc_max_var' and not just by incrementing the largest variable\nindex used so far.\n\nThe return value is the index of the literal that assumes this context.\nThis literal can only be used for 'picosat_failed_context' otherwise\nit will lead to an API usage error.\n ", 'picosat_corelit': 'This function gives access to the variable core, which is made up of the\nvariables that were resolved in deriving the empty clause.\n '}