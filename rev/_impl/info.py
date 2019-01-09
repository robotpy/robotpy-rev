class Info:
    def module_info(self):
        from .. import version

        return "REV bindings", version.__version__, version.__rev_version__
