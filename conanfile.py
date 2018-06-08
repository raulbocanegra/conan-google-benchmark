#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os

class GoogleBenchmarkConan(ConanFile):
    name = "google_benchmark"
    version = "1.4.1"
    description = "A library to support the benchmarking of functions, similar to unit-tests."
    url = "https://github.com/raulbocanegra/conan-google-benchmark"
    homepage = "https://github.com/google/benchmark"
    # Indicates License type of the packaged library
    license = "https://github.com/raulbocanegra/conan-google-benchmark"
    # Packages the license for the conanfile.py
    exports = ["LICENSE.md"]

    # Remove following lines if the target lib does not use cmake.
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    # Options may need to change depending on the packaged library.
    settings = "os", "arch", "compiler", "build_type"
    options =  {
        "fPIC": [True, False], 
        "enable_testing": [True, False], 
        "enable_exceptions": [True, False], 
        "enable_lto":[True, False]
    }
    default_options = "fPIC=True", "enable_testing=False", "enable_exceptions=True", "enable_lto=False" 

    # Custom attributes for Bincrafters recipe conventions
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC            

    def source(self):        
        source_url = "https://github.com/google/benchmark"
        tools.get("{0}/archive/v{1}.zip".format(source_url, self.version))
        extracted_dir = "benchmark-" + self.version

        #Rename to "source_subfolder" is a convention to simplify later steps
        os.rename(extracted_dir, self.source_subfolder)        
        
    def configure_cmake(self):
        cmake = CMake(self)        
        if self.settings.os != 'Windows':
            cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = "ON" if self.options.fPIC else "OFF"
        cmake.definitions['BENCHMARK_ENABLE_TESTING'] = "ON" if self.options.enable_testing else "OFF"
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
        # TODO: on Solaris add "kstat"
        if self.settings.os == "Windows":
            self.cpp_info.libs.append("Shlwapi")
        elif self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")
