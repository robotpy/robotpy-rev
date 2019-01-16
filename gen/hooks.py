import sphinxify

_annotations = {
    "short": "int",
    "int": "int",
    "unsigned int": "int",
    "uint8_t": "int",
    "uint16_t": "int",
    "int32_t": "int",
    "uint32_t": "int",
    "size_t": "int",
    "double": "float",
    "char": "str",
    "bool": "bool",
    "rev::CANError": "CANError",
    "std::vector<uint8_t>": "typing.List[int]",
    "std::string": "str",
    "void": "None",
}

# fmt: off

def _gen_check(pname, ptype, strict=False):

    # TODO: This does checks on normal types, but if you pass a ctypes value
    #       in then this does not check those properly.

    if ptype == 'bool':
        return 'isinstance(%s, bool)' % pname

    elif ptype in ['float', 'double']:
        if strict:
            return 'isinstance(%s, (float))' % pname
        else:
            return 'isinstance(%s, (int, float))' % pname

    #elif ptype is C.c_char:
    #    return 'isinstance(%s, bytes) and len(%s) == 1' % (pname, pname)
    #elif ptype is C.c_wchar:
    #    return 'isinstance(%s, str) and len(%s) == 1' % (pname, pname)
    #elif ptype is C.c_char_p:
    #    return "%s is None or isinstance(%s, bytes) or getattr(%s, '_type_') is _C.c_char" % (pname, pname, pname)
    #elif ptype is C.c_wchar_p:
    #    return '%s is None or isinstance(%s, bytes)' % (pname, pname)

    elif ptype in ['int', 'long']:
        return 'isinstance(%s, int)' % pname
    #elif ptype in [C.c_byte, C.c_int8]:
    #    return 'isinstance(%s, int) and %s < %d and %s > -%d' % (pname, pname, 1<<7, pname, 1<<7)
    elif ptype in ['short', 'int16_t']:
        return 'isinstance(%s, int) and %s < %d and %s > -%d' % (pname, pname, 1<<15, pname, 1<<15)
    elif ptype == 'int32_t':
        return 'isinstance(%s, int) and %s < %d and %s > -%d' % (pname, pname, 1<<31, pname, 1<<31)
    elif ptype == 'int64_t':
        return 'isinstance(%s, int) and %s < %d and %s > -%d' % (pname, pname, 1<<63, pname, 1<<63)

    elif ptype == 'size_t':
        return 'isinstance(%s, int)' % (pname)
    elif ptype == 'uint8_t':
        return 'isinstance(%s, int) and %s < %d and %s >= 0' % (pname, pname, 1<<8, pname)
    elif ptype == 'uint16_t':
        return 'isinstance(%s, int) and %s < %d and %s >= 0' % (pname, pname, 1<<16, pname)
    elif ptype == 'uint32_t':
        return 'isinstance(%s, int) and %s < %d and %s >= 0' % (pname, pname, 1<<32, pname)
    elif ptype == 'uint64_t':
        return 'isinstance(%s, int) and %s < %d and %s >= 0' % (pname, pname, 1<<64, pname)

    elif ptype is None:
        return '%s is None' % pname
    
    elif ptype.startswith("rev::"):
        return 'isinstance(%s, %s)' % (pname, ptype.rsplit("::", 1)[1])

    else:
        # TODO: do validation here
        #return 'isinstance(%s, %s)' % (pname, type(ptype).__name__)
        return None

# fmt: on


def _to_annotation(ctypename):
    computed = ctypename.replace("&", "").strip()
    idx = computed.rfind("::")
    if idx != -1:
        computed = computed[idx + 2 :]
    return _annotations.get(ctypename, computed)


def header_hook(header, data):
    """Called for each header"""

    for e in header.enums:
        e["x_namespace"] = e["namespace"]


