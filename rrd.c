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

static int isquote(char x) {
	return x == '\'' || x == '\"';
}

static int isescape(char x) {
	return x == '\\';
}

static int rrd_parse_arguments(char* command) {
	char* it;
	char* out;
	struct {
		enum { space, nospace } s;
		union {
			struct {
				char quoted_char;
				unsigned int escaped : 1;
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
					state.s_nospace.escaped = isescape(*it);
					state.s_nospace.quoted_char = isquote(*it) ? *it : 0;

					if (!isescape(*it) && !isquote(*it))
						*(out++) = *it;
				}
			break;
			case nospace:
				if (state.s_nospace.escaped) {
					if (state.s_nospace.quoted_char
						&& !(*it == state.s_nospace.quoted_char || isescape(*it))) {

						*(out++) = '\\';
					}
					*(out++) = *it;
					state.s_nospace.escaped = 0;
					break;
				} else if (isescape(*it)) {
					state.s_nospace.escaped = 1;
				} else if (state.s_nospace.quoted_char == *it) {
					state.s_nospace.quoted_char = 0;
				} else if (!state.s_nospace.quoted_char && isquote(*it)) {
					state.s_nospace.quoted_char = *it;
				} else if (!state.s_nospace.quoted_char && isspace(*it)) {
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

	int    i;
	char*  it;
	int    argc;
	char** argv;
	char*  format;
	char*  command;
	int    command_argc;
	char*  command_args;
	char*  upper_format;

	rrd_info_t* rrd_info;
	rrd_info_t* rrd_info_it;

	if (!PyArg_ParseTuple(args, "ss", &command, &format))
		return NULL;

	upper_format = strdup(format);
	if (upper_format == NULL) {
		PyErr_SetString(PyExc_MemoryError, "strdup: Out of memory");
		goto err_strdup_format;
	}
	for (it = upper_format; *it != '\0'; ++it) {
		*it = toupper(*it);
	}

	command_args = strdup(command);
	if (command_args == NULL) {
		PyErr_SetString(PyExc_MemoryError, "strdup: Out of memory");
		goto err_strdup_command;
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
	argv[argc++] = upper_format;

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
err_strdup_command:
	free(upper_format);
err_strdup_format:
	return ret;
}

static PyObject*
rrd_split(PyObject* self, PyObject* args) {
	PyObject* ret = NULL;

	int   i;
	char* it;
	char* command;
	int   command_argc;
	char* command_args;

	if (!PyArg_ParseTuple(args, "s", &command))
		return NULL;

	command_args = strdup(command);
	if (command_args == NULL) {
		PyErr_SetString(PyExc_MemoryError, "strdup: Out of memory");
		goto err_strdup_command;
	}
	command_argc = rrd_parse_arguments(command_args);

	ret = PyList_New(command_argc);
	if (ret == NULL)
		goto err_PyList_New;

	for (i = 0, it = command_args; i < command_argc; ++i, ++it) {
		PyList_SET_ITEM(ret, i, PyBytes_FromString(it));
		for(; *it != '\0'; ++it);
	}

err_PyList_New:
	free(command_args);
err_strdup_command:
	return ret;
}

static PyMethodDef RRDMethods[] = {
	{"render", rrd_render, METH_VARARGS, NULL},
	{"split", rrd_split, METH_VARARGS, NULL},
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
