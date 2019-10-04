#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
from conans.errors import ConanInvalidConfiguration
import os


class GoogleBenchmarkConan(ConanFile):
    name = "benchmark"
    version = "1.4.1"
    description = "A microbenchmark support library "
    url = "https://github.com/raulbocanegra/conan-google-benchmark"
    homepage = "https://github.com/google/benchmark"
    license = "Apache-2.0"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False], 
        "enable_exceptions": [True, False], 
        "enable_lto":[True, False]
    }
    default_options = "shared=False", "fPIC=True", "enable_exceptions=True", "enable_lto=False"

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC
            del self.options.shared  # See https://github.com/google/benchmark/issues/639 - no Windows shared support for now
            if self.settings.compiler == "Visual Studio" and float(self.settings.compiler.version.value) <= 12:
                raise ConanInvalidConfiguration("{} {} does not support Visual Studio <= 12".format(self.name, self.version))
        if self.options.enable_testing == False:
            self.options.enable_gtest_tests = False

    def source(self):        
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)     
        
    def _configure_cmake(self):
        cmake = CMake(self)        
        cmake.definitions["BENCHMARK_ENABLE_TESTING"] = "OFF"
        cmake.definitions["BENCHMARK_ENABLE_GTEST_TESTS"] = "OFF"
        cmake.definitions['BENCHMARK_BUILD_32_BITS'] = "ON" if self.settings.arch == "x86" and self.settings.compiler != "Visual Studio" else "OFF"
        cmake.definitions["BENCHMARK_ENABLE_LTO"] = "ON" if self.options.enable_lto else "OFF"
        cmake.definitions["BENCHMARK_ENABLE_EXCEPTIONS"] = "ON" if self.options.enable_exceptions else "OFF"

        if self.settings.os != "Windows":
            cmake.definitions["BENCHMARK_USE_LIBCXX"] = "ON" if (str(self.settings.compiler.libcxx) == "libc++") else "OFF"

        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()
        
    def package(self):
        self.copy(pattern="LICENSE", dst="license", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()        

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Windows":
            self.cpp_info.libs.append("Shlwapi")
        elif self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")
        elif self.settings.os == "SunOS":
            self.cpp_info.libs.append("kstat")
