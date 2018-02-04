#include <Python.h>
#include <ctype.h>
#include <rrd.h>

/*
 * # Implementation note
 *
 * There are at least three different versions of existing rrd python
 * bindings: old upstream, new upstream, and python-rrdtool from PyPi. In
 * order to ensure good user experience for all librrd versions and
 * installation ways (pip, distribution packaging manager, etc.), we use our
 * tiny wrapper here and don't rely on existing solutions.
 *
 * Unfortunately, some existing python bindings as well as librrd itself also
 * have multithreading issues. For instance:
 * * https://github.com/oetiker/rrdtool-1.x/issues/867
 * * https://github.com/oetiker/rrdtool-1.x/issues/865
 *
 * This is limiting, because modern Django starts multithreading application
 * even when simple `manage.py runserver` invoced. Our current implementation
 * assumes that librrd calls are protected by Python GIL. So as long as you
 * don't use librrd from packages other than that, it is safe to run
 * multithreading application. If future versions of librrd become reentrant,
 * then additional optimizations can be also performed in this module:
 * depending on using librrd version Python GIL may be released before
 * `rrdgraph_v()` call and aquired after that leading to real multithreading.
 */

static PyObject* RRDError;

static int rrd_parse_arguments(char* command) {
	char* it;
	char* out;
	struct {
		enum { space, nospace } s;
		union {
			struct {
				unsigned int escaped : 1;
				unsigned int quoted : 1;
			} s_nospace;
		};
	} state = { space };
	int argc;

	for (it = command, out = command, argc = 0; *it != '\0'; ++it) {
		switch (state.s) {
			case space:
				if (!isspace(*it)) {
					argc++;
					state.s = nospace;
					state.s_nospace.escaped = (*it == '\\');
					state.s_nospace.quoted = (*it == '\"');

					if (*it != '\\' && *it != '\"')
						*(out++) = *it;
				}
			break;
			case nospace:
				if (state.s_nospace.escaped) {
					*(out++) = *it;
					state.s_nospace.escaped = 0;
					break;
				} else if (*it == '\\') {
					state.s_nospace.escaped = 1;
				} else if (*it == '\"') {
					state.s_nospace.quoted = ~state.s_nospace.quoted;
				} else if (!state.s_nospace.quoted && isspace(*it)) {
					state.s = space;
					*(out++) = '\0';
				} else {
					*(out++) = *it;
				}
			break;
		}
	}
	*out = '\0';

	return argc;
}

static PyObject*
rrd_render(PyObject* self, PyObject* args) {
	PyObject* ret = NULL;

	char* command;
	char* format;

	char* command_args;
	int command_argc;

	char** argv;
	int argc;
	char* it;
	int i;

	rrd_info_t* rrd_info;
	rrd_info_t* rrd_info_it;

	if (!PyArg_ParseTuple(args, "ss", &command, &format))
		return NULL;

	command_args = strdup(command);
	if (command_args == NULL) {
		PyErr_SetString(PyExc_MemoryError, "strdup: Out of memory");
		goto err_strdup;
	}
	command_argc = rrd_parse_arguments(command_args);

	argv = PyMem_New(char*, 3 + 1 + command_argc + 1);
	if (argv == NULL) {
		PyErr_SetString(PyExc_MemoryError, "PyMem_New: Out of memory");
		goto err_PyMem_New;
	}

	argc = 0;
	argv[argc++] = "graph";
	argv[argc++] = "-";
	argv[argc++] = "--imgformat";
	argv[argc++] = format;

	for (i = 0, it = command_args; i < command_argc; ++i, ++it) {
		argv[argc++] = it;
		for(; *it != '\0'; ++it);
	}

	argv[argc] = NULL;

	rrd_info = rrd_graph_v(argc, argv);
	if (rrd_info == NULL) {
		PyErr_SetString(RRDError, rrd_get_error());
		rrd_clear_error();
		goto err_rrd_graph;
	}

	for (rrd_info_it = rrd_info;
		rrd_info_it != NULL && strcmp(rrd_info_it->key, "image") != 0;
		rrd_info_it = rrd_info_it->next);

	if (rrd_info_it == NULL) {
		PyErr_SetString(RRDError, "No image found in rrd_graph_v result");
		goto err_rrd_graph_image;
	}

	if (rrd_info_it->type != RD_I_BLO) {
		PyErr_SetString(RRDError, "rrd_graph_v produces wrong type result");
		goto err_rrd_graph_image;
	}

	ret = PyBytes_FromStringAndSize(
		(const char*)(rrd_info_it->value.u_blo.ptr),
		rrd_info_it->value.u_blo.size);
	if (ret == NULL)
		goto err_PyByteArray;

err_PyByteArray:
err_rrd_graph_image:
	rrd_info_free(rrd_info);
err_rrd_graph:
	PyMem_Del(argv);
err_PyMem_New:
	free(command_args);
err_strdup:
	return ret;
}

static PyMethodDef RRDMethods[] = {
	{"render", rrd_render, METH_VARARGS, NULL},
	{NULL, NULL, 0, NULL}
};

#if PY_MAJOR_VERSION >= 3
static struct PyModuleDef rrdmodule = {
	PyModuleDef_HEAD_INIT,
	"rrd",
	NULL,
	-1,
	RRDMethods
};
#endif // PY_MAJOR_VERSION >= 3

PyMODINIT_FUNC
#if PY_MAJOR_VERSION >= 3
PyInit_rrd(void) {
#else
initrrd(void) {
#endif // PY_MAJOR_VERSION >= 3
	PyObject* m;

#if PY_MAJOR_VERSION >= 3
	m = PyModule_Create(&rrdmodule);
	if (!m) return NULL;
#else
	m = Py_InitModule("rrd", RRDMethods);
	if (!m) return;
#endif // PY_MAJOR_VERSION >= 3

	RRDError = PyErr_NewException("rrd.RRDError", NULL, NULL);
	Py_INCREF(RRDError);
	PyModule_AddObject(m, "RRDError", RRDError);

#if PY_MAJOR_VERSION >= 3
	return m;
#endif // PY_MAJOR_VERSION >= 3
}
