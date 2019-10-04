#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bincrafters import build_template_default


def _is_shared_msvc_build(build):
    return not(build.options['benchmark:shared'] == True and build.settings['compiler'] == 'Visual Studio')


if __name__ == "__main__":

    builder = build_template_default.get_builder()
    filter(_is_shared_msvc_build, builder.items)

    builder.run()
