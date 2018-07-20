#!/usr/bin/env python
# -*- coding: utf-8 -*-


from bincrafters import build_template_default
import platform

if __name__ == "__main__":

    builder = build_template_default.get_builder()
    not_suported_builds = []
    os_name = platform.system()
    for build in builder.items:
        settings, options, env_vars, build_requires, reference = build
        if (settings["compiler"] == "Visual Studio" and settings["arch"] == "x86") or (os_name == "Windows" and options["benchmark:shared"]):
            not_suported_builds.append(build)
        
    for not_supported in not_suported_builds:
        builder.items.remove(not_supported)
    builder.run()