project('robotpy-rev', ['cpp'],
        default_options: ['warning_level=1', 'cpp_std=c++20',
                          'b_colorout=auto', 'optimization=2', 'b_pie=true'])

subdir('semiwrap')

rev_sources += files(
  'rev/rev.cpp',
)

#
# Static link 
#

cpp = meson.get_compiler('cpp')
libs_path = meson.current_source_dir() + '/lib/lib'

rev_deps += [
    cpp.find_library('BackendDriver', dirs: libs_path),
    cpp.find_library('REVLibWpi', dirs: libs_path),
    cpp.find_library('REVLibDriver', dirs: libs_path),
    cpp.find_library('REVLib', dirs: libs_path),
]

subdir('semiwrap/modules')
