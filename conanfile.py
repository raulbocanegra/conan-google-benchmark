#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os

class GoogleBenchmarkConan(ConanFile):
    name = "benchmark"
    version = "1.4.1"
    description = "A library to support the benchmarking of functions, similar to unit-tests."
    url = "https://github.com/raulbocanegra/conan-google-benchmark"
    homepage = "https://github.com/google/benchmark"
    license = "https://github.com/raulbocanegra/conan-google-benchmark"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False], 
        "enable_testing": [True, False], 
        "enable_exceptions": [True, False], 
        "enable_lto":[True, False],
        "enable_gtest_tests": [True, False] 
    }
    default_options = "shared=False", "fPIC=True", "enable_testing=False", "enable_exceptions=True", "enable_lto=False", "enable_gtest_tests=True"

    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC
            del self.options.shared

    def source(self):        
        source_url = "https://github.com/google/benchmark"
        tools.get("{0}/archive/v{1}.zip".format(source_url, self.version))
        extracted_dir = "benchmark-" + self.version
        os.rename(extracted_dir, self.source_subfolder)        
        
    def configure_cmake(self):
        cmake = CMake(self)        
        cmake.definitions['BENCHMARK_ENABLE_TESTING'] = "ON" if self.options.enable_testing else "OFF"
        cmake.definitions['BENCHMARK_ENABLE_GTEST_TESTS'] = "ON" if self.options.enable_gtest_tests else "OFF"
        cmake.definitions['BENCHMARK_BUILD_32_BITS'] = "ON" if self.settings.arch == "x86" and self.settings.compiler != "Visual Studio"  else "OFF"

        cmake.configure(build_folder=self.build_subfolder)
        return cmake

    def build_requirements(self):
        self.build_requires("gtest/1.8.0@bincrafters/stable")   
    
    def build(self):
        cmake = self.configure_cmake()
        cmake.build()
        
    def package(self):
        self.copy(pattern="LICENSE", dst="license", src=self.source_subfolder)
        cmake = self.configure_cmake()
        cmake.install()        

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Windows":
            self.cpp_info.libs.append("Shlwapi")
        elif self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")
