import os

from conans import ConanFile, CMake, tools


class RpclibConan(ConanFile):
    name = "rpclib"
    version = "2.2.1"
    license = "MIT"
    url = "https://github.com/rpclib/rpclib-conan"
    description = "RPC for modern C++"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
        archive = "rpclib.zip"
        tools.download(
            "https://github.com/rpclib/rpclib/archive/"
            "v{v}.zip".format(v=self.version),
            archive)
        tools.unzip(archive)
        os.unlink(archive)

    def config_options(self):
        compiler = self.settings.compiler
        version = float(str(compiler.version))
        if compiler == "gcc" and version < 4.8:
            raise ValueError("The minimum supported GCC version is 4.8")
        elif compiler == "clang" and version < 3.7:
            raise ValueError("The minimum supported clang version is 3.7")
        elif compiler == "apple-clang" and version < 8.0:
            raise ValueError(
                "The minimum supported Apple Clang version is 8.0")

    def build(self):
        self.cmake = CMake(self, parallel=True)
        compiler = self.settings.compiler
        if compiler == "Visual Studio" and "MT" in str(compiler.runtime):
            self.cmake.definitions["RPCLIB_MSVC_STATIC_RUNTIME"] = "ON"
        elif str(compiler) in ("gcc", "clang", "apple-clang"):
            if self.settings.arch == 'x86':
                self.cmake.definitions["CMAKE_C_FLAGS"] = "-m32"
                self.cmake.definitions["CMAKE_CXX_FLAGS"] = "-m32"
            elif self.settings.arch == 'x86_64':
                self.cmake.definitions["CMAKE_C_FLAGS"] = "-m64"
                self.cmake.definitions["CMAKE_CXX_FLAGS"] = "-m64"
        self.cmake.configure(source_dir="rpclib-{0}".format(self.version))
        self.cmake.build()

    def package(self):
        self.cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["rpc"]