def public_method_hook(fn, data):
    # Ignore operators, move constructors, copy constructors
    if (
        fn["name"].startswith("operator")
        or fn.get("destructor")
        or (fn.get("constructor") and fn["parameters"][0]["name"] == "&")
    ):
        fn["data"] = {"ignore": True}
        return

    # Python exposed function name converted to camelcase
    x_name = fn["name"]
    x_name = x_name[0].lower() + x_name[1:]

    x_in_params = []
    x_out_params = []
    x_rets = []

    # Simulation assertions
    x_param_checks = []
    x_return_checks = []

    data = data.get(fn["name"])
    if data is None:
        # ensure every function is in our yaml
        print("WARNING:", fn["parent"]["name"], "method", fn["name"], "missing")
        data = {}
        # assert False, fn['name']

    param_defaults = data.get("defaults", {})
    param_override = data.get("param_override", {})

    for i, p in enumerate(fn["parameters"]):
        if p["name"] == "":
            p["name"] = "param%s" % i
        p["x_type"] = p.get("enum", p["raw_type"])
        p["x_callname"] = p["name"]

        # Python annotations for sim
        p["x_pyann_type"] = _to_annotation(p["x_type"])
        if "forward_declared" in p:
            p["x_pyann_type"] = repr(p["x_pyann_type"])
            fn["forward_declare"] = True
        p["x_pyann"] = "%(name)s: %(x_pyann_type)s" % p
        p["x_pyarg"] = 'py::arg("%(name)s")' % p

        if p["name"] in param_defaults:
            _pname = param_defaults.pop(p["name"])
            p["x_pyann"] += " = " + str(_pname)
            p["x_pyarg"] += "=" + str(_pname)
        elif p["name"].lower() == "timeoutms":
            p["x_pyann"] += " = 0"
            p["x_pyarg"] += "=0"

        if p["name"] in param_override:
            p.update(param_override[p["name"]])
            x_in_params.append(p)
        elif p["pointer"]:
            p["x_callname"] = "&%(x_callname)s" % p
            x_out_params.append(p)
        elif p["array"]:
            asz = p.get("array_size", 0)
            if asz:
                p["x_pyann_type"] = "typing.List[%s]" % _to_annotation(p["raw_type"])
                p["x_type"] = "std::array<%s, %s>" % (p["x_type"], asz)
                p["x_callname"] = "%(x_callname)s.data()" % p
            else:
                # it's a vector
                pass

            x_out_params.append(p)
        else:
            chk = _gen_check(p["name"], p["x_type"])
            if chk:
                x_param_checks.append("assert %s" % chk)
            x_in_params.append(p)

        p["x_type"] += "&" * p["reference"]
        p["x_decl"] = "%s %s" % (p["x_type"], p["name"])

    assert not param_defaults

    x_callstart = ""
    x_callend = ""
    x_wrap_return = ""

    # Return all out parameters
    x_rets.extend(x_out_params)

    # if the function has out parameters and if the return value
    # is an error code, suppress the error code. This matches the Java
    # APIs, and the user can retrieve the error code from getLastError if
    # they really care
    if not len(x_rets) and fn["rtnType"] != "void":
        x_callstart = "auto __ret ="
        x_rets.insert(
            0,
            dict(
                name="__ret",
                x_type=fn["rtnType"],
                x_pyann_type=_to_annotation(fn["rtnType"]),
            ),
        )

        # Save some time in the common case -- set the error code to 0
        # if there's a single retval and the type is ErrorCode
        if fn["rtnType"] == "CANError":
            x_param_checks.append("retval = CANError.kOK")

    if len(x_rets) == 1 and x_rets[0]["x_type"] != "void":
        x_wrap_return = "return %s;" % x_rets[0]["name"]
        x_wrap_return_type = x_rets[0]["x_type"]
        x_pyann_ret = x_rets[0]["x_pyann_type"]
        chk = _gen_check("retval", x_wrap_return_type, strict=True)
        if chk:
            x_return_checks.append("assert %s" % chk)
    elif len(x_rets) > 1:
        x_pyann_ret = "typing.Tuple[%s]" % (
            ", ".join([p["x_pyann_type"] for p in x_rets]),
        )

        x_wrap_return = "return std::make_tuple(%s);" % ",".join(
            [p["name"] for p in x_rets]
        )
        x_wrap_return_type = "std::tuple<%s>" % (
            ", ".join([p["x_type"] for p in x_rets])
        )

        x_return_checks.append(
            "assert isinstance(retval, tuple) and len(retval) == %s" % len(x_rets)
        )
        for i, _p in enumerate(x_rets):
            chk = _gen_check("retval[%d]" % i, _p["raw_type"], strict=True)
            if chk:
                x_return_checks.append("assert %s" % chk)
    else:
        x_pyann_ret = "None"
        x_wrap_return_type = "void"

    # Temporary values to store out parameters in
    x_temprefs = ""
    if x_out_params:
        x_temprefs = ";".join(["%(x_type)s %(name)s" % p for p in x_out_params]) + ";"

    if "return" in data.get("code", ""):
        raise ValueError("%s: Do not use return, assign to retval instead" % fn["name"])

    # Rename internal functions
    if data.get("internal", False):
        x_name = "_" + x_name
    elif data.get("rename", False):
        x_name = data["rename"]
    elif fn["constructor"]:
        x_name = "__init__"

    if "doc" in data:
        doc = data["doc"]
    elif "doxygen" in fn:
        # work around a CppHeaderParser bug
        doc = fn["doxygen"].rpartition("*//*")[2]
        doc = sphinxify.process_raw(doc)

    name = fn["name"]

    hascode = "code" in data or "get" in data or "set" in data

    # lazy :)
    fn.update(locals())


def class_hook(cls, data):
    # work around CppHeaderParser hoisting structs nested in classes to top
    if cls["parent"] is not None:
        cls["data"] = {"ignore": True}
        return

    data = data.get("data", {})
    data = data.get(cls["name"])
    if data is None:
        print("WARNING: class", cls["name"], "missing")
        data = {}

    # fix enum paths
    for e in cls["enums"]["public"]:
        e["x_namespace"] = e["namespace"] + "::" + cls["name"] + "::"

    cls["data"] = data
    for fn in cls["methods"]["public"]:
        public_method_hook(fn, data)
